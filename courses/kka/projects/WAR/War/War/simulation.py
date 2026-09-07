
"""
Kingdom War Simulation - Simulation Engine
Core game logic: AI, unit behavior, utility evaluation, combat.
"""

from __future__ import annotations

import math
import random
from typing import List, Optional

from .config import (
    SIM_X, SIM_Y, SIM_W, SIM_H,
    INIT_POP, INIT_RESOURCES, RESOURCE_TYPES,
    HOUSE_COST, SMITH_COST, WEAPON_COST, TOOL_COST,
    RESPAWN_TIME_MIN, RESPAWN_TIME_MAX, RESOURCE_CARRY_AMT,
    HOUSE_SPAWN_TIME, UNIT_ATTACK_DAMAGE, UNIT_TRAIN_TIME,
    SMELL_RADIUS, WANDER_SPEED, WANDER_CHANGE,
    UTILITY_HOUSE_WOOD_WEIGHT, UTILITY_SMITH_IRON_WEIGHT,
    UTILITY_FOOD_WEIGHT, MEAL_TIME_INTERVAL,
    UTILITY_ATTACK_WEIGHT, UTILITY_ATTACK_THRESHOLD,
    UTILITY_MILITARY_CAP_RATIO,
    PATROL_RADIUS, AGGRESSION_RADIUS, FLEE_RADIUS,
    BASE_DANGER_RADIUS, CRITICAL_POP_RATIO, HELP_REQUEST_RADIUS,
    BASE_MAX_HP, RED_COL, BLUE_COL,
)
from .utils import rnd, dst, clamp

