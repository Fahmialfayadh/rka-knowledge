
"""
Kingdom War Simulation - Renderer
Semua fungsi drawing/rendering: map, units, panels, log, UI.
"""

from __future__ import annotations

import random
import math

import pygame

from .config import (
    WIDTH, HEIGHT,
    SIM_X, SIM_Y, SIM_W, SIM_H,
    LEFT_PANEL_X, RIGHT_PANEL_X, PANEL_W, PANEL_H,
    LOG_X, LOG_Y, LOG_W, LOG_H,
    CTRL_X, CTRL_Y, CTRL_H,
    BG, PANEL_BG, PANEL_BORDER,
    TEXT_PRIMARY, TEXT_SEC,
    RED_COL, BLUE_COL, GOLD, GREEN_COL, PURPLE,
    GRASS_TOP, GRASS_BOT,
    RESOURCE_COLORS, BASE_MAX_HP, UNIT_MAX_HP,
)
from .utils import rnd, dst, draw_rounded_rect, draw_text, clamp
from .simulation import Simulation

GOD_POWERS = [
    ("water", "💧 Water (W)", (70, 130, 180)),
    ("mountain", "⛰ Mountain (M)", (139, 90, 43)),
    ("forest", "🌲 Forest (F)", (34, 139, 34)),
    ("grass", "🟩 Eraser (E)", (100, 200, 100)),
    ("bomb", "💣 Bomb (B)", (255, 50, 50)),
    ("lightning", "⚡ Lightning (L)", (255, 255, 0)),
    ("spawn_red", "🔴 Spawn Red (U)", RED_COL),
    ("spawn_blue", "🔵 Spawn Blue (I)", BLUE_COL),
    ("possess", "👻 Possess (P)", PURPLE),
]


