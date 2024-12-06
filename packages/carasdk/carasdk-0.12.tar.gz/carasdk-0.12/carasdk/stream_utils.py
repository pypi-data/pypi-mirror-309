import asyncio
import json
import logging
import time
from typing import Dict, Any, Optional, Tuple, Union, List, Callable, Awaitable

import jsonpath_ng
from langchain_core.output_parsers import JsonOutputParser
from carasdk.log_config import setup_logger

logger = setup_logger('StreamUtils')
# logger.setLevel(logging.DEBUG)


class IncrementalFieldTrackingJsonParser:
    def __init__(self, json_paths: List[str]):
        # Parse each path into a jsonpath_ng expression
        self.json_paths = [jsonpath_ng.parse(path) for path in json_paths]
        self.current_json: Dict[str, Any] = {}
        self.previous_values: Dict[str, Any] = {}  # Change to Any type to support lists
        self.buffer: str = ""

    def parse(self, chunk: Union[str, Dict[str, Any]]) -> Tuple[
        Optional[List[Tuple[str, Any, Any]]], Optional[Dict[str, Any]]]:
        if isinstance(chunk, dict):
            self.current_json = chunk
        else:
            self.buffer += chunk
            try:
                self.current_json = json.loads(self.buffer)
                self.buffer = ""  # Clear buffer
            except json.JSONDecodeError:
                # JSON is incomplete, continue accumulating
                return None, None

        updates = []
        for json_path in self.json_paths:
            matches = json_path.find(self.current_json)
            for match in matches:
                full_path = str(match.full_path)
                new_value = match.value
                previous_value = self.previous_values.get(full_path)
                if new_value != previous_value:
                    if isinstance(new_value, list):
                        # Handle list increments
                        increment = self.get_list_increment(previous_value or [], new_value)
                        if increment:
                            updates.append((full_path, increment, new_value))
                    else:
                        increment = self.get_increment(str(previous_value or ""), str(new_value))
                        updates.append((full_path, increment, new_value))
                    self.previous_values[full_path] = new_value

        return updates if updates else None, self.current_json

    def get_increment(self, old: str, new: str) -> str:
        if not old:
            return new
        for i, (old_char, new_char) in enumerate(zip(old, new)):
            if old_char != new_char:
                return new[i:]
        return new[len(old):]

    def get_list_increment(self, old: List[Any], new: List[Any]) -> List[Any]:
        # Assume new elements are added to the end of the list
        old_length = len(old)
        new_items = new[old_length:]
        return new_items


async def process_json_stream(stream_generator, json_paths: List[str], queue: asyncio.Queue, start_time: float):
    parser = IncrementalFieldTrackingJsonParser(json_paths)
    final_json = None
    first_chunk_received = False

    try:
        async for chunk in stream_generator:
            # logger.info(f"chunk: {chunk}")
            current_time = time.time()
            if not first_chunk_received:
                first_chunk_time = current_time - start_time
                first_chunk_received = True
                await queue.put(("first_chunk_time", first_chunk_time))

            updates, current_json = parser.parse(chunk)
            if updates:
                for update in updates:
                    await queue.put(("update", update))
            if current_json is not None:
                final_json = current_json
    finally:
        # Send total time regardless of whether an exception occurred
        total_time = time.time() - start_time
        await queue.put(("total_time", total_time))

        # Send final JSON result
        if final_json is not None:
            await queue.put(("final", final_json))

    return final_json


async def run_langchain_with_output(
        stream_generator,
        json_paths: List[str] = [],
        chunk_process_handle: Optional[Callable[[str, Any, Any], Union[Awaitable[None], None]]] = None,
):
    json_paths = json_paths.copy()
    json_paths.insert(0, "output")
    queue = asyncio.Queue()
    start_time = time.time()
    processing_task = asyncio.create_task(
        process_json_stream(stream_generator, json_paths, queue, start_time)
    )

    first_chunk_time = None
    total_time = None
    final_result = None

    try:
        while True:
            try:
                msg_type, content = await asyncio.wait_for(queue.get(), timeout=1.0)
                if msg_type == "update":
                    path, increment, full_value = content
                    # Process output field increments
                    if path == "output":
                        logger.debug(f"Output increment: {increment}")
                        if chunk_process_handle:
                            await chunk_process_handle(path, increment, full_value)
                    else:
                        logger.debug(f"Other field increment: {path}, {increment}, {full_value}")
                        if chunk_process_handle:
                            await chunk_process_handle(path, increment, full_value)
                elif msg_type == "first_chunk_time":
                    first_chunk_time = content
                    logger.info(f"First chunk time: {first_chunk_time:.4f} seconds")
                elif msg_type == "total_time":
                    total_time = content
                elif msg_type == "final":
                    final_result = content
                    break
            except asyncio.TimeoutError:
                if processing_task.done():
                    break
    finally:
        if total_time is None:
            total_time = time.time() - start_time

    await processing_task

    logger.info(f"final_result: {final_result}")
    logger.info(f"Total time: {total_time:.4f} seconds")

    return final_result, first_chunk_time, total_time


