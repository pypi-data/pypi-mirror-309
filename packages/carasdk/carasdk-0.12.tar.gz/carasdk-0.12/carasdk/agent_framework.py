import inspect
import json
from typing import Callable, List, get_type_hints, TypedDict, Optional, Any, Dict, NewType, Union

from langchain_openai import ChatOpenAI
import uuid
import asyncio

from .prompt import get_prompt, get_prompt_with_ltm

from .ipc_sdk import get_instance_id, IpcSdk
from .log_config import setup_logger
from .stream_utils import run_langchain_with_output
from .memory import MemoryManager
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import Optional


logger = setup_logger('AgentFramework')


class AgentInfoData(TypedDict):
    instance_id: str
    description: str
    weight: int


class AgentInfo(TypedDict):
    type: str
    name: str
    data: Optional[AgentInfoData]


AgentName = NewType("AgentName", str)


class AgentFramework:
    def __init__(self, agent_name, **kwargs):
        self.agent_name = agent_name
        self.agent_map: Dict[AgentName, Union[Callable, tuple]] = {}
        self.play_output = True
        logger.info("AgentFramework has started")
        self.ipc = IpcSdk(**kwargs)

        self.memory_manager = MemoryManager(ipc=self.ipc)
        try:
            from global_sdk import set_framework
            set_framework(self)
        except ImportError:
            pass
        try:
            from carasdk.global_sdk import set_framework
            set_framework(self)
        except ImportError:
            pass

    async def start(self):
        # Register the request handler for action "MAIN" and category "Agent"
        await self.ipc.register_service(self.agent_name, "MAIN", "Agent")
        self.ipc.on("MAIN", self.request_handler, "Agent")
        logger.info(f"AgentFramework started: {self.agent_name}")

    async def end(self):
        await self.ipc.end()

    async def register_service(self, action: str, category: str):
        await self.ipc.register_service(self.agent_name, action, category)

    async def register_agent(
            self,
            handler: Union[Callable, object],
            prompt: str = "",
            method_name: Optional[str] = None,
            weight=1
    ) -> None:
        """
        Register a new Agent.

        :param weight:
        :param handler: Agent's handling function or object containing the method
        :param description: Description of the Agent
        :param method_name: Method name if handler is an object
        """
        if inspect.ismethod(handler) or inspect.isfunction(handler):
            function = handler
            function_name = handler.__name__
            self.agent_map[function_name] = handler
        elif isinstance(handler, object) and method_name:
            function = getattr(handler, method_name)
            function_name = method_name
            self.agent_map[function_name] = (handler, method_name)
        else:
            raise ValueError(
                "Invalid handler type or missing method_name for object handler")

        # input_spec = self._get_input_spec(function)
        # output_spec = self._get_output_spec(function)

        agent_info: AgentInfo = {
            "type": "register_agent",
            "name": function_name,
            "data": {
                "instance_id": get_instance_id(),
                "description": prompt,
                "weight": weight,
            }
        }
        await self._change_data(agent_info)

    async def _change_data(self, agent_info: AgentInfo) -> None:
        """
        Update Agent data.

        :param agent_info: Agent information
        """
        try:
            await self.ipc.send_request(
                instance_id="org.humanify.agents-manager",
                action="MAIN",
                category="Agent",
                data=json.dumps(agent_info).encode()
            )
            logger.info(f"Tool {agent_info['name']} has been updated")
        except Exception as e:
            logger.error(
                f"Error occurred while updating tool {agent_info['name']}: {str(e)}")

    async def remove_agent(self, name: str) -> None:
        """
        Remove an Agent.

        :param name: Name of the Agent to be removed
        """
        agent_info: AgentInfo = {
            "type": "remove_agent",
            "name": name,
            "data": None
        }
        self.agent_map.pop(name, None)
        await self._change_data(agent_info)

    def get_play_output(self):
        return self.play_output

    async def request_handler(self, data: bytes) -> Any:
        """
        Handle received requests.

        :param data: Received request data
        :return: Processing result
        """
        try:
            res = json.loads(data.decode('utf-8'))
            _type = res.get("type")
            function_name = res.get("name")
            input_data = res.get("data")
            self.play_output = res.get("play_output", True)
            logger.info(
                f"Request type: {_type}: {function_name}: {input_data}")

            if _type == "register_agent":
                handler = self.agent_map.get("register_agent")
                response = handler(name=function_name, **input_data)
                logger.info(f"{function_name} Agent registered: {response}")
                return response
            else:
                logger.info(f"{function_name} Agent received request: {res}")
                logger.info(
                    f"{function_name} Agent received input: {input_data}")
                handler = self.agent_map.get(function_name)
                if not handler:
                    logger.error(f"self.agent_map: {self.agent_map}")
                    raise ValueError(f"Unknown Agent: {function_name}")

                logger.info(f"{handler}")
                if isinstance(handler, tuple):
                    obj, method_name = handler
                    response = await getattr(obj, method_name)()
                else:
                    response = await handler()

                logger.info(f"{function_name} Agent returned: {response}")
                return json.dumps(response).encode()
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error(f"Error occurred while processing request: {str(e)}")
            return "Agent error, please try again later".encode()

    async def output_str_chunk(self, message_id: str, chunk: str, print_output=False, play_output=True):
        """
        Output voice string to output service.
        """
        if print_output:
            logger.info(chunk)
        self.emit_create_ai_message_signal()
        await self.add_ai_message(message_id, chunk)
        if play_output:
            try:
                await self.ipc.send_request(
                    instance_id="org.humanify.output-service",
                    action="MAIN",
                    category="OutputAudioDataChunk",
                    data=json.dumps({
                        "chunk": chunk
                    }).encode()
                )
            except Exception as e:
                logger.error(f"Error sending output chunk: {str(e)}")

    def emit_create_ai_message_signal(self):
        if self.need_emit_create_ai_message_signal:
            logger.info("Emit create ai message signal")
            self.need_emit_create_ai_message_signal = False
            try:
                asyncio.create_task(self.ipc.emit_event(
                    event_name="Agent",
                    category="CreateAiMessage"
                ))
            except Exception as e:
                logger.error(f"Error emitting create ai message signal: {str(e)}")

    async def request_agent(self, instance_id, agent_name: str, play_output: bool):
        result = await self.ipc.send_request(
            instance_id=instance_id,
            action="MAIN",
            category="Agent",
            data=json.dumps({
                "type": "request",
                "name": agent_name,
                "play_output": play_output
            }).encode(),
        )
        return result

    @staticmethod
    def _get_input_spec(func: Callable) -> dict:
        hints = get_type_hints(func)
        params = inspect.signature(func).parameters
        properties = {}
        required = []

        for name, param in params.items():
            if name != 'return' and name != 'self':
                type_hint = hints.get(name, Any)
                properties[name] = {"type": getattr(
                    type_hint, '__name__', str(type_hint))}
                if param.default == inspect.Parameter.empty:
                    required.append(name)

        return {
            "type": "object",
            "properties": properties,
            "required": required
        }

    @staticmethod
    def _get_output_spec(func: Callable) -> dict:
        hints = get_type_hints(func)
        return_type = hints.get('return', Any)
        return {
            "type": "object",
            "properties": {
                "result": {"type": getattr(return_type, '__name__', str(return_type))}
            }
        }

    async def add_ai_message(self, message_id, chunk: str):
        await self.ipc.send_request(
            instance_id="org.humanify.store",
            action="Store",
            category="AddAiMessage",
            data=json.dumps({
                "message_id": message_id,
                "agent_name": self.agent_name,
                "chunk": chunk,
            }).encode(),
        )

    async def add_human_message(self, message_id, chunk: str):
        await self.ipc.send_request(
            instance_id="org.humanify.store",
            action="MAIN",
            category="Store",
            data=json.dumps({
                "type": "add_human_message",
                "message_id": message_id,
                "chunk": chunk,
            }).encode(),
        )

    def create_new_message_id(self):
        self.need_emit_create_ai_message_signal = True
        return str(uuid.uuid4())

    async def get_agent_list(self) -> list:
        result = await self.ipc.send_request(
            instance_id="org.humanify.agents-manager",
            action="MAIN",
            category="Agent",
            data=json.dumps({
                "name": "get_list",
                "data": {}
            }).encode(),
            response_timeout=10
        )
        return json.loads(result)

    async def chat_with_memory(
            self,
            agent_prompt: str,
            output_prompt: Optional[str],
            keywords: list = [],
            remaining_loops: int = 3,
            process_handle: Optional[Callable] = None,
            json_paths: List[str] = [],
            ignore_history: bool = False
    ):
        def generate_prompt(agent_prompt: str, output_prompt: Optional[str], history: list, environment: dict, memory: dict):
            if remaining_loops > 0:
                return get_prompt_with_ltm(history, environment, memory, agent_prompt, output_prompt)
            else:
                return get_prompt(history, environment, memory, agent_prompt, output_prompt)

        if not ignore_history:
            history = await self.memory_manager.get_history()
        else:
            history = []
        environment = await self.memory_manager.get_stm_info()
        memory = await self.memory_manager.get_ltm_info(keywords)

        logger.warning(f"Memory: {memory}")
        logger.warning(f"History: {history}")
        logger.warning(f"Environment: {environment}")

        prompt = generate_prompt(
            agent_prompt, output_prompt, history, environment, memory)

        logger.warning(f"Prompt: {prompt}")

        message_id = self.create_new_message_id()

        llm = ChatOpenAI(
            api_key="EMPTY",
            base_url="http://localhost:10001/v1",
            model="Qwen/Qwen2.5-32B-Instruct-GPTQ-Int8"
        )
        # llm = ChatOpenAI(
        #     api_key="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",
        #     base_url="https://api.openai.com/v1",
        #     model="gpt-4o-mini"
        # )

        chain = llm | JsonOutputParser()
        stream_generator = chain.astream(prompt)

        # Define the chunk processing function
        async def chunk_process_handle(field_name, increment, full_value):
            logger.debug(
                f"Chunk process handle: {field_name}, {increment}, {full_value}")
            if field_name == "output":
                # Output the increment
                await self.output_str_chunk(
                    message_id,
                    increment,
                    print_output=True,
                    play_output=True
                )
            elif process_handle:
                await process_handle(field_name, increment, full_value)

        final_json, first_chunk_time, total_time = await run_langchain_with_output(
            stream_generator,
            json_paths=json_paths,
            chunk_process_handle=chunk_process_handle
        )

        logger.warning(
            f"\nTime to first chunk: {first_chunk_time:.4f} seconds")
        logger.warning(f"Total time: {total_time:.4f} seconds")

        if 'keywords' in final_json and remaining_loops > 0:
            return await self.chat_with_memory(agent_prompt, output_prompt, final_json['keywords'], remaining_loops - 1)
        else:
            return final_json
