extends RefCounted
class_name Kingdom

# ==============================================================================
# DATA KERAJAAN
# ==============================================================================
var kname: String
var base_pos: Vector2
var base_node: Building = null

# Ekonomi & Populasi
var pop: int = 0
var wood: int = 0
var iron: int = 0
var food: int = 0

var houses: int = 0
var smiths: int = 0
var active_tools: int = 0
var armed: int = 0

# Status Ancaman
var is_starving: bool = false
var base_under_attack: bool = false
var meal_timer: float = 30.0
var survival_mode: bool = false

# Otak AI (Utility Values)
var u_food: float = 0.0
var u_wood: float = 0.0
var u_iron: float = 0.0
var u_attack: float = 0.0
var focus: String = "FOOD" # Target utama kerajaan saat ini

var job_board: JobBoard = JobBoard.new()

# CSP Job Scheduler
var csp_scheduler: CSPScheduler = CSPScheduler.new()
var csp_timer: float = 0.0       # Timer periodik untuk CSP
const CSP_INTERVAL: float = 6.0  # Jalankan tiap 6 detik

# ==============================================================================
# INISIALISASI
# ==============================================================================
func _init(p_kname: String, p_pos: Vector2):
	kname = p_kname
	base_pos = p_pos
	if kname == "red":
		pop = Config.INIT_POP_RED
	else:
		pop = Config.INIT_POP_BLUE

# ==============================================================================
# EVALUASI KECERDASAN (UTILITY AI)
# ==============================================================================
func evaluate_utilities(enemy_kingdom: Kingdom, all_units: Array[Node], delta: float):
	# 1. Update Waktu Makan (Meal Time)
	meal_timer -= delta
	if meal_timer <= 0:
		meal_timer = Config.MEAL_TIME_INTERVAL
		if food >= pop:
			food -= pop
			is_starving = false
		else:
			food = 0
			is_starving = true
			
	# 2. Food Utility
	var safe_food_level = pop * 2.0
	if food < safe_food_level:
		u_food = ((safe_food_level - food) / safe_food_level) * 100.0 * 4.0 # UTILITY_FOOD_WEIGHT
	else:
		u_food = 0.0

	# 3. Wood Utility
	var pop_cap = max(10, houses * 5 + 10)
	var pop_pressure = float(pop) / float(pop_cap)
	u_wood = max(10.0, pop_pressure * 100.0 * 2.0) # UTILITY_HOUSE_WOOD_WEIGHT

	# 4. Iron Utility
	var my_military = _count_armed_units(all_units, kname)
	var enemy_military = _count_armed_units(all_units, enemy_kingdom.kname)
	armed = my_military
	
	var ideal_armed = int(pop * Config.MILITARY_RATIO) # Diambil dari Config
	var military_pressure = 1.0 - (float(my_military) / float(max(1, ideal_armed))) if my_military < ideal_armed else 0.0
	u_iron = max(10.0, military_pressure * 100.0 * 3.0) # UTILITY_SMITH_IRON_WEIGHT
	
	# 5. Attack Utility
	u_attack = max(0.0, ((my_military - enemy_military) * 10.0 + my_military * 5.0) * 5.0) # UTILITY_ATTACK_WEIGHT
	
	# 6. Override Focus saat kritis
	base_under_attack = false
	for u in all_units:
		if not is_instance_valid(u) or u.is_queued_for_deletion(): continue
		if u.kingdom != kname and u.armed and u.hp > 0 and u.global_position.distance_to(base_pos) <= Config.BASE_DANGER_RADIUS:
			base_under_attack = true
			break
				
	var init_pop = Config.INIT_POP_RED if kname == "red" else Config.INIT_POP_BLUE
	survival_mode = (pop <= int(init_pop * 0.35))
	
	var old_focus = focus
	if survival_mode:
		focus = "SURVIVE"
	elif base_under_attack:
		focus = "DEFEND"
	else:
		var scores = {"FOOD": u_food, "WOOD": u_wood, "IRON": u_iron, "ATTACK": u_attack}
		var best_focus = "FOOD"
		var best_score = u_food
		for k in scores.keys():
			if scores[k] > best_score:
				best_score = scores[k]
				best_focus = k
		focus = best_focus
		
	if focus != old_focus:
		if focus == "ATTACK" and u_attack >= Config.UTILITY_ATTACK_THRESHOLD:
			EventBus.log_event.emit("Focus: ASSAULT", kname)
		elif focus != "ATTACK":
			EventBus.log_event.emit("Focus: " + focus, kname)

# ==============================================================================
# HELPER INTERNAL
# ==============================================================================
# ==============================================================================
# CSP JOB SCHEDULER — PERIODIK BATCH ASSIGNMENT
# ==============================================================================

## Dipanggil dari World._process() setiap frame, tapi CSP hanya berjalan
## tiap CSP_INTERVAL detik (dikendalikan csp_timer internal).
func tick_csp(delta: float, all_units: Array, all_buildings: Array) -> void:
	csp_timer -= delta
	if csp_timer > 0:
		return
	csp_timer = CSP_INTERVAL

	# Kumpulkan unit idle/wandering yang eligible (tidak bersenjata, tidak mati, tidak possessed)
	var eligible: Array = []
	for u in all_units:
		if not is_instance_valid(u) or u.is_queued_for_deletion():
			continue
		if u.kingdom != kname:
			continue
		if u.hp <= 0 or u.is_possessed:
			continue
		if u.state in ["idle", "wandering"] and not u.armed:
			eligible.append(u)

	if eligible.is_empty():
		return

	csp_scheduler.solve_job_assignments(self, eligible, all_buildings)

func _count_armed_units(units: Array[Node], k: String) -> int:
	var count = 0
	for u in units:
		if not is_instance_valid(u) or u.is_queued_for_deletion(): continue
		if u.kingdom == k and u.armed and u.hp > 0:
			count += 1
	return count
