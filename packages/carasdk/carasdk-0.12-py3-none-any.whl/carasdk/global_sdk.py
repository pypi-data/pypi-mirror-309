from .agent_framework import AgentFramework
from .ipc_sdk import IpcSdk
from .memory import MemoryManager

ipc: IpcSdk = None
framework: AgentFramework = None
memory: MemoryManager = None


def get_ipc() -> IpcSdk:
    global ipc
    if ipc is None:
        raise ValueError("ipc is not initialized")
    return ipc


def set_ipc(new_ipc: IpcSdk):
    global ipc
    ipc = new_ipc


def get_framework() -> AgentFramework:
    global framework
    if framework is None:
        raise ValueError("framework is not initialized")
    return framework


def set_framework(new_framework: AgentFramework):
    global framework
    framework = new_framework


def get_memory() -> MemoryManager:
    global memory
    if memory is None:
        raise ValueError("memory is not initialized")
    return memory


def set_memory(new_memory: MemoryManager):
    global memory
    memory = new_memory
