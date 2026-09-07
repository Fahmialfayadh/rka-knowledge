
"""
Kingdom War Simulation - Configuration Constants
Semua konstanta konfigurasi, tuning game, dan warna.
"""

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 1600, 900
FPS = 60

SIM_X, SIM_Y = 220, 60
SIM_W, SIM_H = 1140, 780

LEFT_PANEL_X  = 0
RIGHT_PANEL_X = SIM_X + SIM_W + 10
PANEL_W       = 210
PANEL_H       = SIM_H

LOG_X   = SIM_X
LOG_Y   = SIM_Y + SIM_H + 12
LOG_W   = SIM_W
LOG_H   = HEIGHT - LOG_Y - 8

CTRL_X = SIM_X
CTRL_Y = 8
CTRL_H = 48

# ---------------------------------------------------------------------------
# GAME TUNING
# ---------------------------------------------------------------------------
INIT_POP            = 10
INIT_RESOURCES      = 50

HOUSE_COST          = {"wood": 10}
SMITH_COST          = {"wood": 6, "iron": 4}
WEAPON_COST         = {"iron": 1}
TOOL_COST           = {"wood": 3}
BASE_MAX_HP         = 100
RESPAWN_TIME_MIN    = 5.0
RESPAWN_TIME_MAX    = 9.0
RESOURCE_CARRY_AMT  = 1

HOUSE_SPAWN_TIME    = 5.0
SMITH_MAX_TRAINEES  = 5

UNIT_MAX_HP         = 10
UNIT_ATTACK_DAMAGE  = 2
UNIT_SPEED_MIN      = 28.0
UNIT_SPEED_MAX      = 40.0
UNIT_TRAIN_TIME     = 20.0

SMELL_RADIUS        = 100
WANDER_SPEED        = 28.0
WANDER_CHANGE       = 2.5

# Utility AI
UTILITY_HOUSE_WOOD_WEIGHT  = 2.0
UTILITY_SMITH_IRON_WEIGHT  = 3.0
UTILITY_FOOD_WEIGHT        = 4.0
UTILITY_ATTACK_WEIGHT      = 5.0
UTILITY_ATTACK_THRESHOLD   = 80.0
UTILITY_MILITARY_CAP_RATIO = 0.5

# ---- Urgency & Reaction Parameters ----
PATROL_RADIUS       = 120   # soldier langsung kejar musuh dalam radius ini
AGGRESSION_RADIUS   = 180   # soldier di wilayah musuh, radius cari target lebih luas
FLEE_RADIUS         = 90    # worker lari kalau enemy armed dalam radius ini
BASE_DANGER_RADIUS  = 80    # jarak enemy dari base = "base diserang"
CRITICAL_POP_RATIO  = 0.35  # populasi <= 35% awal → survival mode
HELP_REQUEST_RADIUS = 200   # radius soldier yang merespons panggilan bantuan worker

MEAL_TIME_INTERVAL = 45.0 # Detik antar waktu makan

RESOURCE_TYPES  = ["wood", "wood", "iron", "food", "food", "food"]
RESOURCE_COLORS = {"wood": (59, 109, 17), "iron": (95, 94, 90), "food": (230, 80, 50)}

# Colors
BG           = (250, 250, 250)
PANEL_BG     = (255, 255, 255)
PANEL_BORDER = (208, 208, 208)
TEXT_PRIMARY = (51,  51,  51)
TEXT_SEC     = (102, 102, 102)
RED_COL      = (216, 90,  48)
BLUE_COL     = (24,  95,  165)
GOLD         = (230, 175, 50)
GREEN_COL    = (60,  200, 100)
GRASS_TOP    = (184, 212, 160)
GRASS_BOT    = (143, 184, 112)
ORANGE       = (230, 130, 30)
PURPLE       = (160, 80,  200)
