
"""
Kingdom War Simulation - Utility Functions
Fungsi helper umum: matematika, drawing primitif.
"""

from __future__ import annotations

import math
import random

import pygame

from .config import TEXT_PRIMARY


def rnd(a, b):
    return a + random.random() * (b - a)

def dst(ax, ay, bx, by):
    return math.hypot(ax - bx, ay - by)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def draw_rounded_rect(surf, color, rect, radius=10, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surf, border_color, rect, border, border_radius=radius)

_TEXT_CACHE = {}

def draw_text(surf, font, text, pos, color=TEXT_PRIMARY, anchor="topleft"):
    text_str = str(text)
    key = (font, text_str, color)
    
    if key not in _TEXT_CACHE:
        _TEXT_CACHE[key] = font.render(text_str, True, color)
        # Cegah memory leak (Max 2000 cache)
        if len(_TEXT_CACHE) > 2000:
            for k in list(_TEXT_CACHE.keys())[:500]:
                del _TEXT_CACHE[k]
                
    img = _TEXT_CACHE[key]
    r   = img.get_rect()
    setattr(r, anchor, pos)
    surf.blit(img, r)
