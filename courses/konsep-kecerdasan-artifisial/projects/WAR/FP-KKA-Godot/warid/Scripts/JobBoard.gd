extends RefCounted
class_name JobBoard

# ==============================================================================
# KELAS JOB (TUGAS)
# ==============================================================================
class Job:
	var job_type: String         # "wood", "iron", atau "food"
	var target_res: GameResource # Referensi ke pohon/besi
	var target_pos: Vector2      # Posisi sumber daya
	var assignee: Unit = null    # Pekerja yang mengambil tugas ini

	func _init(p_type: String, p_res: GameResource, p_pos: Vector2):
		job_type = p_type
		target_res = p_res
		target_pos = p_pos

# ==============================================================================
# VARIABEL PAPAN TUGAS
# ==============================================================================
var available_jobs: Array[Job] = []
var active_jobs: Array[Job] = []

# ==============================================================================
# FUNGSI UTAMA
# ==============================================================================

## Memperbarui daftar tugas berdasarkan sumber daya yang ada di peta
func update_jobs(kingdom, world_resources: Array[Node]):
	# 1. Bersihkan tugas yang sumber dayanya sudah habis/hilang
	for arr in [available_jobs, active_jobs]:
		for i in range(arr.size() - 1, -1, -1):
			var job = arr[i]
			if job.target_res == null or job.target_res.depleted:
				arr.remove_at(i)
				if job.assignee:
					job.assignee.target_res = null
					# Jangan panggil release_unit_jobs di sini untuk mencegah loop tak terbatas

	# 2. Cari sumber daya di peta yang belum dijadikan tugas
	for res in world_resources:
		if not res.depleted:
			var already_listed = false
			# Cek apakah sudah ada di antrean
			for job in available_jobs:
				if job.target_res == res:
					already_listed = true
					break
			if not already_listed:
				for job in active_jobs:
					if job.target_res == res:
						already_listed = true
						break
						
			# Jika belum ada, buat tugas baru!
			if not already_listed:
				available_jobs.append(Job.new(res.rtype, res, res.global_position))

## Memberikan tugas paling cocok untuk seorang pekerja yang sedang menganggur
func get_assignment(unit: Unit, kingdom) -> Job:
	if available_jobs.is_empty():
		return null
		
	# Ambil data jumlah pemegang alat langsung dari kerajaan (Instan O(1), tidak bikin lag!)
	var active_tools = kingdom.active_tools
			
	# Relaksasi batas alat: Tergantung jumlah rumah + 1/5 dari total populasi
	var max_tools = max(3, kingdom.houses * 2 + int(kingdom.pop / 5.0))
	var eligible_jobs: Array[Job] = []
	var eligible_can_craft: Array[bool] = []
	
	# Saring tugas mana yang BOLEH diambil pekerja ini
	for job in available_jobs:
		if job.job_type == "iron" and not unit.has_tool:
			# ATURAN CADANGAN (RESERVE): Jika butuh Blacksmith, tahan 6 Kayu!
			var reserve_wood = 0
			if kingdom.focus == "IRON" and kingdom.smiths == 0:
				reserve_wood = Config.SMITH_COST["wood"]
				
			var can_afford = false
			# Boleh beli beliung JIKA kayu sisa dari tabungan masih cukup, 
			# ATAU jika sama sekali tidak punya beliung (paksa beli 1 untuk mulai)
			if kingdom.wood >= Config.TOOL_COST["wood"] + reserve_wood:
				can_afford = true
			elif active_tools == 0 and kingdom.wood >= Config.TOOL_COST["wood"]:
				can_afford = true
				
			if active_tools < max_tools and can_afford and kingdom.focus != "WOOD":
				eligible_jobs.append(job)
				eligible_can_craft.append(true)
		else:
			eligible_jobs.append(job)
			eligible_can_craft.append(false)
			
	if eligible_jobs.is_empty():
		return null
		
	# Minta kerajaan memilih fokus (Food, Wood, atau Iron) berdasarkan kebutuhannya
	var chosen_type = _decide_urgent_job_type(kingdom)
	var filtered_jobs: Array[Job] = []
	var filtered_craft: Array[bool] = []
	
	for i in range(eligible_jobs.size()):
		if eligible_jobs[i].job_type == chosen_type:
			filtered_jobs.append(eligible_jobs[i])
			filtered_craft.append(eligible_can_craft[i])
			
	if not filtered_jobs.is_empty():
		eligible_jobs = filtered_jobs
		eligible_can_craft = filtered_craft
		
	# Cari tugas yang jaraknya paling dekat dengan pekerja
	var best_job: Job = null
	var best_dist: float = INF
	var best_idx: int = -1
	
	for i in range(eligible_jobs.size()):
		var job = eligible_jobs[i]
		var dist = unit.global_position.distance_squared_to(job.target_pos)
		if dist < best_dist:
			best_dist = dist
			best_job = job
			best_idx = i
			
	if best_job != null:
		# Pindahkan dari tersedia menjadi aktif
		available_jobs.erase(best_job)
		active_jobs.append(best_job)
		best_job.assignee = unit
		
		# Jika ini tugas besi dan pekerja butuh beli beli alat (Pickaxe)
		if eligible_can_craft[best_idx]:
			kingdom.wood -= Config.TOOL_COST["wood"]
			unit.has_tool = true
			unit._update_texture()
			
		return best_job
		
	return null

## Melepas tugas dari pekerja (misal saat pekerja mati atau lari ketakutan)
func release_unit_jobs(unit: Unit):
	for i in range(active_jobs.size() - 1, -1, -1):
		var job = active_jobs[i]
		if job.assignee == unit:
			job.assignee = null
			active_jobs.remove_at(i)
			available_jobs.append(job)

## Helper internal untuk sistem Utility AI
func _decide_urgent_job_type(kingdom) -> String:
	var total = kingdom.u_food + kingdom.u_wood + kingdom.u_iron
	if total <= 0:
		var types = ["food", "wood", "iron"]
		return types[randi() % types.size()]
		
	var rand_val = randf() * total
	if rand_val <= kingdom.u_food: return "food"
	if rand_val <= kingdom.u_food + kingdom.u_wood: return "wood"
	return "iron"