class SpatialHash:
    def __init__(self, cell_size: int = 100):
        self.cell_size = cell_size
        self.cells = {}

    def clear(self):
        self.cells.clear()

    def insert(self, unit):
        cell_x = int(unit.x // self.cell_size)
        cell_y = int(unit.y // self.cell_size)
        key = (cell_x, cell_y)
        if key not in self.cells:
            self.cells[key] = []
        self.cells[key].append(unit)

    def get_nearby_units(self, x: float, y: float, radius: float):
        result = []
        min_cx = int((x - radius) // self.cell_size)
        max_cx = int((x + radius) // self.cell_size)
        min_cy = int((y - radius) // self.cell_size)
        max_cy = int((y + radius) // self.cell_size)

        for cy in range(min_cy, max_cy + 1):
            for cx in range(min_cx, max_cx + 1):
                key = (cx, cy)
                if key in self.cells:
                    result.extend(self.cells[key])
        return result

from .models import Resource, Building, Unit, Kingdom, Job, JobBoard, VisualEffect
from .pathfinding import GridMap, AStar
from .event_log import EventLog


class Simulation:
    def __init__(self):
        self.grid_map = GridMap(SIM_X, SIM_Y, SIM_W, SIM_H, cell_size=20)
        self.debug_mode = False
        self.reset()

    # ------------------------------------------------------------------
    def reset(self):
        self.grid_map = GridMap(SIM_X, SIM_Y, SIM_W, SIM_H, cell_size=20)
        self._generate_map_terrain()
        self.kingdoms = {
            "red":  Kingdom("red",  "Red Dominion",  RED_COL,
                            SIM_X + 60,           SIM_Y + SIM_H // 2),
            "blue": Kingdom("blue", "Blue Covenant", BLUE_COL,
                            SIM_X + SIM_W - 60,   SIM_Y + SIM_H // 2),
        }
        self._clear_around_bases()
        
        self.units:     List[Unit]     = []
        self.resources: List[Resource] = []
        self.buildings: List[Building] = []
        self.sim_time   = 0.0
        self.event_log  = EventLog()
        self.game_over  = False
        self.winner: Optional[str] = None
        self.spatial_hash = SpatialHash(cell_size=100)
        self.effects: List[VisualEffect] = []
        
        self.possessed_unit: Optional[Unit] = None
        self.input_state = {
            "w": False, "a": False, "s": False, "d": False,
            "mx": 0.0, "my": 0.0,
            "slash": False,
            "dash": False
        }

        self._spawn_resources()
        self._spawn_units()

    def _generate_map_terrain(self):
        gm = self.grid_map
        # 1. Place vertical River in the middle with a bridge opening
        mid_col = gm.cols // 2
        for r in range(gm.rows):
            if r not in (int(gm.rows // 2) - 1, int(gm.rows // 2), int(gm.rows // 2) + 1):
                gm.cells[r][mid_col] = 3 # River
                
        # 2. Place horizontal Walls
        for c in range(4, 8):
            gm.cells[4][c] = 1 # Wall
        for c in range(gm.cols - 8, gm.cols - 4):
            gm.cells[gm.rows - 5][c] = 1 # Wall
            
        # 3. Scatter Rocks
        gm.cells[2][2] = 2
        gm.cells[gm.rows - 3][gm.cols - 3] = 2
        gm.cells[3][gm.cols - 4] = 2
        gm.cells[gm.rows - 4][3] = 2

        # 4. Add Roads and Forests
        bridge_row = gm.rows // 2
        for c in range(gm.cols):
            if gm.cells[bridge_row][c] == 0:
                gm.cells[bridge_row][c] = 5 # Road
                
        for r in range(1, 4):
            for c in range(gm.cols // 2 - 4, gm.cols // 2 - 1):
                if gm.cells[r][c] == 0:
                    gm.cells[r][c] = 4 # Forest
        for r in range(gm.rows - 4, gm.rows - 1):
            for c in range(gm.cols // 2 + 1, gm.cols // 2 + 5):
                if gm.cells[r][c] == 0:
                    gm.cells[r][c] = 4 # Forest

    def _clear_around_bases(self):
        gm = self.grid_map
        for k in self.kingdoms.values():
            bc, br = gm.world_to_grid(k.base_x, k.base_y)
            for dc in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    cc, cr = bc + dc, br + dr
                    if 0 <= cc < gm.cols and 0 <= cr < gm.rows:
                        if gm.cells[cr][cc] in (1, 2, 3):
                            gm.cells[cr][cc] = 0

    # ------------------------------------------------------------------
    def _spawn_resources(self):
        self.resources = []
        for _ in range(INIT_RESOURCES):
            self._add_resource()

    def _get_valid_resource_pos(self) -> Tuple[float, float]:
        for _ in range(100):
            rx = rnd(SIM_X + 100, SIM_X + SIM_W - 100)
            ry = rnd(SIM_Y + 30,  SIM_Y + SIM_H - 30)
            rc, rr = self.grid_map.world_to_grid(rx, ry)
            if self.grid_map.is_walkable(rc, rr) and self.grid_map.cells[rr][rc] != 5:
                return rx, ry
        return rnd(SIM_X + 100, SIM_X + SIM_W - 100), rnd(SIM_Y + 30,  SIM_Y + SIM_H - 30)

    def _add_resource(self):
        rtype = random.choice(RESOURCE_TYPES)
        rx, ry = self._get_valid_resource_pos()
        self.resources.append(Resource(x=rx, y=ry, rtype=rtype))

    def _spawn_units(self):
        self.units = []
        roles = ["gatherer"] * 6 + ["builder"] * 2 + ["defender"] * 2  # 60/20/20
        for k in self.kingdoms.values():
            role_pool = roles[:]
            random.shuffle(role_pool)
            for i in range(INIT_POP):
                role = role_pool[i % len(role_pool)]
                # Spawn in walkable cells only
                found = False
                for _ in range(50):
                    ux = k.base_x + rnd(-20, 20)
                    uy = k.base_y + rnd(-20, 20)
                    uc, ur = self.grid_map.world_to_grid(ux, uy)
                    if self.grid_map.is_walkable(uc, ur):
                        self.units.append(Unit(
                            kingdom=k.key,
                            x=ux,
                            y=uy,
                            role=role,
                        ))
                        found = True
                        break
                if not found:
                    self.units.append(Unit(
                        kingdom=k.key,
                        x=k.base_x,
                        y=k.base_y,
                        role=role,
                    ))

    def _make_unit(self, kingdom_key: str) -> Unit:
        k = self.kingdoms[kingdom_key]
        role = random.choices(["gatherer","builder","defender"], weights=[6,2,2])[0]
        # Spawn in walkable cell
        for _ in range(50):
            ux = k.base_x + rnd(-20, 20)
            uy = k.base_y + rnd(-20, 20)
            uc, ur = self.grid_map.world_to_grid(ux, uy)
            if self.grid_map.is_walkable(uc, ur):
                return Unit(kingdom=kingdom_key, x=ux, y=uy, role=role)
        return Unit(kingdom=kingdom_key, x=k.base_x, y=k.base_y, role=role)

    # ------------------------------------------------------------------
    # UTILITY EVALUATION
    # ------------------------------------------------------------------
    def _evaluate_utilities(self):
        for kname, k in self.kingdoms.items():
            ek = self.kingdoms["blue" if kname == "red" else "red"]

            # Update job board
            k.job_board.update_jobs(self.resources)

            # --- Urgency flags dulu ---
            # Base under attack: ada armed enemy dalam BASE_DANGER_RADIUS
            enemies_near_base = [
                u for u in self.units
                if u.kingdom != kname and u.armed and u.hp > 0
                and dst(u.x, u.y, k.base_x, k.base_y) <= BASE_DANGER_RADIUS
            ]
            was_under_attack = k.base_under_attack
            k.base_under_attack = len(enemies_near_base) > 0
            if k.base_under_attack and not was_under_attack:
                self.event_log.add("⚠ BASE UNDER ATTACK!", kname)

            # Survival mode: populasi <= CRITICAL_POP_RATIO dari awal
            was_survival = k.survival_mode
            k.survival_mode = k.pop <= int(INIT_POP * CRITICAL_POP_RATIO)
            if k.survival_mode and not was_survival:
                self.event_log.add("☠ SURVIVAL MODE", kname)

            # --- Utility scores ---
            pop_cap      = max(10, k.houses * 5 + 10)
            pop_pressure = k.pop / pop_cap
            k.u_wood = max(10.0, pop_pressure * 100 * UTILITY_HOUSE_WOOD_WEIGHT)

            ideal_armed       = int(k.pop * UTILITY_MILITARY_CAP_RATIO)
            military_pressure = 1.0 - (k.armed / max(1, ideal_armed)) if k.armed < ideal_armed else 0.0
            k.u_iron = max(10.0, military_pressure * 100 * UTILITY_SMITH_IRON_WEIGHT)

            k.u_attack = max(0.0, ((k.armed - ek.armed) * 10 + k.armed * 5) * UTILITY_ATTACK_WEIGHT)

            # Override focus saat kritis
            if k.survival_mode:
                k.focus = "SURVIVE"
            elif k.base_under_attack:
                k.focus = "DEFEND"
            else:
                scores     = {"FOOD": k.u_food, "WOOD": k.u_wood, "IRON": k.u_iron, "ATTACK": k.u_attack}
                new_focus  = max(scores, key=scores.get)
                if new_focus != k.focus:
                    if new_focus == "ATTACK" and k.u_attack >= UTILITY_ATTACK_THRESHOLD:
                        self.event_log.add("Focus: ASSAULT", kname)
                        k.focus = new_focus
                    elif new_focus != "ATTACK":
                        self.event_log.add(f"Focus: {new_focus}", kname)
                        k.focus = new_focus

    # ------------------------------------------------------------------
    # MAIN UPDATE
    # ------------------------------------------------------------------
    def update(self, dt: float):
        if self.game_over:
            return

        # Perbarui Posisi di Spatial Hash
        self.spatial_hash.clear()
        for u in self.units:
            if u.hp > 0:
                self.spatial_hash.insert(u)

        for k in self.kingdoms.values():
            # Meal Time Mechanic
            k.meal_timer -= dt
            if k.meal_timer <= 0:
                k.meal_timer = MEAL_TIME_INTERVAL
                if k.food >= k.pop:
                    k.food -= k.pop
                    k.is_starving = False
                else:
                    k.food = 0
                    k.is_starving = True
                    self.event_log.add(f"{k.name} didn't have enough food for Meal Time!", k.key)
                    self.event_log.add(f"Population is STARVING!", k.key)

            # Food utility: High if food is low compared to 2 upcoming meals
            safe_food_level = k.pop * 2.0
            if k.food < safe_food_level:
                k.u_food = ((safe_food_level - k.food) / safe_food_level) * 100.0 * UTILITY_FOOD_WEIGHT
            else:
                k.u_food = 0.0

        self.sim_time += dt

        # Hero Logic
        if self.possessed_unit:
            if self.possessed_unit.hp <= 0:
                self.possessed_unit.is_possessed = False
                self.possessed_unit = None
                self.event_log.add("The Hero has fallen!", "red")
            else:
                self._tick_hero(self.possessed_unit, dt)

        self._evaluate_utilities()

        # Update visual effects
        for eff in self.effects:
            eff.timer -= dt
        self.effects = [eff for eff in self.effects if eff.timer > 0]

        # Resource respawn
        for res in self.resources:
            if res.depleted:
                res.respawn_timer -= dt
                if res.respawn_timer <= 0:
                    res.depleted = False
                    res.x, res.y = self._get_valid_resource_pos()

        # House spawn
        for b in self.buildings:
            if b.btype == "house":
                b.spawn_timer -= dt
                if b.spawn_timer <= 0:
                    k = self.kingdoms[b.kingdom]
                    k.pop += 1
                    self.units.append(self._make_unit(b.kingdom))
                    b.spawn_timer = HOUSE_SPAWN_TIME

        # Unit cooldowns
        for u in self.units:
            if u.help_cooldown > 0:
                u.help_cooldown -= dt
            if getattr(u, 'attack_cooldown', 0) > 0:
                u.attack_cooldown -= dt

        # Unit AI
        for u in self.units:
            if u.hp <= 0:
                k = self.kingdoms[u.kingdom]
                k.job_board.release_unit_jobs(u)
                if u.target_building and u.target_building.btype == "smith" and u.state in ("going_to_smith", "training"):
                    u.target_building.trainees = max(0, u.target_building.trainees - 1)
                    u.target_building = None
                continue
            self._tick_unit(u, dt)

        # Boids Separation (Collision Avoidance)
        for u in self.units:
            if u.hp > 0:
                neighbors = self.spatial_hash.get_nearby_units(u.x, u.y, 12.0)
                for n in neighbors:
                    if u != n and n.hp > 0:
                        d = dst(u.x, u.y, n.x, n.y)
                        if 0 < d < 12.0:
                            overlap = 12.0 - d
                            dx = (u.x - n.x) / d
                            dy = (u.y - n.y) / d
                            push_str = overlap * 2.0 * dt
                            
                            nx = u.x + dx * push_str
                            ny = u.y + dy * push_str
                            
                            nc, nr = self.grid_map.world_to_grid(nx, ny)
                            if self.grid_map.is_walkable(nc, nr):
                                u.x = nx
                                u.y = ny

        # Win check — hitung dari unit hidup
        r_alive, r_armed = 0, 0
        b_alive, b_armed = 0, 0
        
        for u in self.units:
            if u.hp > 0:
                if u.kingdom == "red":
                    r_alive += 1
                    if u.armed: r_armed += 1
                elif u.kingdom == "blue":
                    b_alive += 1
                    if u.armed: b_armed += 1
                    
        self.kingdoms["red"].pop    = r_alive
        self.kingdoms["red"].armed  = r_armed
        self.kingdoms["blue"].pop   = b_alive
        self.kingdoms["blue"].armed = b_armed

        # Cleanup Mayat & Bangunan Hancur
        self.units = [u for u in self.units if u.hp > 0]
        
        surviving_buildings = []
        for b in self.buildings:
            if b.hp > 0:
                surviving_buildings.append(b)
            else:
                k = self.kingdoms[b.kingdom]
                if b.btype == "house":
                    k.houses = max(0, k.houses - 1)
                elif b.btype == "smith":
                    k.smiths = max(0, k.smiths - 1)
        self.buildings = surviving_buildings

        if r_alive <= 0:
            self._end_game("Blue Covenant")
        elif b_alive <= 0:
            self._end_game("Red Dominion")

    def apply_god_power(self, power: str, wx: float, wy: float):
        if self.game_over: return
        
        gm = self.grid_map
        if power in ("water", "mountain", "forest", "grass"):
            c, r = gm.world_to_grid(wx, wy)
            if 0 <= c < gm.cols and 0 <= r < gm.rows:
                brush_radius = 2  # 2 cells radius
                terrain_changed = False
                for dr in range(-brush_radius, brush_radius + 1):
                    for dc in range(-brush_radius, brush_radius + 1):
                        if dr*dr + dc*dc <= brush_radius*brush_radius:
                            rr = r + dr
                            cc = c + dc
                            if 0 <= rr < gm.rows and 0 <= cc < gm.cols:
                                val = 0
                                if power == "water": val = 3
                                elif power == "mountain": val = 1
                                elif power == "forest": val = 4
                                elif power == "grass": val = 0
                                
                                # Protect base areas from being overwritten with impassable terrain
                                is_near_base = False
                                for k in self.kingdoms.values():
                                    bc, br = gm.world_to_grid(k.base_x, k.base_y)
                                    if abs(rr - br) <= 3 and abs(cc - bc) <= 3:
                                        is_near_base = True
                                        
                                if is_near_base and val in (1, 3):
                                    continue # Jangan taruh wall/water di base
                                    
                                if gm.cells[rr][cc] != val:
                                    gm.cells[rr][cc] = val
                                    terrain_changed = True
                
                if terrain_changed:
                    # Invalidate pathfinding cache
                    for u in self.units:
                        u.path = []
                        u.waypoint_idx = 0
                        u.path_target_cell = None
                        
        elif power == "bomb":
            self.effects.append(VisualEffect(wx, wy, "explosion", 60.0, 1.0, 1.0))
            self.event_log.add("God dropped a Bomb!", "red")  # Hack to color red
            # Damage units
            for u in self.units:
                if u.hp > 0 and dst(u.x, u.y, wx, wy) <= 60.0:
                    u.hp -= 100
                    if u.hp <= 0:
                        self.event_log.add("Unit obliterated by Bomb!", u.kingdom)
            # Damage buildings
            for b in self.buildings:
                if b.hp > 0 and dst(b.x, b.y, wx, wy) <= 60.0:
                    b.hp -= 50

        elif power == "lightning":
            self.effects.append(VisualEffect(wx, wy, "lightning", 20.0, 0.5, 0.5))
            self.event_log.add("God struck Lightning!", "blue")
            for u in self.units:
                if u.hp > 0 and dst(u.x, u.y, wx, wy) <= 20.0:
                    u.hp -= 200
                    if u.hp <= 0:
                        self.event_log.add("Unit smote by Lightning!", u.kingdom)

        elif power == "spawn_red":
            self.units.append(Unit(kingdom="red", x=wx, y=wy, role="gatherer", armed=False))
            self.kingdoms["red"].pop += 1
            self.event_log.add("God spawned a Red worker", "red")
            
        elif power == "spawn_blue":
            self.units.append(Unit(kingdom="blue", x=wx, y=wy, role="gatherer", armed=False))
            self.kingdoms["blue"].pop += 1
            self.event_log.add("God spawned a Blue worker", "blue")

        elif power == "possess":
            if self.possessed_unit:
                self.possessed_unit.is_possessed = False
                self.possessed_unit = None
                
            best_u = None
            min_d = 40.0
            for u in self.units:
                if u.hp > 0:
                    d = dst(u.x, u.y, wx, wy)
                    if d < min_d:
                        min_d = d
                        best_u = u
                        
            if best_u:
                best_u.is_possessed = True
                self.possessed_unit = best_u
                self.event_log.add("God possessed a unit!", best_u.kingdom)

    # ------------------------------------------------------------------
    # UNIT TICK
    # ------------------------------------------------------------------
    def _tick_unit(self, u: Unit, dt: float):
        if u.is_possessed:
            return

        if u.hp <= 0: return
        k  = self.kingdoms[u.kingdom]
        ek = self.kingdoms["blue" if u.kingdom == "red" else "red"]
        bx, by = k.base_x, k.base_y

        # ----------------------------------------------------------------
        # TRAINING (di blacksmith)
        # ----------------------------------------------------------------
        if u.state == "training":
            u.train_timer -= dt
            if u.train_timer <= 0:
                u.armed  = True
                u.speed += 5
                u.state  = "idle"
                if u.target_building:
                    u.target_building.trainees -= 1
                    u.target_building = None
                self.event_log.add("Warrior ready!", u.kingdom)
            return

        # ----------------------------------------------------------------
        # SURVIVAL MODE — semua unit (armed atau tidak) kumpul di base
        # ----------------------------------------------------------------
        if k.survival_mode and u.state not in ("training", "going_to_smith"):
            if u.state not in ("survival",):
                u.state    = "survival"
                u.tx       = bx + rnd(-30, 30)
                u.ty       = by + rnd(-30, 30)
                u.carry    = 0
                u.carry_type = None
                u.target_res = None
                k.job_board.release_unit_jobs(u)
            self._move_toward_target(u, dt)
            if dst(u.x, u.y, u.tx, u.ty) < 6:
                # Sudah di base, patroli kecil
                u.tx = bx + rnd(-35, 35)
                u.ty = by + rnd(-35, 35)
            return

        # ----------------------------------------------------------------
        # BASE UNDER ATTACK — soldier override ke defend_base
        # ----------------------------------------------------------------
        if k.base_under_attack and u.armed:
            if u.state not in ("defending_base", "training"):
                dist_to_home = dst(u.x, u.y, bx, by)
                # Boleh bertarung di jalan HANYA JIKA musuhnya bersenjata (pencegat), atau sudah dekat markas
                is_chasing_armed = (u.state == "chasing" and getattr(u, 'target_unit', None) and u.target_unit.armed)
                is_near_home = (dist_to_home <= BASE_DANGER_RADIUS + 40)
                
                if u.state == "chasing" and (is_chasing_armed or is_near_home):
                    pass
                else:
                    u.state = "defending_base"
                    u.target_unit = None
                    u.tx    = bx + rnd(-40, 40)
                    u.ty    = by + rnd(-40, 40)

        # ----------------------------------------------------------------
        # CALL TO ARMS (Militia): Pekerja panik membuang alat dan membela markas
        # ----------------------------------------------------------------
        if k.base_under_attack and not u.armed:
            if u.state not in ("defending_base", "training", "going_to_smith", "chasing", "fleeing", "survival"):
                u.carry = 0
                u.carry_type = None
                u.target_res = None
                k.job_board.release_unit_jobs(u)
                u.state = "defending_base"
                u.tx = bx + rnd(-40, 40)
                u.ty = by + rnd(-40, 40)

        # ----------------------------------------------------------------
        # PASSIVE THREAT CHECK: worker flee kalau ada armed enemy dekat
        # ----------------------------------------------------------------
        if not u.armed and u.state not in ("fleeing", "training", "going_to_smith", "survival", "defending_base", "chasing"):
            threat = self._nearest_armed_enemy(u)
            if threat and dst(u.x, u.y, threat.x, threat.y) <= FLEE_RADIUS:
                # Drop resource, lari ke base
                u.carry      = 0
                u.carry_type = None
                u.target_res = None
                u.state      = "fleeing"
                u.tx         = bx + rnd(-20, 20)
                u.ty         = by + rnd(-20, 20)
                k.job_board.release_unit_jobs(u)
                # Minta bantuan soldier terdekat (cooldown 5s)
                if u.help_cooldown <= 0:
                    self._call_for_help(u, threat)
                    u.help_cooldown = 5.0

        # ----------------------------------------------------------------
        # SOLDIER PATROL & MILITIA — cek musuh di PATROL_RADIUS
        # ----------------------------------------------------------------
        is_militia = (not u.armed and u.state == "defending_base")
        if (u.armed or is_militia) and u.state in ("idle", "patrolling", "defending_base"):
            enemy_in_range = self._nearest_enemy_in_radius(u, PATROL_RADIUS)
            
            if enemy_in_range:
                dist_to_home = dst(u.x, u.y, bx, by)
                # Jika sedang lari pulang tapi masih jauh, hiraukan pekerja biasa (fokus ke markas atau prajurit saja)
                if k.base_under_attack and u.state == "defending_base" and dist_to_home > BASE_DANGER_RADIUS + 40:
                    if not enemy_in_range.armed:
                        enemy_in_range = None
                        
            if enemy_in_range:
                u.target_unit = enemy_in_range
                u.state       = "chasing"

        # ----------------------------------------------------------------
        # IDLE DECISION
        # ----------------------------------------------------------------
        if u.state == "idle":
            self._idle_decision(u, k, ek, bx, by)

        # ----------------------------------------------------------------
        # WANDERING
        # ----------------------------------------------------------------
        elif u.state == "wandering":
            self._tick_wander(u, dt)

        # ----------------------------------------------------------------
        # FLEEING — sampai base, idle lagi
        # ----------------------------------------------------------------
        elif u.state == "fleeing":
            self._move_toward_target(u, dt)
            if dst(u.x, u.y, u.tx, u.ty) < 6:
                u.state = "idle"

        # ----------------------------------------------------------------
        # CHASING — soldier kejar target sampai mati
        # ----------------------------------------------------------------
        elif u.state == "chasing":
            t = u.target_unit
            if not t or t.hp <= 0:
                u.target_unit = None
                u.state       = "idle"
            else:
                u.tx = t.x
                u.ty = t.y
                self._move_toward_target(u, dt)
                if dst(u.x, u.y, t.x, t.y) < 8:
                    if getattr(u, 'attack_cooldown', 0) <= 0:
                        damage = UNIT_ATTACK_DAMAGE if u.armed else UNIT_ATTACK_DAMAGE * 0.25
                        t.hp -= damage
                        u.attack_cooldown = 0.5  # Serang setiap 0.5 detik
                        
                        if t.hp <= 0:
                            self.event_log.add("Enemy killed!", u.kingdom)
                            u.target_unit = None
                            u.state       = "idle"

        # ----------------------------------------------------------------
        # DEFENDING BASE — soldier jaga base, kejar enemy yang mendekat
        # ----------------------------------------------------------------
        elif u.state == "defending_base":
            if not k.base_under_attack:
                u.state = "idle"
                return
            # Cari enemy terdekat di sekitar base
            threat = self._nearest_armed_enemy(u)
            if threat and dst(threat.x, threat.y, bx, by) <= BASE_DANGER_RADIUS + 30:
                if u.armed:
                    u.target_unit = threat
                    u.state       = "chasing"
                else:
                    # Unarmed defender -> call for help occasionally
                    if getattr(u, 'help_cooldown', 0) <= 0:
                        self._call_for_help(u, threat)
                        u.help_cooldown = 2.0
                    else:
                        u.help_cooldown -= dt
                    
                    self._move_toward_target(u, dt)
                    if dst(u.x, u.y, u.tx, u.ty) < 6:
                        u.tx = bx + rnd(-30, 30)
                        u.ty = by + rnd(-30, 30)
            else:
                self._move_toward_target(u, dt)
                if dst(u.x, u.y, u.tx, u.ty) < 6:
                    u.tx = bx + rnd(-40, 40)
                    u.ty = by + rnd(-40, 40)

        # ----------------------------------------------------------------
        # STARVATION DAMAGE (Applies to all states)
        # ----------------------------------------------------------------
        if k.is_starving:
            u.hp -= 0.05 * dt
            if u.hp <= 0:
                if not getattr(u, 'starved', False):
                    u.starved = True
                    self.event_log.add("Unit starved to death!", u.kingdom)
                return  # Hentikan semua aktivitas jika sudah mati!

        # ----------------------------------------------------------------
        # GATHERING DELAY
        # ----------------------------------------------------------------
        if u.state == "gathering":
            u.gather_timer -= dt
            if u.gather_timer <= 0:
                if u.target_res and not u.target_res.depleted:
                    u.target_res.depleted      = True
                    u.target_res.respawn_timer = rnd(RESPAWN_TIME_MIN, RESPAWN_TIME_MAX)
                    u.carry_type               = u.target_res.rtype
                    u.carry                    = RESOURCE_CARRY_AMT
                    k.job_board.release_unit_jobs(u)
                    u.target_res               = None
                    u.state = "returning"
                    u.tx    = bx + rnd(-25, 25)
                    u.ty    = by + rnd(-25, 25)
                else:
                    u.target_res = None
                    k.job_board.release_unit_jobs(u)
                    self._start_wander(u, k)
            return

        # ----------------------------------------------------------------
        # MOVING / RETURNING / ATTACKING / GOING_TO_SMITH / PATROLLING
        # ----------------------------------------------------------------
        elif u.state in ("moving", "returning", "attacking", "going_to_smith", "patrolling"):
            # Update target position kalau attacking
            if u.state == "attacking":
                if u.target_unit:
                    if u.target_unit.hp > 0:
                        u.tx = u.target_unit.x
                        u.ty = u.target_unit.y
                    else:
                        u.state       = "idle"
                        u.target_unit = None
                        return
                elif getattr(u, 'target_building', None):
                    if u.target_building.hp > 0:
                        u.tx = u.target_building.x
                        u.ty = u.target_building.y
                    else:
                        u.state = "idle"
                        u.target_building = None
                        return

            speed_mult = 1.0
            if k.is_starving:
                speed_mult = 0.7

            self._move_toward_target(u, dt, speed_mult=speed_mult)
            d = dst(u.x, u.y, u.tx, u.ty)

            if d < 6:
                self._arrive(u, k, bx, by)

    # ------------------------------------------------------------------
    def _idle_decision(self, u: Unit, k: Kingdom, ek: Kingdom, bx: float, by: float):
        """Keputusan unit saat idle, mempertimbangkan role dan kondisi kingdom."""

        if u.carry > 0:
            u.state = "returning"
            u.tx    = bx + rnd(-25, 25)
            u.ty    = by + rnd(-25, 25)
            return

        # --- Armed unit ---
        if u.armed:
            # Aggression: cek musuh di radius lebih luas kalau sudah di wilayah musuh
            radius = AGGRESSION_RADIUS if self._in_enemy_territory(u, ek) else PATROL_RADIUS
            enemy_in_range = self._nearest_enemy_in_radius(u, radius)
            if enemy_in_range:
                u.target_unit = enemy_in_range
                u.state       = "chasing"
                return

            if k.u_attack >= UTILITY_ATTACK_THRESHOLD:
                enemies = [e for e in self.units if e.kingdom != u.kingdom and e.hp > 0]
                # Filter out protected enemies
                unprotected_enemies = []
                for e in enemies:
                    ek_base = self.kingdoms[e.kingdom]
                    is_protected = ek_base.base_hp > 0 and dst(e.x, e.y, ek_base.base_x, ek_base.base_y) <= 35
                    if not is_protected:
                        unprotected_enemies.append(e)

                if unprotected_enemies:
                    unprotected_enemies.sort(key=lambda e: e.hp)  # kejar yang paling lemah
                    u.target_unit = unprotected_enemies[0]
                    u.state       = "chasing"
                else:
                    # No unprotected enemies. Attack buildings or base shield!
                    ek_buildings = [b for b in self.buildings if b.kingdom != u.kingdom and b.hp > 0]
                    if ek_buildings:
                        target_b = random.choice(ek_buildings)
                        u.target_building = target_b
                        u.tx = target_b.x
                        u.ty = target_b.y
                        u.state = "attacking"
                    else:
                        # Attack the base shield directly!
                        u.tx    = ek.base_x
                        u.ty    = ek.base_y
                        u.state = "attacking"
            else:
                # Patroli di sekitar base sendiri
                u.state = "patrolling"
                u.tx    = bx + rnd(-60, 60)
                u.ty    = by + rnd(-60, 60)
            return

        # --- Unarmed unit: cek role ---

        # CALL TO ARMS (Militia) → Jika base diserang, SEMUA pekerja wajib jaga base!
        if k.base_under_attack:
            u.state = "defending_base"
            u.tx    = bx + rnd(-40, 40)
            u.ty    = by + rnd(-40, 40)
            return

        # DEFENDER role → utamakan jaga base (jika tidak diserang, mereka patroli kecil)
        if u.role == "defender" and k.base_under_attack:
            # (Baris ini ditinggalkan sebagai fallback role logis)
            u.state = "defending_base"
            u.tx    = bx + rnd(-40, 40)
            u.ty    = by + rnd(-40, 40)
            return

        # BUILDER role → cek apakah bisa bangun sesuatu
        if u.role == "builder":
            if k.wood >= HOUSE_COST["wood"] or (k.wood >= SMITH_COST["wood"] and k.iron >= SMITH_COST["iron"]):
                self._try_build(u.kingdom)
            # fall through ke gather

        # Masuk blacksmith kalau ada slot dan kingdom butuh militer
        if (k.smiths > 0 and k.u_iron > 20.0
                and k.iron >= WEAPON_COST["iron"]):
            avail_smith = next(
                (b for b in self.buildings
                 if b.kingdom == u.kingdom and b.btype == "smith"
                 and b.trainees < b.max_trainees),
                None
            )
            if avail_smith and random.random() < 0.8:
                k.iron                -= WEAPON_COST["iron"]
                avail_smith.trainees  += 1
                u.state                = "going_to_smith"
                u.target_building      = avail_smith
                u.tx, u.ty             = avail_smith.x, avail_smith.y
                return

        # Default: query Job Board for tasks
        assignment = k.job_board.get_assignment(u, k, self.units)
        if assignment:
            job, crafted_tool = assignment
            u.target_res = job.target_res
            u.state = "moving"
            u.tx = job.target_res.x
            u.ty = job.target_res.y
            if crafted_tool:
                self.event_log.add(f"Worker crafted tool ({TOOL_COST['wood']} Wood)", u.kingdom)
        else:
            self._start_wander(u, k)

    # ------------------------------------------------------------------
    def _arrive(self, u: Unit, k: Kingdom, bx: float, by: float):
        """Logika saat unit sampai di tujuan."""
        if u.state == "going_to_smith":
            u.state       = "training"
            u.train_timer = UNIT_TRAIN_TIME
            return

        if u.state == "moving":
            if u.target_res and not u.target_res.depleted:
                u.state = "gathering"
                u.gather_timer = 1.0
            else:
                u.target_res = None
                k.job_board.release_unit_jobs(u)
                self._start_wander(u, k)
            return

        if u.state == "returning":
            k = self.kingdoms[u.kingdom]
            if u.carry_type == "wood":
                k.wood += u.carry
            elif u.carry_type == "iron":
                k.iron += u.carry
            elif u.carry_type == "food":
                k.food += u.carry
                
            u.carry      = 0
            u.carry_type = None
            u.state      = "idle"
            k.job_board.release_unit_jobs(u)
            self._try_build(u.kingdom)
            return

        if u.state == "attacking":
            if getattr(u, 'attack_cooldown', 0) > 0:
                u.x -= math.cos(math.atan2(u.ty - u.y, u.tx - u.x)) * 10
                u.y -= math.sin(math.atan2(u.ty - u.y, u.tx - u.x)) * 10
                return

            u.attack_cooldown = 1.0

            if u.target_unit:
                if u.target_unit.hp > 0:
                    u.target_unit.hp -= UNIT_ATTACK_DAMAGE
                    if u.target_unit.hp <= 0:
                        self.event_log.add("Enemy killed!", u.kingdom)
                        u.state       = "idle"
                        u.target_unit = None
            elif getattr(u, 'target_building', None):
                b = u.target_building
                if b.hp > 0:
                    b.hp -= UNIT_ATTACK_DAMAGE * 2
                    if b.hp <= 0:
                        self.event_log.add(f"🔥 {b.btype.capitalize()} destroyed!", u.kingdom)
                        u.state = "idle"
                        u.target_building = None
            else:
                # Attacking the enemy base shield directly!
                ek = self.kingdoms["blue" if u.kingdom == "red" else "red"]
                if ek.base_hp > 0:
                    ek.base_hp = max(0, ek.base_hp - UNIT_ATTACK_DAMAGE)
                    if ek.base_hp <= 0:
                        self.event_log.add("💥 BASE SHIELD COLLAPSED!", u.kingdom)
                        u.state = "idle"
                else:
                    u.state = "idle"
            return

        if u.state == "patrolling":
            u.state = "idle"
            return

        u.state = "idle"

    # ------------------------------------------------------------------
    # SPATIAL & THREAT EVALUATION
    # ------------------------------------------------------------------
    def _nearest_enemy_in_radius(self, u: Unit, radius: float) -> Optional[Unit]:
        best_target = None
        best_score = -1.0

        nearby_units = self.spatial_hash.get_nearby_units(u.x, u.y, radius)
        for t in nearby_units:
            if t.kingdom != u.kingdom and t.hp > 0:
                d = dst(u.x, u.y, t.x, t.y)
                if d <= radius:
                    score = 1000.0 / max(1.0, d)
                    if t.armed: score += 500.0
                    if t.hp < 4: score += 200.0

                    if score > best_score:
                        best_score = score
                        best_target = t
        return best_target

    def _nearest_armed_enemy(self, u: Unit) -> Optional[Unit]:
        best_target = None
        best_score = -1.0
        radius = 250.0  # Maksimal pencarian wajar

        nearby_units = self.spatial_hash.get_nearby_units(u.x, u.y, radius)
        for t in nearby_units:
            if t.kingdom != u.kingdom and t.armed and t.hp > 0:
                d = dst(u.x, u.y, t.x, t.y)
                if d <= radius:
                    score = 1000.0 / max(1.0, d)
                    if t.hp < 4: score += 200.0
                    
                    if score > best_score:
                        best_score = score
                        best_target = t
        return best_target

    # ------------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------------
    def _move_toward_target(self, u: Unit, dt: float, speed_mult: float = 1.0):
        target_c, target_r = self.grid_map.world_to_grid(u.tx, u.ty)
        current_target_cell = (target_c, target_r)

        # Hanya kalkulasi ulang path jika target berpindah ke CELL grid yang berbeda!
        # Ini mencegah bug unit bergetar (vibrating) di tempat.
        if getattr(u, 'path_target_cell', None) != current_target_cell:
            start_c, start_r = self.grid_map.world_to_grid(u.x, u.y)

            # Jika target exact berada di dalam obstacle, geser ke titik walkable terdekat
            if not self.grid_map.is_walkable(target_c, target_r):
                tc_safe, tr_safe = AStar.find_nearest_walkable(self.grid_map, (target_c, target_r))
                u.tx, u.ty = self.grid_map.grid_to_world(tc_safe, tr_safe)
                target_c, target_r = tc_safe, tr_safe
                current_target_cell = (target_c, target_r)

            u.path = AStar.find_path(self.grid_map, (start_c, start_r), (target_c, target_r))
            u.path_target_cell = current_target_cell
            u.waypoint_idx = 0

            # If path is entirely unreachable
            if not u.path:
                u.state = "idle"
                if u.role == "worker" and getattr(u, 'target_res', None):
                    self.kingdoms[u.kingdom].job_board.release_unit_jobs(u)
                return

        # Follow cached path waypoints
        if u.path and u.waypoint_idx < len(u.path):
            wc, wr = u.path[u.waypoint_idx]
            wx, wy = self.grid_map.grid_to_world(wc, wr)
            
            # Calculate speed with terrain and starvation modifiers
            terrain_cost = self.grid_map.get_cost(wc, wr)
            current_speed = (u.speed / terrain_cost) * speed_mult
            
            dx = wx - u.x
            dy = wy - u.y
            d = math.hypot(dx, dy)
            
            if d < 4.0: # Close enough to waypoint, increment index
                u.waypoint_idx += 1
            else:
                u.x += (dx / d) * current_speed * dt
                u.y += (dy / d) * current_speed * dt
        elif u.path:
            # Fallback straight-line movement for fine adjustments at terminal point ONLY if path was valid
            dx = u.tx - u.x
            dy = u.ty - u.y
            d = math.hypot(dx, dy)
            if d > 0.5:
                # Limit fallback speed across obstacles if they somehow clip
                u.x += (dx / d) * (u.speed * speed_mult) * dt
                u.y += (dy / d) * (u.speed * speed_mult) * dt

    def _tick_hero(self, u: Unit, dt: float):
        if u.dash_timer > 0: u.dash_timer -= dt
        if u.slash_timer > 0: u.slash_timer -= dt

        is_dashing = (u.dash_cooldown - u.dash_timer) < 0.2 and u.dash_timer > 0

        # Facing angle
        mx, my = self.input_state["mx"], self.input_state["my"]
        if not is_dashing:
            u.facing_angle = math.atan2(my - u.y, mx - u.x)

        # Movement
        speed = u.speed * 2.0
        if is_dashing:
            speed = u.speed * 8.0
            dx = math.cos(u.facing_angle) * speed * dt
            dy = math.sin(u.facing_angle) * speed * dt
        else:
            dx, dy = 0, 0
            if self.input_state["w"]: dy -= speed * dt
            if self.input_state["s"]: dy += speed * dt
            if self.input_state["a"]: dx -= speed * dt
            if self.input_state["d"]: dx += speed * dt

            if dx != 0 and dy != 0:
                length = math.hypot(dx, dy)
                dx = (dx / length) * speed * dt
                dy = (dy / length) * speed * dt

        nx, ny = u.x + dx, u.y + dy

        c, r = self.grid_map.world_to_grid(nx, ny)
        if self.grid_map.is_walkable(c, r) or is_dashing:
            u.x, u.y = nx, ny
            u.x = clamp(u.x, 0, self.grid_map.cols * self.grid_map.cell_size)
            u.y = clamp(u.y, 0, self.grid_map.rows * self.grid_map.cell_size)

        # Normal Slash
        if self.input_state["slash"] and u.slash_timer <= 0 and not is_dashing:
            u.slash_timer = 0.5
            self.effects.append(VisualEffect(u.x, u.y, "slash", u.facing_angle, 0.2, 0.2))
            for e in self.spatial_hash.get_nearby_units(u.x, u.y, 40.0):
                if e != u and e.hp > 0 and e.kingdom != u.kingdom:
                    angle_to_e = math.atan2(e.y - u.y, e.x - u.x)
                    angle_diff = (angle_to_e - u.facing_angle + math.pi) % (2*math.pi) - math.pi
                    if abs(angle_diff) < math.pi / 2.5: # ~72 deg
                        e.hp -= 5
                        if e.hp <= 0:
                            self.event_log.add("Hero slew an enemy!", u.kingdom)
            for b in self.buildings:
                if b.kingdom != u.kingdom and b.hp > 0 and dst(u.x, u.y, b.x, b.y) <= 40.0:
                    b.hp -= 10
                    
            self.input_state["slash"] = False # Consume input

        # Dash-Slash
        if self.input_state["dash"] and u.dash_timer <= 0:
            u.dash_timer = u.dash_cooldown
            self.effects.append(VisualEffect(u.x, u.y, "dash", u.facing_angle, 0.3, 0.3))
            length = u.speed * 8.0 * 0.2
            for e in self.spatial_hash.get_nearby_units(u.x, u.y, length):
                if e != u and e.hp > 0 and e.kingdom != u.kingdom:
                    v_x, v_y = math.cos(u.facing_angle), math.sin(u.facing_angle)
                    w_x, w_y = e.x - u.x, e.y - u.y
                    proj = w_x * v_x + w_y * v_y
                    if 0 < proj < length:
                        perp_dist = math.hypot(w_x - proj*v_x, w_y - proj*v_y)
                        if perp_dist < 30.0:
                            e.hp -= 15
                            if e.hp <= 0:
                                self.event_log.add("Hero obliterated an enemy!", u.kingdom)
                                
            self.input_state["dash"] = False # Consume input

    def _tick_wander(self, u: Unit, dt: float):
        u.wander_timer -= dt
        if u.wander_timer <= 0:
            u.state = "idle"
            return

        step = WANDER_SPEED * dt
        nx   = u.x + math.cos(u.wander_angle) * step
        ny   = u.y + math.sin(u.wander_angle) * step

        margin = 10
        if nx < SIM_X + margin or nx > SIM_X + SIM_W - margin:
            u.wander_angle = math.pi - u.wander_angle
            nx = clamp(nx, SIM_X + margin, SIM_X + SIM_W - margin)
        if ny < SIM_Y + margin or ny > SIM_Y + SIM_H - margin:
            u.wander_angle = -u.wander_angle
            ny = clamp(ny, SIM_Y + margin, SIM_Y + SIM_H - margin)

        nc, nr = self.grid_map.world_to_grid(nx, ny)
        if self.grid_map.is_walkable(nc, nr):
            u.x, u.y = nx, ny
        else:
            u.wander_angle += math.pi + random.uniform(-0.5, 0.5)

    def _start_wander(self, u: Unit, k: Kingdom):
        u.state        = "wandering"
        u.wander_timer = rnd(0, WANDER_CHANGE)

    def _sniff(self, u: Unit, wanted: Optional[str]) -> Optional[Resource]:
        best, best_d = None, float("inf")
        for r in self.resources:
            if r.depleted:
                continue
            if wanted and r.rtype != wanted:
                continue
            d = dst(u.x, u.y, r.x, r.y)
            if d <= SMELL_RADIUS and d < best_d:
                best_d, best = d, r
        return best


    def _in_enemy_territory(self, u: Unit, ek: Kingdom) -> bool:
        """True kalau unit sudah lebih dekat ke base musuh daripada ke base sendiri."""
        k  = self.kingdoms[u.kingdom]
        d_own   = dst(u.x, u.y, k.base_x,  k.base_y)
        d_enemy = dst(u.x, u.y, ek.base_x, ek.base_y)
        return d_enemy < d_own

    def _call_for_help(self, caller: Unit, threat: Unit):
        """Worker minta bantuan — soldier terdekat dalam HELP_REQUEST_RADIUS langsung kejar ancaman."""
        soldiers = [
            s for s in self.units
            if s.kingdom == caller.kingdom and s.armed and s.hp > 0
            and s.state not in ("training", "chasing", "defending_base")
            and dst(s.x, s.y, caller.x, caller.y) <= HELP_REQUEST_RADIUS
        ]
        if soldiers:
            soldiers.sort(key=lambda s: dst(s.x, s.y, threat.x, threat.y))
            responder = soldiers[0]
            responder.target_unit = threat
            responder.state       = "chasing"
            self.event_log.add("Soldier called for help!", caller.kingdom)

    # ------------------------------------------------------------------
    def _try_build(self, kname: str):
        k    = self.kingdoms[kname]
        sign = 1 if kname == "red" else -1

        has_empty_smith = any(
            b.kingdom == kname and b.btype == "smith" and b.trainees < b.max_trainees
            for b in self.buildings
        )
        
        can_build_smith = (not has_empty_smith and k.wood >= SMITH_COST["wood"] and k.iron >= SMITH_COST["iron"])
        can_build_house = (k.wood >= HOUSE_COST["wood"])

        want_smith = k.u_iron > 40.0
        want_house = k.u_wood > 30.0
        want_smith_building = want_smith and not has_empty_smith

        def build_smith():
            k.wood   -= SMITH_COST["wood"]
            k.iron   -= SMITH_COST["iron"]
            k.smiths += 1
            bx = k.base_x + sign * 60 + rnd(-15, 15)
            by = k.base_y - 30 + rnd(-20, 20)
            self.buildings.append(Building(kname, "smith", bx, by))
            self.event_log.add("Blacksmith built!", kname)

        def build_house():
            k.wood   -= HOUSE_COST["wood"]
            k.houses += 1
            bx = k.base_x + sign * 40 + rnd(-20, 20)
            by = k.base_y + rnd(-40, 40)
            self.buildings.append(Building(kname, "house", bx, by))
            self.event_log.add("House built!", kname)

        if k.focus == "WOOD" and want_house:
            # Fokus buat rumah -> TABUNG kayu! Jangan buat smith kecuali sisa kayunya cukup
            if can_build_house:
                build_house()
            elif can_build_smith and (k.wood - SMITH_COST["wood"] >= HOUSE_COST["wood"]):
                build_smith()
        elif k.focus == "IRON" and want_smith_building:
            # Fokus buat militer dan BELUM PUNYA SMITH -> TABUNG kayu untuk smith!
            if can_build_smith:
                build_smith()
            elif can_build_house and (k.wood - HOUSE_COST["wood"] >= SMITH_COST["wood"]):
                build_house()
        else:
            # Fokus lain, bangun apa saja yang bisa dan butuh
            if can_build_smith and want_smith_building:
                build_smith()
            elif can_build_house and want_house:
                build_house()

    # ------------------------------------------------------------------
    def _end_game(self, winner: str):
        self.game_over = True
        self.winner    = winner
        kingdom_key    = "red" if "Red" in winner else "blue"
        self.event_log.add(f"🏆 {winner} wins!", kingdom_key)
