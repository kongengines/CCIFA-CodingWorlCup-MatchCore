"""Arena — sovereign offline execution nodes.

Arena nodes are physically isolated machines that execute official
matches. They have no network access during a match; the only thing
that leaves the arena is a sealed, signed record on physical media
(USB courier).
"""

from matchcore.engine.arena.arena_node import ArenaNode
from matchcore.engine.arena.offline_runtime import OfflineRuntime
from matchcore.engine.arena.physical_sync import PhysicalSync

__all__ = ["ArenaNode", "OfflineRuntime", "PhysicalSync"]
