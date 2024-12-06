import importlib.metadata

try:
    # Try to get version from package metadata
    __version__ = importlib.metadata.version(__package__)
except importlib.metadata.PackageNotFoundError:
    # Fallback version if package metadata is not available
    __version__ = "0.1.0"

from mem0.memory.main import Memory

__all__ = ["Memory"]