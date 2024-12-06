import importlib.metadata

__version__ = importlib.metadata.version("mem0ai_boop_custom")

from mem0.client.main import MemoryClient, AsyncMemoryClient  # noqa
from mem0.memory.main import Memory  # noqa