"""CCIFA Coding World Cup — top-level package.

Re-exports the engine for convenience::

    from matchcore import MatchCore, SealEngine, SovereignLedger
"""

from matchcore.engine import __version__  # noqa: F401

__all__ = ["__version__"]