# Example usage
async def demo():
    from langchain_openai import ChatOpenAI

    # Define available agents and their parameters
    agents = {
        "Search Agent": {"description": "Used for web search and information retrieval"},
        "Calculation Agent": {"description": "Performing mathematical calculations and data analysis"},
        "Translation Agent": {"description": "Providing multi-language translation services"},
        "Weather Agent": {"description": "Providing weather forecasts and meteorological information"},
        "Schedule Agent": {"description": "Managing schedules and reminders"}
    }

    # Extract agent names
    agent_names = list(agents.keys())

    # Simulated conversation history
    conversation_history = [
        {"role": "user", "content": "Hello, I'm a new user."},
        {"role": "assistant", "content": "Hello! Welcome to our service. I'm Cara. How can I assist you today?"},
        {"role": "user", "content": "I want to know the weather in Beijing tomorrow."},
        {"role": "assistant", "content": "Sure, I can help you check the weather in Beijing tomorrow. I'll use the weather agent to get this information."},
        {"role": "user", "content": "Thank you, and then I want to arrange a meeting next week."}
    ]

    prompt = f"""
        You are a helpful assistant named Cara. You receive messages that are transcribed from audio, so you can hear them.
        Based on the following conversation history and available agents, please analyze the message and answer the following questions:
        1. Is the message understandable and relevant?
        2. Can the available agents solve the user's problem?

        Respond with a JSON object in the following structure:
        Note: "output" and "solve_agent" cannot appear in the same response!
        {{
            "output": string,
            "main_agent": string,
            "other_agent": string[],
        }}

        When responding, first focus on the most recent message. Unless the last sentence is directly related to the previous ones, do not emphasize the history background.

        - "output": If the question can be solved directly without using a proxy, answer directly. For questions that require a proxy, use the proxy without providing a direct answer. If the message is noise or cannot be understood, use this field to output a relevant response.
        - "main_agent": If a proxy is needed, provide the name of the proxy that can solve the problem.
        - "other_agent": If multiple agents can solve the problem, provide the names of agents other than main_agent.

        Respond naturally and flexibly, avoiding overly mechanical responses.

        Available agents and their parameters:
        {agents}

        Agent names: {agent_names}

        Conversation history:
        {conversation_history}

        Please respond based on the latest user message: "{conversation_history[-1]['content']}"
    """

    llm = ChatOpenAI(
        api_key="EMPTY",
        base_url="http://localhost:8001/v1",
        model="Qwen/Qwen2.5-32B-Instruct-GPTQ-Int8"
    )

    chain = llm | JsonOutputParser()
    stream_generator = chain.astream(prompt)

    async def process_handle(field_name, increment, full_value):
        if field_name == "output":
            logger.info(f"Processing output increment: {increment}")
            # Add processing logic for output field increments here
            pass
        elif field_name == "main_agent":
            logger.info(f"Processing main_agent value: {full_value}")
            # Add processing logic for main_agent field here
            pass
        elif field_name == "other_agent":
            logger.info(f"Processing other_agent increment: {full_value}")
            # Add processing logic for other_agent field here
            pass

    logger.info("Running langchain to get output, main_agent, and other_agent...")
    final_json, first_chunk_time, total_time = await run_langchain_with_output(
        stream_generator,
        process_handle,
    )
    logger.info("Stream processing completed.")

    logger.info("\nFinal JSON returned:")
    logger.info(json.dumps(final_json, indent=2, ensure_ascii=False))
    logger.info(f"\nFirst chunk time: {first_chunk_time:.4f} seconds")
    logger.info(f"Total time: {total_time:.4f} seconds")


if __name__ == "__main__":
    logger.info("Starting main execution...")
    asyncio.run(demo())
    logger.info("Main execution finished.")
