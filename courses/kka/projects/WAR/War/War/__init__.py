
"""
Kingdom War Simulation - FSM AI + Urgency System

Perubahan utama:
  1. Soldier Aktif   — PATROL_RADIUS: langsung kejar musuh tanpa tunggu u_attack threshold
  2. Reaction Ancaman — FLEE_RADIUS: worker drop resource & lari ke base, trigger minta bantuan
  3. Urgensi Kritis  — base diserang / populasi kritis → override semua prioritas
  4. Role Spesialisasi — tiap unit punya role (gatherer/builder/defender) saat spawn

Controls:
  Space       : Start / Pause
  R           : Reset
  1-4         : Speed 0.5x / 1x / 2x / 4x
  Q / Esc     : Quit

Usage:
  python -m War
"""

from .main import main

__all__ = ["main"]
