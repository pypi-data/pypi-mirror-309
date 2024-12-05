import importlib.metadata as importlib_metadata

from .analysis import Bound
from .chain import Chain, ChainConfig
from .chainconsumer import ChainConsumer
from .color_finder import colors
from .examples import make_sample
from .plotting.config import PlotConfig
from .truth import Truth

__all__ = ["ChainConsumer", "Chain", "ChainConfig", "Truth", "PlotConfig", "make_sample", "Bound", "colors"]

__version__ = importlib_metadata.version(__name__)
