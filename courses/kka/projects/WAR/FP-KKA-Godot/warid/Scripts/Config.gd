extends Node

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
const WIDTH: int = 1600
const HEIGHT: int = 900
const FPS: int = 60

const SIM_X: float = 240.0
const SIM_Y: float = 320.0 # Diturunkan agar spawn aman di bawah area pegunungan
const SIM_W: float = 1120.0
const SIM_H: float = 560.0 # Disesuaikan agar batas bawah (SIM_Y + SIM_H) tetap di 880

# ---------------------------------------------------------------------------
# GAME TUNING
# ---------------------------------------------------------------------------
var INIT_POP_RED: int = 15
var INIT_POP_BLUE: int = 15
var INIT_RESOURCES: int = 50
const MILITARY_RATIO: float = 0.5 # Target 50% populasi menjadi tentara

const HOUSE_COST = {"wood": 10}
const SMITH_COST = {"wood": 6, "iron": 4}
const WEAPON_COST = {"iron": 0}
const TOOL_COST = {"wood": 3}
const BASE_MAX_HP: float = 100.0

const RESPAWN_TIME_MIN: float = 5.0
const RESPAWN_TIME_MAX: float = 9.0
const RESOURCE_CARRY_AMT: int = 1

const HOUSE_SPAWN_TIME: float = 5.0
const SMITH_MAX_TRAINEES: int = 5

const UNIT_MAX_HP: float = 10.0
const ARMED_MAX_HP: float = 20.0 # Darah prajurit diturunkan jadi 2x lipat saja

const UNIT_ATTACK_DAMAGE: float = 1.5
const ARMED_ATTACK_DAMAGE: float = 3.0 # Damage prajurit diturunkan ke 3.0

const UNIT_SPEED_MIN: float = 28.0
const UNIT_SPEED_MAX: float = 40.0
const UNIT_TRAIN_TIME: float = 20.0

const SMELL_RADIUS: float = 100.0
const WANDER_SPEED: float = 28.0
const WANDER_CHANGE: float = 2.5

# Utility AI
const UTILITY_HOUSE_WOOD_WEIGHT: float = 2.0
const UTILITY_SMITH_IRON_WEIGHT: float = 3.0
const UTILITY_ATTACK_WEIGHT: float = 5.0
const UTILITY_FOOD_WEIGHT: float = 4.0
const UTILITY_ATTACK_THRESHOLD: float = 80.0

# Combat & AI state bounds
const AGGRESSION_RADIUS: float = 180.0
const PATROL_RADIUS: float = 120.0
const FLEE_RADIUS: float = 90.0
const BASE_DANGER_RADIUS: float = 80.0
const CRITICAL_POP_RATIO: float = 0.35
const HELP_REQUEST_RADIUS: float = 200.0
const UTILITY_MILITARY_CAP_RATIO: float = 0.5
const COMBAT_RADIUS: float = 8.0

const MEAL_TIME_INTERVAL: float = 45.0

const RESOURCE_TYPES: Array[String] = ["wood", "wood", "iron", "food", "food", "food"]
const RESOURCE_COLORS = {
	"wood": Color8(59, 109, 17),
	"iron": Color8(95, 94, 90),
	"food": Color8(230, 80, 50)
}

# ==============================================================================
# MAP BARRIER (Gunung Latar Belakang)
# ==============================================================================
func get_mountain_bound(x: float) -> float:
	var base_y = 260.0
	# Kombinasi dua gelombang agar garis pembatas melengkung secara organik
	var wave1 = sin(x * 0.005) * 35.0
	var wave2 = cos(x * 0.012) * 15.0
	return base_y + wave1 + wave2
