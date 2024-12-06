import importlib.metadata

try:
    # Try to get version from package metadata
    __version__ = importlib.metadata.version(__package__)
except importlib.metadata.PackageNotFoundError:
    # Fallback version if package metadata is not available
    __version__ = "0.1.31"

# Set API version to match package version
api_version = __version__

from mem0.memory.main import Memory

# Add api_version to Memory class
Memory.api_version = api_version

__all__ = ["Memory"]