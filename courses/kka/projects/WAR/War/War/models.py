
"""
Kingdom War Simulation - Data Models
Data classes: Resource, Building, Unit, Kingdom.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from .config import (
    UNIT_MAX_HP, UNIT_SPEED_MIN, UNIT_SPEED_MAX,
    HOUSE_SPAWN_TIME, SMITH_MAX_TRAINEES,
    INIT_POP, BASE_MAX_HP, WANDER_CHANGE,
    TOOL_COST,
)
from .utils import rnd, dst


@dataclass
class Resource:
    x: float
    y: float
    rtype: str
    depleted: bool  = False
    respawn_timer: float = 0.0

@dataclass
class Building:
    kingdom: str
    btype: str
    x: float
    y: float
    spawn_timer: float = HOUSE_SPAWN_TIME
    trainees: int = 0
    max_trainees: int = SMITH_MAX_TRAINEES
    hp: int = 50

@dataclass
class Unit:
    kingdom: str
    x: float
    y: float
    # Role: 'gatherer' | 'builder' | 'defender'  (armed units ignore role)
    role: str = "gatherer"
    tx: float = 0.0
    ty: float = 0.0
    armed: bool = False
    hp: int = UNIT_MAX_HP
    # States: idle | wandering | moving | returning | fleeing |
    #         attacking | chasing | patrolling | defending_base |
    #         going_to_smith | training | survival
    state: str = "idle"
    target_res: Optional[Resource]  = None
    target_unit: Optional["Unit"]   = None
    target_building: Optional[Building] = None
    carry: int = 0
    carry_type: Optional[str] = None
    speed: float = 34.0
    train_timer: float = 0.0
    gather_timer: float = 0.0
    wander_angle: float = 0.0
    wander_timer: float = 0.0
    smell_type: Optional[str] = None
    # Cooldown agar tidak spam log
    help_cooldown: float = 0.0
    
    # Pathfinding Cache Attributes
    path: List[Tuple[int, int]] = field(default_factory=list)
    path_target: Optional[Tuple[float, float]] = None
    waypoint_idx: int = 0
    has_tool: bool = False
    
    # Hero Possession properties
    is_possessed: bool = False
    facing_angle: float = 0.0
    dash_cooldown: float = 2.0
    dash_timer: float = 0.0
    slash_timer: float = 0.0

    def __post_init__(self):
        self.tx = self.x
        self.ty = self.y
        self.speed = rnd(UNIT_SPEED_MIN, UNIT_SPEED_MAX)
        self.wander_angle = rnd(0, math.tau)
        self.wander_timer = rnd(0, WANDER_CHANGE)

@dataclass
class VisualEffect:
    x: float
    y: float
    type: str
    radius: float
    timer: float
    max_timer: float

@dataclass
class Job:
    job_id: int
    job_type: str  # "wood" | "iron"
    target_res: Resource
    assigned_unit: Optional[Unit] = None

class JobBoard:
    def __init__(self, kingdom_key: str):
        self.kingdom_key = kingdom_key
        self.jobs: List[Job] = []
        self._next_id = 1

    def update_jobs(self, resources: List[Resource]):
        # Keep only jobs that target active (not depleted) resources
        self.jobs = [j for j in self.jobs if not j.target_res.depleted]

        # Add new jobs for any active resource that isn't on the board yet
        existing_res_ids = {id(j.target_res) for j in self.jobs}
        for r in resources:
            if not r.depleted and id(r) not in existing_res_ids:
                self.jobs.append(Job(
                    job_id=self._next_id,
                    job_type=r.rtype,
                    target_res=r
                ))
                self._next_id += 1

    def get_assignment(self, unit: Unit, kingdom: Kingdom, units: List[Unit]) -> Optional[Job]:
        # Filter unassigned jobs
        unassigned = [j for j in self.jobs if j.assigned_unit is None]
        if not unassigned:
            return None

        # Calculate active tools count
        active_tools = sum(1 for un in units if un.kingdom == unit.kingdom and un.has_tool and un.hp > 0)
        max_tools = max(3, kingdom.houses * 2)

        eligible_jobs = []
        for j in unassigned:
            if j.job_type == "iron" and not unit.has_tool:
                # Can only take iron job if we can craft a tool
                if active_tools < max_tools and kingdom.wood >= TOOL_COST["wood"]:
                    eligible_jobs.append((j, True))
            else:
                # Wood jobs or iron jobs if we already have tool
                eligible_jobs.append((j, False))

        if not eligible_jobs:
            return None

        u_total = kingdom.u_food + kingdom.u_wood + kingdom.u_iron
        if u_total > 0:
            import random
            weights = [kingdom.u_food, kingdom.u_wood, kingdom.u_iron]
            # Avoid ValueError if all weights are 0 due to some edge case
            if sum(weights) > 0:
                chosen_type = random.choices(["food", "wood", "iron"], weights=weights, k=1)[0]
                filtered_jobs = [(j, c) for (j, c) in eligible_jobs if j.job_type == chosen_type]
                if filtered_jobs:
                    eligible_jobs = filtered_jobs

        # Pick the closest eligible job
        best_job = None
        best_dist = float("inf")
        needs_crafting_best = False

        for j, needs_crafting in eligible_jobs:
            d = dst(unit.x, unit.y, j.target_res.x, j.target_res.y)
            if d < best_dist:
                best_dist = d
                best_job = j
                needs_crafting_best = needs_crafting

        if best_job:
            if needs_crafting_best:
                kingdom.wood -= TOOL_COST["wood"]
                unit.has_tool = True
            best_job.assigned_unit = unit
            return best_job, needs_crafting_best

        return None

    def release_unit_jobs(self, unit: Unit):
        for j in self.jobs:
            if j.assigned_unit == unit:
                j.assigned_unit = None

@dataclass
class Kingdom:
    key: str
    name: str
    color: Tuple[int, int, int]
    base_x: float
    base_y: float
    u_wood: float  = 0.0
    u_iron: float  = 0.0
    u_food: float  = 0.0
    u_attack: float = 0.0
    focus: str     = "GATHER"
    # Urgency flags
    base_under_attack: bool = False
    survival_mode: bool     = False
    is_starving: bool       = False
    meal_timer: float       = 30.0
    wood: float = 0.0
    iron: float = 0.0
    food: float = 20.0
    pop: int    = INIT_POP
    armed: int  = 0
    houses: int = 0
    smiths: int = 0
    base_hp: int = BASE_MAX_HP
    job_board: JobBoard = field(default=None, init=False)

    def __post_init__(self):
        self.job_board = JobBoard(self.key)
