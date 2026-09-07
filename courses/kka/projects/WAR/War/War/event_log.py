
"""
Kingdom War Simulation - Event Log
Sistem log event untuk tracking aksi kingdom.
"""

from __future__ import annotations

from typing import List, Tuple


class EventLog:
    def __init__(self, max_items=35):
        self.items: List[Tuple[str, str, str]] = []
        self.max_items = max_items

    def add(self, msg: str, kingdom: str):
        label = "Red" if kingdom == "red" else "Blue"
        self.items.insert(0, (kingdom, label, msg))
        if len(self.items) > self.max_items:
            self.items.pop()
