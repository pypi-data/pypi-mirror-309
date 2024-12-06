from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("roxbot")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0+unknown"


from .node import Node  # noqa F401

# Define the logging format
LOG_FORMAT = "%(asctime)s.%(msecs)03d [%(name)s] %(filename)s:%(lineno)d - %(message)s"
