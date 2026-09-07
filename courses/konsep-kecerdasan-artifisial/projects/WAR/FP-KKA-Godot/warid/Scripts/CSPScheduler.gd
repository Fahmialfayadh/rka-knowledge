extends RefCounted
class_name CSPScheduler

# ==============================================================================
# CSP JOB SCHEDULER
# Algoritma: Backtracking + Forward Checking
# Goal: Pure satisfaction — cari assignment valid pertama, bukan yang optimal
#
# Variables : Unit yang sedang idle/wandering
# Domain    : Job slot kosong di JobBoard (food, wood, iron)
# Constraints:
#   1. Jarak unit ke job <= PATROL_RADIUS
#   2a. Job iron: kerajaan punya kayu untuk beli pickaxe
#   2b. Job iron: kuota slot iron masih tersisa
#   2c. Job iron: ada smithy (infrastruktur besi) di kerajaan
#   3. Satu job hanya untuk satu unit dalam satu batch
# ==============================================================================

# ------------------------------------------------------------------------------
# STATE INTERNAL (dipakai selama satu sesi backtracking)
# ------------------------------------------------------------------------------

## Assignment sementara selama backtracking. Key: Unit, Value: JobBoard.Job
var _assignment: Dictionary = {}

## Sisa kuota slot iron yang boleh di-assign dalam batch ini.
## Didekremen saat assign job iron, dikembalikan saat backtrack.
var _remaining_iron_slots: int = 0


# ==============================================================================
# ENTRY POINT UTAMA
# Dipanggil dari Kingdom.tick_csp() secara periodik (~6 detik)
# ==============================================================================

## Menyelesaikan penugasan CSP untuk sekumpulan unit idle sekaligus.
## Assignment hasil CSP langsung ditulis ke job_board kerajaan dalam format
## yang identik dengan get_assignment() biasa, sehingga transparan bagi FSM unit.
func solve_job_assignments(
	kingdom,               # Kingdom — akses .wood, .active_tools, .houses, .pop, .smiths, .job_board
	idle_units: Array,     # Array[Unit] — unit dengan state "idle" atau "wandering"
	world_buildings: Array # Array[Node] — semua bangunan di dunia
) -> void:

	# --- 1. Precompute shared state ---

	# Snapshot job yang tersedia (kita tidak mau mengubah array asli selama backtracking)
	var available_jobs: Array = kingdom.job_board.available_jobs.duplicate()
	if available_jobs.is_empty():
		return

	# Hitung batas kuota iron sesuai rumus JobBoard yang sudah ada
	var max_iron_slots: int = max(3, kingdom.houses * 2 + int(kingdom.pop / 5.0))
	var cur_iron_active: int = kingdom.active_tools
	_remaining_iron_slots = max(0, max_iron_slots - cur_iron_active)

	# Cari smithy available milik kerajaan ini
	var avail_smith: Building = null
	for b in world_buildings:
		if not is_instance_valid(b) or b.is_queued_for_deletion():
			continue
		if b.kingdom == kingdom.kname and b.btype == "smith" and b.trainees < b.max_trainees:
			avail_smith = b
			break

	# Cek apakah kerajaan mampu beli pickaxe sekarang
	var can_buy_pickaxe: bool = (kingdom.wood >= Config.TOOL_COST["wood"])

	# --- 2. Order units (variable ordering) ---
	# Urutkan berdasarkan ai_think_timer ascending (nilai kecil = paling lama idle)
	var units_ordered: Array = idle_units.duplicate()
	units_ordered.sort_custom(func(a, b): return a.ai_think_timer < b.ai_think_timer)

	# --- 3. Reset state backtracking ---
	_assignment = {}

	# --- 4. Jalankan backtracking ---
	_backtrack(units_ordered, available_jobs, kingdom, avail_smith, can_buy_pickaxe)

	# --- 5. Terapkan hasil assignment ---
	if _assignment.is_empty():
		return

	for unit in _assignment:
		var job: JobBoard.Job = _assignment[unit]

		# Pindahkan job dari available ke active (sama persis seperti get_assignment())
		kingdom.job_board.available_jobs.erase(job)
		kingdom.job_board.active_jobs.append(job)
		job.assignee = unit

		# Set state unit
		unit.target_res = job.target_res
		unit.target_pos = job.target_pos
		unit.state = "moving"

		# Beli pickaxe jika dibutuhkan untuk job iron
		if job.job_type == "iron" and not unit.has_tool:
			kingdom.wood -= Config.TOOL_COST["wood"]
			unit.has_tool = true
			unit._update_texture()


# ==============================================================================
# BACKTRACKING REKURSIF
# ==============================================================================