class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        pygame.font.init()
        self.f_title = pygame.font.SysFont("segoeui", 20, bold=True)
        self.f_h2    = pygame.font.SysFont("segoeui", 15, bold=True)
        self.f_body  = pygame.font.SysFont("segoeui", 13)
        self.f_small = pygame.font.SysFont("segoeui", 11)
        self.f_badge = pygame.font.SysFont("segoeui", 10, bold=True)
        self.f_tiny  = pygame.font.SysFont("segoeui", 8, bold=True)

        random.seed(42)
        self.noise = [
            (rnd(SIM_X, SIM_X + SIM_W), rnd(SIM_Y, SIM_Y + SIM_H), random.randint(8, 20))
            for _ in range(200)
        ]
        random.seed()
        self.grass = self._make_grass()

    def _make_grass(self):
        s = pygame.Surface((SIM_W, SIM_H))
        for y in range(SIM_H):
            t   = y / SIM_H
            col = tuple(int(GRASS_TOP[i] + (GRASS_BOT[i] - GRASS_TOP[i]) * t) for i in range(3))
            pygame.draw.line(s, col, (0, y), (SIM_W, y))
        return s

    # ------------------------------------------------------------------
    def draw(self, sim: Simulation, running: bool, speed: float, active_power: str = "none"):
        self.screen.fill(BG)
        self._draw_map(sim)
        self._draw_visual_effects(sim)
        self._draw_bases(sim)
        self._draw_buildings(sim)
        self._draw_resources(sim)
        self._draw_units(sim)
        self._draw_left_panel(sim)
        self._draw_right_panel(sim)
        self._draw_controls(sim, running, speed)
        self._draw_god_mode_ui(active_power)
        self._draw_log(sim)
        self._draw_brush_cursor(sim, active_power)
        
        if sim.debug_mode:
            self._draw_debug_overlay(sim)
            
        if sim.game_over:
            self._draw_game_over(sim)

    def _draw_map(self, sim):
        self.screen.blit(self.grass, (SIM_X, SIM_Y))
        
        # Draw road/forest overlays first, so obstacles render on top
        gm = sim.grid_map
        for r in range(gm.rows):
            for c in range(gm.cols):
                code = gm.cells[r][c]
                wx, wy = gm.grid_to_world(c, r)
                rx, ry = int(wx - gm.cell_size / 2), int(wy - gm.cell_size / 2)
                rect = pygame.Rect(rx, ry, gm.cell_size, gm.cell_size)
                
                if code == 4: # Forest
                    # Soft semi-transparent forest green overlays
                    fs = pygame.Surface((gm.cell_size, gm.cell_size), pygame.SRCALPHA)
                    pygame.draw.rect(fs, (34, 139, 34, 90), (0, 0, gm.cell_size, gm.cell_size))
                    self.screen.blit(fs, (rx, ry))
                elif code == 5: # Road
                    # Soft concrete/sand path
                    pygame.draw.rect(self.screen, (225, 210, 180), rect)

        # Draw semi-transparent grass noise
        ns = pygame.Surface((SIM_W, SIM_H), pygame.SRCALPHA)
        for nx, ny, na in self.noise:
            pygame.draw.circle(ns, (0, 0, 0, na), (int(nx - SIM_X), int(ny - SIM_Y)), 3)
        self.screen.blit(ns, (SIM_X, SIM_Y))

        # Draw static blocking obstacles on top
        for r in range(gm.rows):
            for c in range(gm.cols):
                code = gm.cells[r][c]
                wx, wy = gm.grid_to_world(c, r)
                rx, ry = int(wx - gm.cell_size / 2), int(wy - gm.cell_size / 2)
                rect = pygame.Rect(rx, ry, gm.cell_size, gm.cell_size)
                
                if code == 1: # Wall
                    # Textured solid brown walls
                    pygame.draw.rect(self.screen, (101, 67, 33), rect, border_radius=4)
                    pygame.draw.rect(self.screen, (139, 90, 43), rect.inflate(-4, -4), border_radius=2)
                elif code == 2: # Rock
                    # Round dark slate rock
                    pygame.draw.circle(self.screen, (80, 80, 85), (int(wx), int(wy)), gm.cell_size // 2 - 2)
                    pygame.draw.circle(self.screen, (110, 110, 115), (int(wx) - 2, int(wy) - 2), gm.cell_size // 4)
                elif code == 3: # River
                    # Solid water channels
                    pygame.draw.rect(self.screen, (70, 130, 180), rect)
                    # Small stream details
                    pygame.draw.line(self.screen, (135, 206, 250), (rx + 2, ry + 4), (rx + gm.cell_size - 2, ry + 4), 1)
                    pygame.draw.line(self.screen, (135, 206, 250), (rx + 4, ry + 12), (rx + gm.cell_size - 4, ry + 12), 1)

        # Border
        pygame.draw.rect(self.screen, PANEL_BORDER, (SIM_X, SIM_Y, SIM_W, SIM_H), 1, border_radius=12)

    def _draw_visual_effects(self, sim):
        for eff in sim.effects:
            if eff.type == "explosion":
                alpha = int(255 * (eff.timer / eff.max_timer))
                s = pygame.Surface((eff.radius*2, eff.radius*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 100, 0, alpha), (eff.radius, eff.radius), eff.radius)
                pygame.draw.circle(s, (255, 200, 0, alpha), (eff.radius, eff.radius), eff.radius * 0.6)
                self.screen.blit(s, (eff.x - eff.radius, eff.y - eff.radius))
            elif eff.type == "lightning":
                alpha = int(255 * (eff.timer / eff.max_timer))
                points = [(eff.x, 0), (eff.x - 10, eff.y * 0.3), (eff.x + 10, eff.y * 0.6), (eff.x, eff.y)]
                pygame.draw.lines(self.screen, (255, 255, 255, alpha), False, points, 4)
                pygame.draw.circle(self.screen, (200, 200, 255, alpha), (int(eff.x), int(eff.y)), eff.radius)
            elif eff.type == "slash":
                alpha = int(255 * (eff.timer / eff.max_timer))
                angle = eff.radius # radius is overloaded as angle
                s = pygame.Surface((100, 100), pygame.SRCALPHA)
                rect = pygame.Rect(10, 10, 80, 80)
                start_angle = -angle - math.pi/2.5
                end_angle = -angle + math.pi/2.5
                pygame.draw.arc(s, (255, 255, 255, alpha), rect, start_angle, end_angle, 6)
                self.screen.blit(s, (eff.x - 50, eff.y - 50))
            elif eff.type == "dash":
                alpha = int(255 * (eff.timer / eff.max_timer))
                angle = eff.radius
                length = 200.0
                end_x = eff.x + math.cos(angle) * length
                end_y = eff.y + math.sin(angle) * length
                pygame.draw.line(self.screen, (255, 255, 100, alpha), (eff.x, eff.y), (end_x, end_y), 8)
                pygame.draw.line(self.screen, (255, 255, 255, alpha), (eff.x, eff.y), (end_x, end_y), 3)

    def _draw_god_mode_ui(self, active_power: str):
        btn_w, btn_h = 120, 26
        start_x = SIM_X + 250
        start_y = CTRL_Y
        gap = 6
        
        for i, (pid, label, col) in enumerate(GOD_POWERS):
            bx = start_x + (i % 5) * (btn_w + gap)
            by = start_y + (i // 5) * (btn_h + gap)
            rect = pygame.Rect(bx, by, btn_w, btn_h)
            
            mx, my = pygame.mouse.get_pos()
            is_hover = rect.collidepoint(mx, my)
            
            bg_col = (col[0]*0.2, col[1]*0.2, col[2]*0.2) if active_power != pid else col
            if is_hover and active_power != pid:
                bg_col = (col[0]*0.4, col[1]*0.4, col[2]*0.4)
                
            draw_rounded_rect(self.screen, bg_col, rect, 6)
            pygame.draw.rect(self.screen, col, rect, 2, border_radius=6)
            
            text_col = (255, 255, 255) if active_power == pid else col
            draw_text(self.screen, self.f_body, label, rect.center, text_col, anchor="center")

    def _draw_brush_cursor(self, sim, active_power):
        if active_power == "none": return
        mx, my = pygame.mouse.get_pos()
        if not (SIM_X <= mx <= SIM_X + SIM_W and SIM_Y <= my <= SIM_Y + SIM_H): return
        
        radius = 20
        if active_power in ("water", "mountain", "forest", "grass"):
            radius = sim.grid_map.cell_size * 2.5
        elif active_power == "bomb":
            radius = 60
        elif active_power == "lightning":
            radius = 20
            
        s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 255, 80), (radius, radius), radius, 2)
        pygame.draw.circle(s, (255, 255, 255, 30), (radius, radius), radius)
        self.screen.blit(s, (mx - radius, my - radius))

    def _draw_debug_overlay(self, sim: Simulation):
        gm = sim.grid_map
        # 1. Draw Grid mesh lines
        for c in range(gm.cols + 1):
            wx = gm.x + c * gm.cell_size
            pygame.draw.line(self.screen, (200, 200, 200, 70), (wx, gm.y), (wx, gm.y + gm.h), 1)
        for r in range(gm.rows + 1):
            wy = gm.y + r * gm.cell_size
            pygame.draw.line(self.screen, (200, 200, 200, 70), (gm.x, wy), (gm.x + gm.w, wy), 1)

        # 2. Draw A* Path lines for every moving unit
        for u in sim.units:
            if u.hp <= 0 or not u.path:
                continue
            col = RED_COL if u.kingdom == "red" else BLUE_COL
            points = []
            # Draw from current position to remaining waypoints
            points.append((u.x, u.y))
            for i in range(u.waypoint_idx, len(u.path)):
                wx, wy = gm.grid_to_world(u.path[i][0], u.path[i][1])
                points.append((wx, wy))
            
            if len(points) >= 2:
                pygame.draw.lines(self.screen, col, False, points, 2)
                # Draw current active target waypoint node
                if u.waypoint_idx < len(u.path):
                    tc, tr = u.path[u.waypoint_idx]
                    tx, ty = gm.grid_to_world(tc, tr)
                    pygame.draw.circle(self.screen, GOLD, (int(tx), int(ty)), 4)

    def _draw_bases(self, sim):
        for k in sim.kingdoms.values():
            bx, by = int(k.base_x), int(k.base_y)
            col    = k.color
            # Flash merah kalau base diserang
            if k.base_under_attack:
                flash = pygame.Surface((80, 80), pygame.SRCALPHA)
                pygame.draw.rect(flash, (255, 50, 50, 60), (0, 0, 80, 80), border_radius=10)
                self.screen.blit(flash, (bx - 40, by - 40))
            gs = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.rect(gs, (*col, 40), (0, 0, 80, 80), border_radius=10)
            self.screen.blit(gs, (bx - 40, by - 40))
            pygame.draw.rect(self.screen, col, (bx - 30, by - 30, 60, 60), 2, border_radius=8)
            label = "RED" if k.key == "red" else "BLUE"
            if k.survival_mode:
                label += " ☠"
            draw_text(self.screen, self.f_badge, label, (bx, by - 40), col, anchor="center")

            # Draw Base Shield HP Bar
            if k.base_hp > 0:
                bar_w = 60
                bar_h = 4
                bx_start = bx - bar_w // 2
                by_start = by - 33
                # Draw background
                pygame.draw.rect(self.screen, (60, 60, 70), (bx_start, by_start, bar_w, bar_h))
                # Draw foreground
                fill_w = int(bar_w * (k.base_hp / BASE_MAX_HP))
                if fill_w > 0:
                    pygame.draw.rect(self.screen, (0, 200, 200), (bx_start, by_start, fill_w, bar_h))

    def _draw_buildings(self, sim):
        for b in sim.buildings:
            col = RED_COL if b.kingdom == "red" else BLUE_COL
            bx, by = int(b.x), int(b.y)
            if b.btype == "house":
                pygame.draw.rect(self.screen, col, (bx - 10, by - 12, 20, 16))
                pygame.draw.polygon(self.screen, col,
                                    [(bx - 13, by - 12), (bx, by - 22), (bx + 13, by - 12)])
            else:
                pygame.draw.rect(self.screen, (85, 85, 85), (bx - 12, by - 8, 24, 16))
                pygame.draw.rect(self.screen, col, (bx - 4, by - 16, 8, 8))
                for i, sy in enumerate([by - 20, by - 26, by - 31]):
                    a  = 80 - i * 25
                    ss = pygame.Surface((8, 8), pygame.SRCALPHA)
                    pygame.draw.circle(ss, (180, 180, 180, a), (4, 4), 4 - i)
                    self.screen.blit(ss, (bx - 4, sy))
                badge_txt  = f"{b.trainees}/{b.max_trainees}"
                badge_w    = self.f_badge.size(badge_txt)[0] + 8
                badge_rect = pygame.Rect(bx - badge_w // 2, by + 10, badge_w, 14)
                draw_rounded_rect(self.screen, col, badge_rect, 4)
                draw_text(self.screen, self.f_badge, badge_txt,
                          badge_rect.center, (255, 255, 255), anchor="center")

    def _draw_resources(self, sim):
        for r in sim.resources:
            if r.depleted:
                continue
            col = RESOURCE_COLORS[r.rtype]
            rx, ry = int(r.x), int(r.y)
            if r.rtype == "wood":
                pygame.draw.circle(self.screen, col, (rx, ry), 7)
            elif r.rtype == "food":
                # Draw small berries
                pygame.draw.circle(self.screen, col, (rx - 3, ry + 2), 4)
                pygame.draw.circle(self.screen, col, (rx + 3, ry + 2), 4)
                pygame.draw.circle(self.screen, col, (rx, ry - 3), 4)
            else:
                pygame.draw.rect(self.screen, col, (rx - 6, ry - 5, 12, 10))

            if r.rtype != "food":
                draw_text(self.screen, self.f_small, r.rtype[0].upper(),
                          (rx, ry), (255, 255, 255), anchor="center")

    def _draw_units(self, sim):
        mx, my = pygame.mouse.get_pos()
        self.hovered_unit = None
        min_d = 12.0
        
        # 1. Find hovered unit
        for u in sim.units:
            if u.hp <= 0 or u.state == "training":
                continue
            d = dst(mx, my, u.x, u.y)
            if d < min_d:
                min_d = d
                self.hovered_unit = u

        state_colors = {
            "fleeing":        (230, 50,  50),
            "survival":       (200,  50, 200),
        }
        
        # 2. Render units
        for u in sim.units:
            if u.hp <= 0 or u.state == "training":
                continue
            base_col = RED_COL if u.kingdom == "red" else BLUE_COL
            col      = state_colors.get(u.state, base_col)
            ux, uy   = int(u.x), int(u.y)
            radius   = 5 if u.armed else 3
            alpha    = 255 if u.armed else 160

            s = pygame.Surface((radius * 2 + 6, radius * 2 + 6), pygame.SRCALPHA)
            pygame.draw.circle(s, (*col, alpha), (radius + 3, radius + 3), radius)
            
            # Draw state-specific glowing rings (outline)
            if u.state == "chasing":
                pygame.draw.circle(s, (255, 180, 0, 200), (radius + 3, radius + 3), radius + 2, 2)
            elif u.state == "defending_base":
                pygame.draw.circle(s, (0, 200, 200, 200), (radius + 3, radius + 3), radius + 2, 2)

            self.screen.blit(s, (ux - radius - 3, uy - radius - 3))

            # Draw a glowing cyan ring around workers equipped with tools (much more visible)
            if not u.armed and u.has_tool:
                pygame.draw.circle(self.screen, (0, 255, 255), (ux, uy), radius + 3, 2)

            # Hero Aura
            if getattr(u, 'is_possessed', False):
                pygame.draw.circle(self.screen, GOLD, (ux, uy), 15, 3)
                pygame.draw.circle(self.screen, (GOLD[0], GOLD[1], GOLD[2], 100), (ux, uy), 15)
                
                # Draw Cooldown Bar
                cd_ratio = 1.0 - (u.dash_timer / u.dash_cooldown) if u.dash_cooldown > 0 else 1.0
                bar_w = 20
                pygame.draw.rect(self.screen, (50, 50, 50), (ux - bar_w//2, uy - 20, bar_w, 4))
                pygame.draw.rect(self.screen, (0, 255, 255), (ux - bar_w//2, uy - 20, int(bar_w * cd_ratio), 4))

            # Carry dot
            if u.carry > 0:
                pygame.draw.circle(self.screen, GOLD, (ux + 4, uy - 4), 2)

            # Draw persistent tactical badge above unit
            badge_bg = (160, 170, 180)
            badge_text = ""
            border_col = None
            
            if u.armed:
                badge_bg = (190, 30, 45) # Crimson
                badge_text = "A"
            else:
                if u.state == "going_to_smith":
                    badge_bg = (235, 130, 20) # Orange
                    badge_text = "T"
                elif u.state == "returning":
                    res_type = u.carry_type if u.carry_type else "wood"
                    badge_text = res_type[0].upper()
                    badge_bg = (34, 139, 34) if res_type == "wood" else (112, 128, 144) if res_type == "iron" else (230, 80, 50)
                    border_col = GOLD
                elif u.state == "moving":
                    res_type = u.carry_type if u.carry_type else (u.target_res.rtype if u.target_res else "wood")
                    badge_text = res_type[0].upper()
                    badge_bg = (34, 139, 34) if res_type == "wood" else (112, 128, 144) if res_type == "iron" else (230, 80, 50)
                elif u.state == "wandering":
                    res_type = u.smell_type if u.smell_type else "wood"
                    badge_text = res_type[0].upper()
                    badge_bg = (34, 139, 34) if res_type == "wood" else (112, 128, 144) if res_type == "iron" else (230, 80, 50)
                elif u.state == "fleeing":
                    badge_bg = (220, 40, 40)
                    badge_text = "!"
                elif u.state == "survival":
                    badge_bg = (180, 40, 180)
                    badge_text = "S"
                elif u.state == "defending_base":
                    badge_bg = (0, 180, 180)
                    badge_text = "D"
                else:
                    badge_bg = (140, 145, 150)
                    badge_text = "Z"

            if badge_text:
                bx, by = ux, uy - 12
                pygame.draw.circle(self.screen, badge_bg, (bx, by), 6)
                if border_col:
                    pygame.draw.circle(self.screen, border_col, (bx, by), 6, 1)
                draw_text(self.screen, self.f_tiny, badge_text, (bx, by), (255, 255, 255), anchor="center")

            # Draw micro health bar if damaged
            if u.hp < UNIT_MAX_HP:
                bar_y = uy + 6
                bar_w = 12
                bar_h = 3
                pygame.draw.rect(self.screen, (200, 50, 50), (ux - bar_w // 2, bar_y, bar_w, bar_h))
                fill_w = int(bar_w * (u.hp / UNIT_MAX_HP))
                if fill_w > 0:
                    pygame.draw.rect(self.screen, (50, 200, 50), (ux - bar_w // 2, bar_y, fill_w, bar_h))

        # Highlight hovered unit
        if self.hovered_unit:
            hu = self.hovered_unit
            h_radius = 5 if hu.armed else 3
            h_col = RED_COL if hu.kingdom == "red" else BLUE_COL
            pygame.draw.circle(self.screen, (255, 255, 255), (int(hu.x), int(hu.y)), h_radius + 3, 1)
            pygame.draw.circle(self.screen, h_col, (int(hu.x), int(hu.y)), h_radius + 4, 1)

    def _draw_hover_tooltip(self, sim: Simulation):
        u = self.hovered_unit
        if not u:
            return
        k = sim.kingdoms[u.kingdom]
        
        mx, my = pygame.mouse.get_pos()
        tx = mx + 15
        ty = my + 15
        
        tw, th = 200, 115
        if tx + tw > WIDTH:
            tx = mx - tw - 15
        if ty + th > HEIGHT:
            ty = my - th - 15
        if tx < 0:
            tx = 10
        if ty < 0:
            ty = 10
            
        # Translucent background card
        ts = pygame.Surface((tw, th), pygame.SRCALPHA)
        draw_rounded_rect(ts, (20, 22, 32, 235), pygame.Rect(0, 0, tw, th), 10, 1, (120, 120, 130, 200))
        self.screen.blit(ts, (tx, ty))
        
        k_col = RED_COL if u.kingdom == "red" else BLUE_COL
        k_name = "Red Dominion" if u.kingdom == "red" else "Blue Covenant"
        
        draw_text(self.screen, self.f_h2, k_name, (tx + 12, ty + 10), k_col)
        
        role_text = "SOLDIER (Armed)" if u.armed else f"WORKER ({u.role.upper()})"
        role_col = GOLD if u.armed else (140, 200, 255)
        draw_text(self.screen, self.f_badge, role_text, (tx + 12, ty + 28), role_col)
        
        # HP Text & HP Bar
        draw_text(self.screen, self.f_small, f"HP: {u.hp}/{UNIT_MAX_HP}", (tx + 12, ty + 44), (240, 240, 240))
        hp_bar_w = 80
        hp_bar_h = 6
        hp_x = tx + tw - hp_bar_w - 12
        hp_y = ty + 47
        draw_rounded_rect(self.screen, (60, 60, 70), pygame.Rect(hp_x, hp_y, hp_bar_w, hp_bar_h), 2)
        fill_w = int(hp_bar_w * (u.hp / UNIT_MAX_HP))
        if fill_w > 0:
            draw_rounded_rect(self.screen, (46, 204, 113), pygame.Rect(hp_x, hp_y, fill_w, hp_bar_h), 2)
            
        # State & Urgency
        state_desc = "Idle"
        urgency_desc = "N/A"
        
        if u.armed:
            state_desc = "Assaulting Enemy" if u.state in ("attacking", "chasing") else u.state.capitalize().replace("_", " ")
            urgency_desc = f"Attack Urgency: {k.u_attack:.1f}%"
        else:
            if u.state == "going_to_smith":
                state_desc = "Going to Blacksmith"
                urgency_desc = f"Smith Urgency: {k.u_iron:.1f}%"
            elif u.state == "returning":
                res = "Wood" if u.carry_type == "wood" else "Iron"
                state_desc = f"Carrying {res}"
                urgency_desc = f"Carrying {u.carry} units"
            elif u.state == "moving":
                res = u.carry_type if u.carry_type else (u.target_res.rtype if u.target_res else "wood")
                state_desc = f"Gathering {res.capitalize()}"
                urg_score = k.u_wood if res == "wood" else k.u_iron
                urgency_desc = f"{res.capitalize()} Urgency: {urg_score:.1f}%"
            elif u.state == "wandering":
                res = u.smell_type if u.smell_type else "wood"
                state_desc = f"Searching for {res.capitalize()}"
                urg_score = k.u_wood if res == "wood" else k.u_iron
                urgency_desc = f"{res.capitalize()} Urgency: {urg_score:.1f}%"
            else:
                state_desc = u.state.capitalize().replace("_", " ")
                urgency_desc = "Deciding next action..."
                
        draw_text(self.screen, self.f_body, f"Action: {state_desc}", (tx + 12, ty + 64), (220, 220, 220))
        
        # Tools & Driver info
        tool_status = "Equipped" if u.has_tool else "None"
        draw_text(self.screen, self.f_small, f"Tool: {tool_status} | {urgency_desc}", (tx + 12, ty + 84), (180, 180, 180))
        
        # A* Path status
        path_nodes = len(u.path) - u.waypoint_idx if u.path else 0
        draw_text(self.screen, self.f_small, f"A* Path: {path_nodes} waypoints remaining", (tx + 12, ty + 98), (140, 150, 160))

    # ------------------------------------------------------------------
    def _draw_kingdom_panel(self, sim, kname, panel_x, panel_y):
        k    = sim.kingdoms[kname]
        col  = k.color
        rect = pygame.Rect(panel_x, panel_y, PANEL_W, PANEL_H)
        draw_rounded_rect(self.screen, PANEL_BG, rect, 12, 1, PANEL_BORDER)

        # Alert banner
        if k.survival_mode:
            alert_rect = pygame.Rect(panel_x + 4, panel_y + 4, PANEL_W - 8, 18)
            draw_rounded_rect(self.screen, (200, 50, 200), alert_rect, 4)
            draw_text(self.screen, self.f_badge, "☠ SURVIVAL MODE",
                      alert_rect.center, (255, 255, 255), anchor="center")
        elif k.base_under_attack:
            alert_rect = pygame.Rect(panel_x + 4, panel_y + 4, PANEL_W - 8, 18)
            draw_rounded_rect(self.screen, (200, 50, 50), alert_rect, 4)
            draw_text(self.screen, self.f_badge, "⚠ BASE UNDER ATTACK",
                      alert_rect.center, (255, 255, 255), anchor="center")

        icon = "⚔" if kname == "red" else "🛡"
        draw_text(self.screen, self.f_h2, f"{icon} {k.name}",
                  (panel_x + 12, panel_y + 28), col)

        badge_col  = (238, 238, 238)
        badge_rect = pygame.Rect(panel_x + PANEL_W - 90, panel_y + 26, 78, 20)
        draw_rounded_rect(self.screen, badge_col, badge_rect, 4)
        draw_text(self.screen, self.f_badge, f"FOCUS: {k.focus}",
                  badge_rect.center, TEXT_PRIMARY, anchor="center")

        workers = k.pop - k.armed
        rows = [
            ("Base Shield", f"{k.base_hp}/{BASE_MAX_HP}" if k.base_hp > 0 else "COLLAPSED"),
            ("Population", str(k.pop)),
            ("Workers",    str(workers)),
            ("Armed",      str(k.armed)),
            ("Wood",       str(int(k.wood))),
            ("Iron",       str(int(k.iron))),
            ("Houses",     str(k.houses)),
            ("Blacksmiths",str(k.smiths)),
        ]
        y_off = panel_y + 55
        for label, val in rows:
            pygame.draw.line(self.screen, (238, 238, 238),
                             (panel_x + 8, y_off + 18),
                             (panel_x + PANEL_W - 8, y_off + 18), 1)
            draw_text(self.screen, self.f_body, label,
                      (panel_x + 12, y_off), TEXT_SEC)
            draw_text(self.screen, self.f_h2, val,
                      (panel_x + PANEL_W - 12, y_off), TEXT_PRIMARY, anchor="topright")
            y_off += 26

        bars = [("Food", k.food, (230, 80, 50), 50),
                ("Wood", k.wood, (150, 104, 56), 100),
                ("Iron", k.iron, (150, 160, 170), 80)]
        y_off += 6
        for bar_label, val, bar_col, maxv in bars:
            draw_text(self.screen, self.f_small, bar_label,
                      (panel_x + 12, y_off), TEXT_SEC)
            bar_rect = pygame.Rect(panel_x + 12, y_off + 14, PANEL_W - 24, 7)
            draw_rounded_rect(self.screen, (220, 220, 220), bar_rect, 4)
            fill_w = int(bar_rect.width * clamp(val / maxv, 0, 1))
            if fill_w > 0:
                draw_rounded_rect(self.screen, bar_col,
                                  pygame.Rect(bar_rect.x, bar_rect.y, fill_w, bar_rect.height), 4)
            y_off += 26

    def _draw_left_panel(self, sim):
        self._draw_kingdom_panel(sim, "red", LEFT_PANEL_X + 6, SIM_Y)

    def _draw_right_panel(self, sim):
        self._draw_kingdom_panel(sim, "blue", RIGHT_PANEL_X, SIM_Y)

    def _draw_controls(self, sim, running, speed):
        draw_text(self.screen, self.f_h2, "♛ Kingdom War — Urgency AI",
                  (SIM_X, CTRL_Y + 4), TEXT_PRIMARY)
        draw_text(self.screen, self.f_h2, f"t = {int(sim.sim_time)}s",
                  (SIM_X + SIM_W, CTRL_Y + 4), TEXT_SEC, anchor="topright")
        hint = "Space: Play/Pause   R: Reset   1-4: 0.5x/1x/2x/4x   Q: Quit"
        draw_text(self.screen, self.f_small, hint,
                  (SIM_X + SIM_W // 2, CTRL_Y + 30), TEXT_SEC, anchor="center")
        col = GOLD if running else TEXT_SEC
        draw_text(self.screen, self.f_h2, f"Speed: {speed}x",
                  (SIM_X + SIM_W // 2, CTRL_Y + 4), col, anchor="center")

        # Legend warna state
        legend = [
            ("yellow outline = chasing",  (255, 180, 0)),
            ("cyan outline = defend base",(0, 200, 200)),
            ("red dot = fleeing (!)", (230,50,50)),
            ("purple = survival", (200,50,200)),
        ]
        lx = SIM_X
        ly = CTRL_Y + 44
        for txt, lcol in legend:
            draw_text(self.screen, self.f_small, txt, (lx, ly), lcol)
            lx += 130

    def _draw_log(self, sim):
        rect = pygame.Rect(LOG_X, LOG_Y, LOG_W, LOG_H)
        draw_rounded_rect(self.screen, PANEL_BG, rect, 12, 1, PANEL_BORDER)
        draw_text(self.screen, self.f_h2, "Event Log",
                  (LOG_X + 12, LOG_Y + 6), TEXT_PRIMARY)
        y_off = LOG_Y + 28
        for kingdom, label, msg in sim.event_log.items:
            if y_off + 16 > LOG_Y + LOG_H - 4:
                break
            col = RED_COL if kingdom == "red" else BLUE_COL
            draw_text(self.screen, self.f_small, label, (LOG_X + 12, y_off), col)
            draw_text(self.screen, self.f_small, msg,   (LOG_X + 48, y_off), TEXT_SEC)
            y_off += 17

    def _draw_game_over(self, sim):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))
        box = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 90, 400, 180)
        draw_rounded_rect(self.screen, (20, 22, 32), box, 16, 2, GOLD)
        draw_text(self.screen, self.f_title, "GAME OVER",
                  (box.centerx, box.y + 30), GOLD, anchor="center")
        draw_text(self.screen, self.f_h2, f"Winner: {sim.winner}",
                  (box.centerx, box.y + 72), (230, 225, 210), anchor="center")
        draw_text(self.screen, self.f_body, "Press R to restart",
                  (box.centerx, box.y + 144), GOLD, anchor="center")
