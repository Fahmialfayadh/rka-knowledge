
"""
Kingdom War Simulation - Main Entry Point
Game loop utama: input handling, update, render.
"""

from __future__ import annotations

import pygame

from .config import WIDTH, HEIGHT, FPS, GOLD, TEXT_SEC, SIM_X, SIM_Y, SIM_W, SIM_H, CTRL_Y
from .simulation import Simulation
from .renderer import Renderer, GOD_POWERS


def main():
    pygame.init()
    screen    = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Kingdom War — Urgency AI")
    clock     = pygame.time.Clock()
    sim       = Simulation()
    renderer  = Renderer(screen)
    running   = False
    speed     = 1.0
    speed_map = {pygame.K_1: 0.5, pygame.K_2: 1.0, pygame.K_3: 2.0, pygame.K_4: 4.0}
    active_power = "none"
    is_mouse_down = False

    while True:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                btn_w, btn_h = 120, 26
                start_x = SIM_X + 250
                start_y = CTRL_Y
                gap = 6
                
                clicked_ui = False
                if event.button == 1:
                    for i, (pid, label, col) in enumerate(GOD_POWERS):
                        bx = start_x + (i % 5) * (btn_w + gap)
                        by = start_y + (i // 5) * (btn_h + gap)
                        rect = pygame.Rect(bx, by, btn_w, btn_h)
                        if rect.collidepoint(mx, my):
                            active_power = pid if active_power != pid else "none"
                            clicked_ui = True
                            if active_power != "possess" and sim.possessed_unit:
                                sim.possessed_unit.is_possessed = False
                                sim.possessed_unit = None
                            break
                        
                if not clicked_ui and active_power != "none":
                    if SIM_X <= mx <= SIM_X + SIM_W and SIM_Y <= my <= SIM_Y + SIM_H:
                        if active_power == "possess":
                            if sim.possessed_unit:
                                if event.button == 1: sim.input_state["slash"] = True
                                elif event.button == 3: sim.input_state["dash"] = True
                            else:
                                if event.button == 1: sim.apply_god_power(active_power, mx, my)
                        else:
                            if event.button == 1:
                                is_mouse_down = True
                                sim.apply_god_power(active_power, mx, my)
                            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_mouse_down = False
                    
            elif event.type == pygame.MOUSEMOTION:
                if is_mouse_down and active_power != "none" and active_power != "possess":
                    mx, my = event.pos
                    if SIM_X <= mx <= SIM_X + SIM_W and SIM_Y <= my <= SIM_Y + SIM_H:
                        sim.apply_god_power(active_power, mx, my)

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit(); return
                elif event.key == pygame.K_SPACE:
                    if active_power == "possess" and sim.possessed_unit:
                        sim.input_state["dash"] = True
                    else:
                        running = not running
                elif event.key == pygame.K_r:
                    sim = Simulation(); renderer = Renderer(screen); running = False
                elif event.key == pygame.K_TAB:
                    sim.debug_mode = not sim.debug_mode
                elif event.key == pygame.K_w and active_power != "possess": active_power = "water" if active_power != "water" else "none"
                elif event.key == pygame.K_m: active_power = "mountain" if active_power != "mountain" else "none"
                elif event.key == pygame.K_f: active_power = "forest" if active_power != "forest" else "none"
                elif event.key == pygame.K_e: active_power = "grass" if active_power != "grass" else "none"
                elif event.key == pygame.K_b: active_power = "bomb" if active_power != "bomb" else "none"
                elif event.key == pygame.K_l: active_power = "lightning" if active_power != "lightning" else "none"
                elif event.key == pygame.K_u: active_power = "spawn_red" if active_power != "spawn_red" else "none"
                elif event.key == pygame.K_i: active_power = "spawn_blue" if active_power != "spawn_blue" else "none"
                elif event.key == pygame.K_p: 
                    active_power = "possess" if active_power != "possess" else "none"
                    if active_power != "possess" and sim.possessed_unit:
                        sim.possessed_unit.is_possessed = False
                        sim.possessed_unit = None
                elif event.key in speed_map:
                    speed = speed_map[event.key]

        keys = pygame.key.get_pressed()
        if active_power == "possess" and sim.possessed_unit:
            sim.input_state["w"] = keys[pygame.K_w]
            sim.input_state["a"] = keys[pygame.K_a]
            sim.input_state["s"] = keys[pygame.K_s]
            sim.input_state["d"] = keys[pygame.K_d]
            mx, my = pygame.mouse.get_pos()
            sim.input_state["mx"] = mx
            sim.input_state["my"] = my
        else:
            sim.input_state["w"] = False
            sim.input_state["a"] = False
            sim.input_state["s"] = False
            sim.input_state["d"] = False

        if running and not sim.game_over:
            sim.update(dt * speed)

        renderer.draw(sim, running, speed, active_power)
        pygame.display.flip()


if __name__ == "__main__":
    main()