## Inti algoritma CSP — mencoba assign unit satu per satu secara rekursif.
## Failure tolerance: unit yang tidak dapat job dilewati (tidak menyebabkan gagal total).
func _backtrack(
	units_remaining: Array,   # Sisa unit yang belum diproses
	jobs_remaining: Array,    # Sisa job yang belum diassign
	kingdom,
	avail_smith: Building,
	can_buy_pickaxe: bool
) -> bool:

	# Base case: semua unit sudah diproses (berhasil assign atau dilewati)
	if units_remaining.is_empty():
		return true

	var unit = units_remaining[0]
	var rest: Array = units_remaining.slice(1)

	# Coba setiap job di domain unit ini
	for job in jobs_remaining:
		if _is_valid(unit, job, kingdom, avail_smith, can_buy_pickaxe):

			# Tentative assign
			_assignment[unit] = job
			var new_jobs: Array = jobs_remaining.duplicate()
			new_jobs.erase(job)

			# Forward checking (bisa berupa check ringan atau agresif — lihat _forward_check)
			if _forward_check(rest, new_jobs, kingdom, avail_smith, can_buy_pickaxe):

				# Update kuota iron jika dipakai
				var needs_iron: bool = (job.job_type == "iron" and not unit.has_tool)
				if needs_iron:
					_remaining_iron_slots -= 1

				# Rekursi ke unit berikutnya
				if _backtrack(rest, new_jobs, kingdom, avail_smith, can_buy_pickaxe):
					return true

				# Backtrack: kembalikan kuota iron
				if needs_iron:
					_remaining_iron_slots += 1

			# Undo assignment sementara
			_assignment.erase(unit)

	# Failure tolerance: unit ini tidak dapat job valid apapun
	# Lewati saja dan lanjut ke unit berikutnya — jangan gagalkan seluruh batch
	return _backtrack(rest, jobs_remaining, kingdom, avail_smith, can_buy_pickaxe)


# ==============================================================================
# CONSTRAINT CHECKER
# ==============================================================================

## Memeriksa apakah pasangan (unit, job) memenuhi semua constraint CSP.
## Dipanggil untuk setiap kandidat assignment sebelum diterapkan.
func _is_valid(
	unit,       # Unit
	job,        # JobBoard.Job
	kingdom,
	avail_smith: Building,
	can_buy_pickaxe: bool
) -> bool:

	# Constraint 1: Jarak unit ke job tidak boleh melebihi PATROL_RADIUS
	# (hanya assign unit yang memang sudah dekat dengan resource)
	if unit.global_position.distance_to(job.target_pos) > Config.PATROL_RADIUS:
		return false

	# Constraint 2: Khusus job iron — unit perlu pickaxe
	if job.job_type == "iron" and not unit.has_tool:

		# Sub-constraint 2a: Kerajaan harus punya kayu untuk beli pickaxe
		if not can_buy_pickaxe:
			return false

		# Sub-constraint 2b: Kuota slot iron dalam batch ini masih tersisa
		if _remaining_iron_slots <= 0:
			return false

		# Sub-constraint 2c: Infrastruktur besi (smithy) harus eksis di kerajaan
		# Ini memastikan kita tidak assign iron tanpa ada jalur produksi militer
		if avail_smith == null and kingdom.smiths == 0:
			return false

	# Constraint 3: Job ini belum diassign ke unit lain dalam batch yang sama
	for assigned_unit in _assignment:
		if _assignment[assigned_unit] == job:
			return false

	return true


# ==============================================================================
# FORWARD CHECKING
# ==============================================================================

## Memeriksa apakah unit-unit berikutnya masih punya domain yang layak
## setelah assignment sementara diterapkan.
##
## Implementasi default: Simplified (selalu true)
## Karena failure tolerance sudah menangani unit tanpa job (mereka cukup dilewati),
## forward checking agresif tidak diperlukan dan bisa memangkas solusi valid.
##
## Untuk pruning lebih agresif, uncomment blok di bawah.
func _forward_check(
	units_ahead: Array,
	jobs_remaining: Array,
	kingdom,
	avail_smith: Building,
	can_buy_pickaxe: bool
) -> bool:

	# Default: simplified forward check — selalu lolos
	# Failure tolerance di _backtrack() sudah handle unit tanpa job
	return true

	# --- VERSI AGRESIF (opsional) ---
	# Uncomment jika ingin pruning lebih ketat. Setiap unit di depan harus
	# punya setidaknya 1 job valid (atau boleh idle — jadi return true tetap).
	#
	# for u in units_ahead:
	# 	var has_any = false
	# 	for j in jobs_remaining:
	# 		if _is_valid(u, j, kingdom, avail_smith, can_buy_pickaxe):
	# 			has_any = true
	# 			break
	# 	# has_any == false masih OK karena unit bisa idle (failure tolerance)
	# return true
