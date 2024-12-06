import json
from typing import Callable, get_type_hints, TypedDict, Optional, Any, Dict, NewType, Union

import asyncio
from .ipc_sdk import IpcSdk
from .log_config import setup_logger
from enum import Enum

logger = setup_logger("Memory")


class STM_INFO_TYPE(Enum):
    ENVIRONMENT_PLACE = "environment_place"
    CARA_ATTENTION = "cara_attention"
    USER_MOOD = "user_mood"
    USER_INTENTION = "user_intention"


class MemoryManager:
    def __init__(self, ipc: IpcSdk):
        self.ipc = ipc
        self.unconfirmed_text = ""
        self.unmatched_text = ""
        try:
            from global_sdk import set_memory
            set_memory(self)
        except ImportError:
            pass
        try:
            from carasdk.global_sdk import set_memory
            set_memory(self)
        except ImportError:
            pass

    async def init(self):
        await self.ipc.register_handler("Paragraph", "UnconfirmedText")
        self.ipc.on_event(
            "Paragraph", self.handle_unconfirmed_text, "UnconfirmedText")
        await self.ipc.register_handler("Paragraph", "UnmatchedText")
        self.ipc.on_event(
            "Paragraph", self.handle_unmatched_text, "UnmatchedText")

    async def handle_unconfirmed_text(self, data: bytes):
        logger.info(f"Received unconfirmed text: {data}")
        obj = json.loads(data.decode())
        self.unconfirmed_text = obj.get("context", "")

    async def handle_unmatched_text(self, data: bytes):
        logger.info(f"Received unmatched text: {data}")
        obj = json.loads(data.decode())
        self.unmatched_text = obj.get("context", "")

    async def get_stm_info(self):
        response = await self.ipc.send_request(
            instance_id="org.humanify.store",
            action="Stm",
            category="Get"
        )
        response_str = response.decode()
        stm_infos = json.loads(response_str)
        stm_dict = {}
        for stm_info in stm_infos:
            stm_dict[stm_info['type']] = stm_info['value']
        result = ""
        for type in STM_INFO_TYPE:
            if type.value in stm_dict:
                result += f"{type.name}: {stm_dict[type.value]}\n"
            else:
                result += f"{type.name}: None\n"
        return result

    async def insert_stm_info(self, type: str, value: str):
        if value is None:
            return
        type_enum = STM_INFO_TYPE[type]
        await self.ipc.send_request(
            instance_id="org.humanify.store",
            action="Stm",
            category="Insert",
            data=json.dumps({"type": type_enum.value, "value": value})
        )

    async def get_ltm_info(self, query: list[str]):
        logger.info(f"get_ltm_info Query: {query}")
        if len(query) == 0:
            return ""
        response = await self.ipc.send_request(
            instance_id="org.humanify.store",
            action="Ltm",
            category="Query",
            data=json.dumps({"query": query})
        )
        response_str = response.result.decode("utf-8")
        return response_str

    async def insert_ltm_info(self, text: str):
        await self.ipc.send_request(
            instance_id="org.humanify.store",
            action="Ltm",
            category="Insert",
            data=json.dumps({"value": text})
        )

    async def get_history(self, count: int = 40, response_timeout=10) -> Optional[list]:
        res = await self.ipc.send_request(
            # instance_id="org.humanify.mock",
            instance_id="org.humanify.store",
            action="Store",
            category="GetHistory",
            data=json.dumps({
                "count": count
            }).encode(),
            response_timeout=response_timeout
        )
        data = json.loads(res.decode())
        # logger.info(f"History: {data}")

        formatted_history = [
            {
                "user": {
                    "name": (message.get("person") or {"name": "unknown_person"}).get("name", "unknown_person"),
                    "role": (message.get("person") or {"type": "unknown_role"}).get("type", "unknown_role"),
                    "id": (message.get("person") or {"id": "unknown_person"}).get("id", "unknown_person")
                },
                "content": message.get("text", "")
            }
            for message in data
        ]

        # Add unconfirmed text at the end
        if self.unconfirmed_text and len(formatted_history) > 0:
            formatted_history.append({
                "user": {
                    "name": "unknown_person",
                    "role": "unknown_role",
                    "id": "unknown_id"
                },
                "content": self.unconfirmed_text + self.unmatched_text
            })
        return formatted_history[-5:]
        # return formatted_history


def format_history(history: list):
    # - name: role, content: text
    return "\n".join([f"- name: {message['user']['role']}, content: {message['content']}" for message in history])


async def main():
    memory_manager = MemoryManager()
    await memory_manager.init()

if __name__ == "__main__":
    asyncio.run(main())
