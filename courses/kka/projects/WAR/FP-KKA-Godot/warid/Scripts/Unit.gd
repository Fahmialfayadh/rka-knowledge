extends CharacterBody2D
class_name Unit

# ==============================================================================
# VARIABEL IDENTITAS & STATUS
# ==============================================================================
@export var kingdom: String = "red"
var role: String = "gatherer" # "gatherer", "builder", "defender"
var armed: bool = false
var has_tool: bool = false
@export var carry: int = 0
@export var carry_type: String = "" # "wood", "iron", "food"

var dust_particles: CPUParticles2D
var state: String = "idle"

# Hero Possession properties
var is_possessed: bool = false:
	set(value):
		is_possessed = value
		_update_texture()
		queue_redraw()
var dash_cooldown: float = 2.0
var dash_timer: float = 0.0
var slash_timer: float = 0.0
var hero_aim_dir: Vector2 = Vector2.RIGHT
var dash_hit_enemies: Array = []

# ==============================================================================
# VARIABEL ATRIBUT (STATISTIK)
# ==============================================================================
var hp: float = Config.UNIT_MAX_HP
var hp_visible_timer: float = 0.0
var current_speed: float = Config.UNIT_SPEED_MIN

var wander_timer: float = 0.0
var wander_angle: float = 0.0
var gather_timer: float = 0.0
var boids_timer: float = 0.0 # Throttle untuk fisika tabrakan
var cached_sep_dir: Vector2 = Vector2.ZERO
var attack_cooldown: float = 0.0
var train_timer: float = 0.0
var help_cooldown: float = 0.0
var ai_think_timer: float = 0.0 # Throttle: unit berpikir setiap 0.3 detik, bukan setiap frame
var starved: bool = false

# ==============================================================================
# VARIABEL TARGET & NAVIGASI
# ==============================================================================
var target_pos: Vector2 = Vector2.ZERO
var target_unit: Unit = null
var target_res: GameResource = null
var target_building: Building = null

@onready var sprite = $Sprite2D

# Referensi eksternal (diinjeksi oleh World/Main)
var my_kingdom = null
var enemy_kingdom = null
var world_units: Array[Node]:
	get:
		var w = get_tree().current_scene
		return w.all_units if w else []

var world_buildings: Array[Node]:
	get:
		var w = get_tree().current_scene
		return w.all_buildings if w else []

func _ready() -> void:
	add_to_group("units")
	add_to_group(kingdom + "_units")
	current_speed = randf_range(Config.UNIT_SPEED_MIN, Config.UNIT_SPEED_MAX)
	ai_think_timer = randf_range(0.0, 0.5) # Offset acak diperbesar (0.5 detik)
	
	# Matikan Fisika Batu (tidak dipakai, kita gerak manual)
	collision_layer = 0
	collision_mask = 0
	
	# Setup Partikel Debu
	dust_particles = CPUParticles2D.new()
	dust_particles.emitting = false
	dust_particles.amount = 8
	dust_particles.lifetime = 0.4
	dust_particles.gravity = Vector2(0, -15) # Menguap ke atas
	dust_particles.initial_velocity_min = 5.0
	dust_particles.initial_velocity_max = 10.0
	dust_particles.scale_amount_min = 2.0
	dust_particles.scale_amount_max = 5.0
	dust_particles.color = Color(0.6, 0.6, 0.5, 0.4) # Warna debu transparan
	dust_particles.z_index = -1 # Di bawah sprite karakter
	dust_particles.position = Vector2(0, 5) # Di kaki karakter
	add_child(dust_particles)
	
	_update_texture()

# ==============================================================================
# HP BAR via _draw() — DIJAMIN MUNCUL karena langsung menggambar piksel
# ==============================================================================
func _draw():
	if not visible or hp_visible_timer <= 0 or not SettingsManager.show_hp_bar:
		return
		
	# Hitung tingkat kepudaran (Alpha)
	var alpha = 1.0
	if hp_visible_timer < 0.5:
		alpha = hp_visible_timer / 0.5 # Memudar perlahan di 0.5 detik terakhir
		
	var inv_scale = 1.0 / scale.x if scale.x > 0 else 1.0
	# Dikecilkan ukurannya jadi 18x3
	var bar_w = 18.0 * inv_scale
	var bar_h = 3.0 * inv_scale
	var bar_x = -bar_w / 2.0
	var bar_y = -30.0 * inv_scale # Agak naik sedikit
	
	# 1. Outline Hitam Solid (Gaya Retro)
	var out_w = bar_w + 2.0 * inv_scale
	var out_h = bar_h + 2.0 * inv_scale
	draw_rect(Rect2(bar_x - inv_scale, bar_y - inv_scale, out_w, out_h), Color(0.0, 0.0, 0.0, alpha))
	
	# 2. Background Merah Gelap (Daging kosong)
	draw_rect(Rect2(bar_x, bar_y, bar_w, bar_h), Color(0.3, 0.0, 0.0, alpha))
	
	# 3. Foreground (Nyawa)
	var ratio = clamp(hp / Config.UNIT_MAX_HP, 0.0, 1.0)
	if ratio > 0:
		var fg_color = Color.GREEN if ratio > 0.5 else (Color.YELLOW if ratio > 0.25 else Color.RED)
		fg_color.a = alpha
		draw_rect(Rect2(bar_x, bar_y, bar_w * ratio, bar_h), fg_color)
		
	# Indikator Pasukan (Defenders) agar kelihatan dari jauh
	if armed and hp > 0 and not is_possessed:
		var top_y = -20.0 * inv_scale
		var pts = PackedVector2Array([
			Vector2(-4.0 * inv_scale, top_y - 8.0 * inv_scale),
			Vector2(4.0 * inv_scale, top_y - 8.0 * inv_scale),
			Vector2(0, top_y)
		])
		var ind_color = Color(1.0, 0.3, 0.3) if kingdom == "red" else Color(0.3, 0.6, 1.0)
		draw_polygon(pts, PackedColorArray([ind_color]))
		# Garis tepi agar tegas
		draw_polyline(PackedVector2Array([Vector2(-4.0 * inv_scale, top_y - 8.0 * inv_scale), Vector2(4.0 * inv_scale, top_y - 8.0 * inv_scale), Vector2(0, top_y), Vector2(-4.0 * inv_scale, top_y - 8.0 * inv_scale)]), Color.BLACK, 1.0 * inv_scale)
		
	# 4. Hero Aura & Cooldown
	if is_possessed:
		# Draw glowing base (lingkaran cahaya di kaki)
		draw_circle(Vector2(0, 10.0), 35.0, Color(1, 0.8, 0, 0.4))
		draw_arc(Vector2(0, 10.0), 35.0, 0, TAU, 32, Color(1, 0.8, 0, 0.9), 4.0)
		
		# Draw pointer arrow ke arah hero_aim_dir
		draw_line(Vector2(0, 10.0), Vector2(0, 10.0) + hero_aim_dir * 50.0, Color(1, 0.2, 0.2, 0.8), 4.0)
		
		# Arrow Indicator di atas unit
		var bounce = sin(Time.get_ticks_msec() * 0.005) * 5.0
		var arrow_pts = PackedVector2Array([
			Vector2(-8, -45 + bounce),
			Vector2(8, -45 + bounce),
			Vector2(0, -35 + bounce)
		])
		draw_polygon(arrow_pts, PackedColorArray([Color.GREEN, Color.GREEN, Color.GREEN]))
		draw_polyline(PackedVector2Array([Vector2(-8, -45 + bounce), Vector2(8, -45 + bounce), Vector2(0, -35 + bounce), Vector2(-8, -45 + bounce)]), Color.BLACK, 2.0)

		
		var cd_ratio = 1.0 - clamp(dash_timer / dash_cooldown, 0.0, 1.0)
		draw_rect(Rect2(bar_x, bar_y + 6.0 * inv_scale, bar_w, 4.0 * inv_scale), Color(0.2, 0.2, 0.2, 0.8))
		draw_rect(Rect2(bar_x, bar_y + 6.0 * inv_scale, bar_w * cd_ratio, 4.0 * inv_scale), Color(0.0, 0.8, 1.0, 0.8))

func _update_texture():
	if is_possessed:
		if armed:
			if kingdom == "red":
				sprite.texture = preload("res://Asset/Sprites/armored_Red_posses.png")
			else:
				sprite.texture = preload("res://Asset/Sprites/armored_blue_posses.png")
		else:
			if kingdom == "red":
				if has_tool:
					sprite.texture = preload("res://Asset/Sprites/iron_worker_red_posses.png")
				else:
					sprite.texture = preload("res://Asset/Sprites/redpeople_posses.png")
			else:
				if has_tool:
					sprite.texture = preload("res://Asset/Sprites/iron_worker_blue_posses.png")
				else:
					sprite.texture = preload("res://Asset/Sprites/bluepeople_posses.png")
	else:
		if armed:
			if kingdom == "red":
				sprite.texture = preload("res://Asset/Sprites/armored_Red.png")
			else:
				sprite.texture = preload("res://Asset/Sprites/armored_blue.png")
		else:
			if kingdom == "red":
				if has_tool:
					sprite.texture = preload("res://Asset/Sprites/iron_worker_red.png")
				else:
					sprite.texture = preload("res://Asset/Sprites/redpeople.png")
			else:
				if has_tool:
					sprite.texture = preload("res://Asset/Sprites/iron_worker_blue.png")
				else:
					sprite.texture = preload("res://Asset/Sprites/bluepeople.png")

# ==============================================================================
# FUNGSI UTAMA (GAME LOOP)
# ==============================================================================
func _physics_process(delta: float) -> void:
	if is_possessed:
		_tick_hero(delta)
		return
		
	if hp_visible_timer > 0:
		hp_visible_timer -= delta
		queue_redraw() # Hanya redraw saat HP bar sedang aktif (hemat performa!)
	if hp <= 0:
		# Jika mati, tidak langsung hilang, tapi pudar ke atas
		if not is_queued_for_deletion() and not has_meta("dying"):
			set_meta("dying", true)
			collision_layer = 0
			collision_mask = 0
			
			if target_building and is_instance_valid(target_building) and target_building.btype == "smith" and state in ["going_to_smith", "training"]:
				target_building.trainees = max(0, target_building.trainees - 1)
				target_building = null
			my_kingdom.job_board.release_unit_jobs(self)
			
			AudioManager.play_sfx("die")
			EventBus.spawn_blood_stain(global_position) # Bercak darah permanen di tanah!
			EventBus.shake_camera.emit(1.5, 0.1) # Getaran layar saat musuh tumbang
			
			# Animasi Roh (Death Fade)
			var tween = create_tween()
			tween.tween_property(sprite, "modulate:a", 0.0, 1.0)
			tween.parallel().tween_property(self, "global_position", global_position + Vector2(0, -30), 1.0)
			tween.tween_callback(queue_free)
		return
		
	# Pastikan referensi sudah di-set oleh World
	if my_kingdom == null or enemy_kingdom == null:
		return
		
	_handle_starvation(delta)
	
	if help_cooldown > 0:
		help_cooldown -= delta
		
	if attack_cooldown > 0:
		attack_cooldown -= delta
		
	if hp <= 0:
		return # Hentikan eksekusi jika mati kelaparan
	
	var bx = my_kingdom.base_pos.x
	var by = my_kingdom.base_pos.y
		
	# ================================================================
	# SURVIVAL MODE — semua unit kumpul di base (Python L417-431)
	# ================================================================
	if my_kingdom.survival_mode and state not in ["survival", "training", "going_to_smith"]:
		state = "survival"
		carry = 0
		carry_type = ""
		target_res = null
		my_kingdom.job_board.release_unit_jobs(self)
		target_pos = my_kingdom.base_pos + Vector2(randf_range(-30, 30), randf_range(-30, 30))
	
	# ================================================================
	# BASE UNDER ATTACK — soldier override ke defend_base (Python L436-449)
	# ================================================================
	if my_kingdom.base_under_attack and armed:
		if state not in ["defending_base", "training"]:
			var dist_to_home = global_position.distance_to(my_kingdom.base_pos)
			var is_chasing_armed = (state == "chasing" and target_unit != null and is_instance_valid(target_unit) and target_unit.armed)
			var is_near_home = (dist_to_home <= Config.BASE_DANGER_RADIUS + 40)
			
			if state == "chasing" and (is_chasing_armed or is_near_home):
				pass # Boleh lanjut kejar
			else:
				state = "defending_base"
				target_unit = null
				target_pos = my_kingdom.base_pos + Vector2(randf_range(-40, 40), randf_range(-40, 40))
	
	# ================================================================
	# CALL TO ARMS (Militia): Pekerja drop resource & lari ke base (Python L454-462)
	# ================================================================
	if my_kingdom.base_under_attack and not armed:
		if state not in ["defending_base", "training", "going_to_smith", "chasing", "fleeing", "survival"]:
			carry = 0
			carry_type = ""
			target_res = null
			my_kingdom.job_board.release_unit_jobs(self)
			state = "defending_base"
			target_pos = my_kingdom.base_pos + Vector2(randf_range(-40, 40), randf_range(-40, 40))
	
	# ================================================================
	# PASSIVE FLEEING: Worker lari dari armed enemy (Python L467-481)
	# ================================================================
	# AI Throttle: Hanya scan musuh setiap 0.3 detik (bukan 60× per detik!)
	ai_think_timer -= delta
	if ai_think_timer <= 0:
		ai_think_timer = 0.5 # Reset timer (diperlambat dari 0.3)
		_handle_passive_fleeing()
	
	# ================================================================
	# SOLDIER/MILITIA PATROL SCAN di PATROL_RADIUS (Python L486-499)
	# ================================================================
	# Scan ini juga hanya dijalankan saat ai_think_timer habis (sudah di-throttle di atas)
	if ai_think_timer <= 0.01: # Masih di frame yang sama dengan throttle di atas
		var is_militia = (not armed and state == "defending_base")
		# Prajurit (Armed) sekarang BISA memindai musuh meski sedang memotong kayu (moving/gathering/returning)
		if (armed or is_militia) and state not in ["chasing", "attacking", "training", "fleeing"]:
			var enemy_in_range = _nearest_enemy_in_radius(Config.PATROL_RADIUS)
			
			if enemy_in_range:
				var dist_to_home = global_position.distance_to(my_kingdom.base_pos)
				if my_kingdom.base_under_attack and state == "defending_base" and dist_to_home > Config.BASE_DANGER_RADIUS + 40:
					if not enemy_in_range.armed:
						enemy_in_range = null
					
			if enemy_in_range:
				target_unit = enemy_in_range
				state = "chasing"
	
	_update_state_machine(delta)
	
	# Balik arah sprite (hadap kiri/kanan) berdasarkan pergerakan
	if velocity.length() > 5.0 and not has_meta("dying"):
		if velocity.x < 0:
			sprite.flip_h = true
		elif velocity.x > 0:
			sprite.flip_h = false
			
		# Animasi Jalan (Squash & Stretch)
		var speed_factor = current_speed / Config.UNIT_SPEED_MIN
		var t = Time.get_ticks_msec() * 0.015 * speed_factor
		
		# Melompat kecil (hanya nilai negatif karena Godot sumbu Y positif ke bawah)
		sprite.position.y = -abs(sin(t)) * 5.0
		
		# Efek membal (memendek-melebar dan memanjang-menyempit)
		var squash = sin(t * 2.0) * 0.15
		sprite.scale = Vector2(1.0 + squash, 1.0 - squash)
		
	if velocity.length_squared() > 0.1:
		sprite.rotation = 0 # Matikan rotasi geleng-geleng
		if dust_particles: dust_particles.emitting = true
	else:
		sprite.rotation = 0
		sprite.scale = Vector2.ONE # Kembali ke ukuran normal saat berhenti
		sprite.position.y = 0
		if dust_particles: dust_particles.emitting = false
		
	# Pergerakan manual (WorldBox-style, tanpa physics engine)
	var prev_pos = global_position
	global_position += velocity * delta
	
	# Batasan Area Gunung (Wavy Boundary)
	var mountain_y = Config.get_mountain_bound(global_position.x)
	if global_position.y < mountain_y:
		global_position.y = mountain_y

	# Obstacle Hard Collision (Slide & Block)
	var w = get_tree().current_scene
	if w and "obstacles" in w:
		for obs in w.obstacles:
			if is_instance_valid(obs):
				if obs.get("depleted") == true:
					continue
				if obs.has_meta("boids_type") and obs.get_meta("boids_type") == "water":
					continue
				var rad = obs.get_meta("avoid_radius") if obs.has_meta("avoid_radius") else 50.0
				var hit_rad = rad * 0.7
				var dist_prev = prev_pos.distance_to(obs.global_position)
				var dist_curr = global_position.distance_to(obs.global_position)
				
				# Mencegah pergerakan mendekati pusat rintangan jika berada dalam hit_rad
				if dist_curr < hit_rad:
					if dist_curr < dist_prev:
						if dist_prev >= hit_rad:
							var push = (global_position - obs.global_position).normalized()
							global_position = obs.global_position + push * hit_rad
						else:
							# Meluncur menyamping jika berada di dalam (proyeksi tangen) agar tidak stuck
							var normal = (global_position - obs.global_position).normalized()
							if dist_curr == 0:
								normal = Vector2(randf_range(-1, 1), randf_range(-1, 1)).normalized()
							var movement = global_position - prev_pos
							var dot = movement.dot(normal)
							if dot < 0:
								global_position = prev_pos + (movement - normal * dot)

# ==============================================================================
# STATE MACHINE (MESIN KECERDASAN)
# ==============================================================================
func _update_state_machine(delta: float):
	if state == "idle":
		velocity = Vector2.ZERO
		_idle_decision()
		
	elif state == "wandering":
		_tick_wander(delta)
		
	elif state in ["moving", "returning", "attacking", "going_to_smith", "patrolling"]:
		# Update target posisi dinamis
		if state == "attacking" and target_unit != null:
			if target_unit.hp > 0 and target_unit.visible: 
				target_pos = target_unit.global_position
			else: 
				state = "idle"
				target_unit = null
				return
		
		# Terapkan algoritma pergerakan rombongan (Boids)
		_move_toward_target_boids(delta)
		
		var arrival_dist = 20.0 # Batas toleransi standar
		if state in ["going_to_smith", "returning", "attacking"]:
			arrival_dist = 45.0 # Bangunan berukuran besar, toleransi jarak jauh agar tidak nyangkut
			
		if global_position.distance_to(target_pos) < arrival_dist:
			_arrive_at_target()
			
	elif state == "gathering":
		velocity = Vector2.ZERO
		gather_timer -= delta
		if gather_timer <= 0:
			if target_res and not target_res.depleted:
				AudioManager.play_sfx("chop")
				EventBus.spawn_floating_text(global_position, "+1", Color.GREEN)
				_play_squash_anim()
				
				target_res.deplete()
				carry_type = target_res.rtype
				carry = Config.RESOURCE_CARRY_AMT
				my_kingdom.job_board.release_unit_jobs(self)
				target_res = null
			state = "returning"
			target_pos = my_kingdom.base_pos + Vector2(randf_range(-30, 30), randf_range(-30, 30))
			
	# Blok kode going_to_smith yang tidak terpakai sudah dihapus
			
	elif state == "training":
		velocity = Vector2.ZERO
		train_timer -= delta
		if train_timer <= 0:
			if target_building:
				target_building.trainees -= 1
			armed = true
			hp = Config.ARMED_MAX_HP # Langsung sembuh dan darah jadi 3x lipat
			current_speed += 5.0 # Militer lebih cepat 5 unit kecepatan
			_update_texture()
			state = "idle"
			has_tool = false
			visible = true # Muncul kembali dari dalam bangunan!
			# Beri efek lompat keluar
			global_position += Vector2(randf_range(-20, 20), randf_range(10, 30))
			visible = true # Muncul kembali ke permukaan
			
			# Efek Pop-out saat selesai training
			var target_scale = scale
			scale = Vector2.ZERO
			var tween = create_tween()
			tween.tween_property(self, "scale", target_scale, 0.5).set_trans(Tween.TRANS_ELASTIC).set_ease(Tween.EASE_OUT)
			EventBus.spawn_hit_particles(global_position + Vector2(0, 10), Color.WEB_GRAY)
			
	elif state == "chasing":
		if target_unit == null or target_unit.hp <= 0 or not target_unit.visible:
			state = "idle"
			target_unit = null
		else:
			target_pos = target_unit.global_position
			_move_toward_target_boids(delta)
			
			if global_position.distance_to(target_pos) < 30.0: # Jarak serang HARUS lebih besar dari boids separation (20px)
				_combat_attack()

	elif state == "defending_base":
		if not my_kingdom.base_under_attack:
			state = "idle"
			return
			
		var threat = _nearest_armed_enemy()
		if threat and threat.global_position.distance_to(my_kingdom.base_pos) <= Config.BASE_DANGER_RADIUS + 30.0:
			if armed:
				target_unit = threat
				state = "chasing"
			else:
				# Pekerja biasa minta tolong tentara sesungguhnya
				if help_cooldown <= 0:
					_call_for_help(threat)
					help_cooldown = 2.0
					
				_move_toward_target_boids(delta)
				if global_position.distance_to(target_pos) < 15.0:
					target_pos = my_kingdom.base_pos + Vector2(randf_range(-30, 30), randf_range(-30, 30))
		else:
			_move_toward_target_boids(delta)
			if global_position.distance_to(target_pos) < 15.0:
				target_pos = my_kingdom.base_pos + Vector2(randf_range(-40, 40), randf_range(-40, 40))
				
	elif state == "fleeing":
		_move_toward_target_boids(delta)
		if global_position.distance_to(target_pos) < 15.0:
			state = "idle"
		
	elif state == "survival":
		_move_toward_target_boids(delta)
		if global_position.distance_to(target_pos) < 15.0:
			# Sudah di base, patroli kecil (Python L428-430)
			target_pos = my_kingdom.base_pos + Vector2(randf_range(-35, 35), randf_range(-35, 35))

# ==============================================================================
# LOGIKA KEPUTUSAN (AI BRAIN)
# ==============================================================================
func _idle_decision():
	# 1. Prajurit Bersenjata (Armed)
	if armed:
		var rad = Config.AGGRESSION_RADIUS if _in_enemy_territory() else Config.PATROL_RADIUS
		var enemy = _nearest_enemy_in_radius(rad)
		if enemy:
			target_unit = enemy
			state = "chasing"
			return
			
		# Mode pengepungan (Siege / Assault)
		if my_kingdom.u_attack >= Config.UTILITY_ATTACK_THRESHOLD:
			var enemies = []
			for e in world_units:
				if not is_instance_valid(e) or e.is_queued_for_deletion(): continue
				if e.kingdom != kingdom and e.hp > 0:
					enemies.append(e)
					
			var unprotected_enemies = []
			for e in enemies:
				var is_protected = false
				if enemy_kingdom.base_node and is_instance_valid(enemy_kingdom.base_node) and enemy_kingdom.base_node.hp > 0:
					if e.global_position.distance_to(enemy_kingdom.base_pos) <= 35.0:
						is_protected = true
				if not is_protected:
					unprotected_enemies.append(e)
					
			if unprotected_enemies.size() > 0:
				# Kejar musuh yang paling lemah (HP terendah)
				var weakest = unprotected_enemies[0]
				for e in unprotected_enemies:
					if e.hp < weakest.hp:
						weakest = e
				target_unit = weakest
				state = "chasing"
			else:
				# Tidak ada musuh terproteksi, serang bangunan biasa (non-base) dulu
				var ek_buildings = []
				for b in world_buildings:
					if not is_instance_valid(b) or b.is_queued_for_deletion(): continue
					if b.kingdom != kingdom and b.hp > 0 and b.btype != "base":
						ek_buildings.append(b)
						
				if not ek_buildings.is_empty():
					target_building = ek_buildings[randi() % ek_buildings.size()]
					target_pos = target_building.global_position
					state = "attacking"
				else:
					# Semua bangunan biasa hancur, saatnya serang Markas Utama!
					if enemy_kingdom.base_node != null and enemy_kingdom.base_node.hp > 0:
						target_building = enemy_kingdom.base_node
						target_pos = target_building.global_position
					else:
						target_pos = enemy_kingdom.base_pos
					state = "attacking"
			return
			
		# [MODIFIKASI] Daripada berpatroli pasif, biarkan Prajurit bekerja!
		# Kita tidak menggunakan 'return' di sini, sehingga logika akan jatuh (fall-through) 
		# ke bawah, membuat mereka mengambil tugas layaknya pekerja biasa.
		pass
		
	# 2. Pekerja (Unarmed) & Prajurit Part-Time (Armed)
	if carry > 0:
		state = "returning"
		target_pos = my_kingdom.base_pos + Vector2(randf_range(-30, 30), randf_range(-30, 30))
		return
		
	# Cek apakah pangkalan diserang (Call to Arms / Militia)
	if my_kingdom.base_under_attack:
		state = "defending_base"
		# [FIX] Beri sedikit acak posisi agar 300 unit tidak berkumpul di 1 piksel yang bikin Boids meledak!
		target_pos = my_kingdom.base_pos + Vector2(randf_range(-60, 60), randf_range(-60, 60))
		return
		
	# Khusus Defender, jika aman, patroli di base
	if role == "defender" and my_kingdom.base_under_attack:
		state = "defending_base"
		# Scatter juga untuk para defender agar tidak menumpuk
		target_pos = my_kingdom.base_pos + Vector2(randf_range(-50, 50), randf_range(-50, 50))
		return
		
	# Khusus Builder, jika punya uang, bangun sesuatu!
	if role == "builder":
		if my_kingdom.wood >= Config.HOUSE_COST["wood"] or (my_kingdom.wood >= Config.SMITH_COST["wood"] and my_kingdom.iron >= Config.SMITH_COST["iron"]):
			var world = get_tree().current_scene
			if world.has_method("_try_build"):
				world._try_build(kingdom)
				
	# Masuk blacksmith kalau ada slot dan kingdom butuh militer
	var mil_ratio = float(my_kingdom.armed) / float(max(1, my_kingdom.pop))
	if my_kingdom.smiths > 0 and mil_ratio < Config.UTILITY_MILITARY_CAP_RATIO:
		var avail_smith: Building = null
		for b in world_buildings:
			if not is_instance_valid(b) or b.is_queued_for_deletion(): continue
			if b.kingdom == kingdom and b.btype == "smith" and b.trainees < b.max_trainees:
				avail_smith = b
				break
		if avail_smith != null and randf() < 0.8:
			avail_smith.trainees += 1
			target_building = avail_smith
			target_pos = avail_smith.global_position + Vector2(randf_range(-30, 30), randf_range(-30, 30))
			state = "going_to_smith"
			return
			
	# Cari tugas di papan kerajaan (berlaku untuk semua role jika tidak ada aktivitas lain)
	var job = my_kingdom.job_board.get_assignment(self, my_kingdom)
	if job:
		target_res = job.target_res
		target_pos = job.target_pos
		state = "moving"
		return
		
	# Tidak ada tugas, jalan-jalan
	_start_wander()

# ==============================================================================
# PERGERAKAN (MENIRU PYTHON GARIS LURUS)
# ==============================================================================
func _update_boids(delta: float):
	boids_timer -= delta
	if boids_timer <= 0:
		boids_timer = 0.3
		var sep_dir = Vector2.ZERO
		var count = 0
		
		var world = get_tree().current_scene
		if world:

			# AVOID OBSTACLES (TANGENTIAL STEERING FIX)
			if "obstacles" in world:
				var my_target_dir = Vector2.ZERO
				if target_pos != Vector2.ZERO:
					my_target_dir = (target_pos - global_position).normalized()
				else:
					my_target_dir = velocity.normalized()
					
				for obs in world.obstacles:
					if is_instance_valid(obs):
						if obs.get("depleted") == true:
							continue
						if obs.has_meta("boids_type") and obs.get_meta("boids_type") == "water":
							continue
						var obs_rad = obs.get_meta("avoid_radius") if obs.has_meta("avoid_radius") else 50.0
						var d = global_position.distance_to(obs.global_position)
						
						if d < obs_rad:
							var push_dir = (global_position - obs.global_position).normalized()
							
							# Gaya menyamping (tangential) agar tidak stuck/bingung
							var tangent = Vector2(-push_dir.y, push_dir.x)
							
							# Pilih jalur menyamping yang searah dengan tujuan akhir
							if tangent.dot(my_target_dir) < 0:
								tangent = -tangent
								
							# Gabungkan tolakan (push_dir) dengan geseran (tangent)
							var avoid_force = (push_dir * 1.0 + tangent * 2.5).normalized()
							
							sep_dir += avoid_force * ((obs_rad * 3.0) / max(d, 1.0))
							count += 1
					
		if count > 0:
			cached_sep_dir = (sep_dir / count).normalized() * 2.5 # Perbesar kekuatan dorongan boids
		else:
			cached_sep_dir = Vector2.ZERO

func _move_toward_target_boids(delta: float):
	var speed_mult = 1.0
	if my_kingdom.is_starving:
		speed_mult *= 0.7
		
	speed_mult *= _get_water_speed_modifier()
		
	var to_target = (target_pos - global_position).normalized()
	_update_boids(delta)
	velocity = (to_target + cached_sep_dir).normalized() * (current_speed * speed_mult)

func _get_water_speed_modifier() -> float:
	var w = get_tree().current_scene
	if w and "obstacles" in w:
		for obs in w.obstacles:
			if is_instance_valid(obs) and obs.has_meta("boids_type") and obs.get_meta("boids_type") == "water":
				var rad = obs.get_meta("avoid_radius") if obs.has_meta("avoid_radius") else 130.0
				if global_position.distance_to(obs.global_position) < rad * 0.9:
					return 0.3
	return 1.0

func _tick_wander(delta: float):
	wander_timer -= delta
	if wander_timer <= 0:
		wander_timer = randf_range(Config.WANDER_CHANGE - 0.5, Config.WANDER_CHANGE + 0.5)
		wander_angle += randf_range(-PI/2, PI/2)
		
	var wander_dir = Vector2(cos(wander_angle), sin(wander_angle))
	
	# Jangan keluar terlalu jauh, tapi juga JANGAN terlalu dekat dengan markas agar tidak numpuk!
	var dist_to_base = global_position.distance_to(my_kingdom.base_pos)
	if dist_to_base > 200.0: # Perluas radius pedesaan
		var back_to_base = (my_kingdom.base_pos - global_position).normalized()
		wander_dir = (wander_dir + back_to_base * 2.0).normalized()
	elif dist_to_base < 80.0: # Terlalu sumpek di tengah markas
		var push_out = (global_position - my_kingdom.base_pos).normalized()
		wander_dir = (wander_dir + push_out * 2.5).normalized()
		
	_update_boids(delta)
	
	# Tambahkan daya dorong antar-unit saat menganggur
	var speed_mult = _get_water_speed_modifier()
	velocity = (wander_dir + cached_sep_dir * 1.5).normalized() * (Config.WANDER_SPEED * 0.5 * speed_mult)

	# Batal wander jika ada tugas
	if not armed and my_kingdom.job_board.available_jobs.size() > 0:
		state = "idle"
		return
		
	# Penciuman Sumber Daya Bawaan (SMELL RADIUS)
	if not armed:
		var best_d = Config.SMELL_RADIUS
		var best_r = null
		var world = get_tree().current_scene
		if world and world.has_node("Resources"):
			for r in world.get_node("Resources").get_children():
				if not r.depleted:
					var d = global_position.distance_to(r.global_position)
					if d < best_d:
						best_d = d
						best_r = r
		if best_r:
			target_res = best_r
			target_pos = best_r.global_position
			state = "moving"
			return

func _start_wander():
	state = "wandering"
	wander_timer = randf_range(Config.WANDER_CHANGE - 0.5, Config.WANDER_CHANGE + 0.5)
	wander_angle = randf() * PI * 2

# ==============================================================================
# LOGIKA KETIBAAN & INTERAKSI (ARRIVAL & COMBat)
# ==============================================================================
func _arrive_at_target():
	if state == "moving":
		if target_res and not target_res.depleted:
			state = "gathering"
			gather_timer = 1.0 # Butuh 1 detik untuk menambang
		else:
			my_kingdom.job_board.release_unit_jobs(self)
			state = "idle"
			
	elif state == "returning":
		if carry_type == "wood": my_kingdom.wood += carry
		elif carry_type == "iron": my_kingdom.iron += carry
		elif carry_type == "food": my_kingdom.food += carry
		
		carry = 0
		carry_type = ""
		my_kingdom.job_board.release_unit_jobs(self)
		state = "idle"
		
		# Setelah menyerahkan sumber daya, coba bangun sesuatu (sama seperti Python)
		var world = get_tree().current_scene
		if world and world.has_method("_try_build"):
			world._try_build(kingdom)
		
	elif state == "going_to_smith":
		if target_building and target_building.hp > 0:
			state = "training"
			train_timer = 20.0 # Waktu training dikembalikan normal
			visible = false # MENGHILANG agar tidak jadi perisai daging!
		else:
			state = "idle"
			
	elif state == "attacking":
		if attack_cooldown > 0:
			return # Tunggu cooldown habis
			
		attack_cooldown = 0.5
		
		# Animasi hit memantul sederhana tapi bukan mengubah global_position tiap frame
		var bounce_dir = (global_position - target_pos).normalized()
		var tw = create_tween()
		var orig = sprite.position
		tw.tween_property(sprite, "position", bounce_dir * 8.0, 0.1)
		tw.tween_property(sprite, "position", orig, 0.1)
		
		AudioManager.play_sfx("hit")
		
		if target_building:
			if target_building.hp > 0:
				target_building.take_damage(Config.UNIT_ATTACK_DAMAGE)
				if target_building.hp <= 0:
					EventBus.log_event.emit("Building destroyed!", kingdom)
					state = "idle"
					target_building = null
			else:
				state = "idle"
				target_building = null
		else:
			# Menyerang Base musuh langsung
			if enemy_kingdom.base_node and enemy_kingdom.base_node.hp > 0:
				enemy_kingdom.base_node.take_damage(Config.UNIT_ATTACK_DAMAGE)
				if enemy_kingdom.base_node.hp <= 0:
					EventBus.log_event.emit("Base Shield DESTROYED!", kingdom)
					state = "idle"
			else:
				state = "idle"
				
	elif state == "patrolling":
		state = "idle"

func _combat_attack():
	if attack_cooldown <= 0:
		attack_cooldown = 0.3 if armed else 0.5 # Prajurit terlatih menebas jauh lebih cepat!
		var dmg = Config.ARMED_ATTACK_DAMAGE if armed else 1.0 # Pekerja punya damage 1.0
		
		AudioManager.play_sfx("hit")
		_play_squash_anim()
		
		# Brutal Combat Animation (Wind-up, Slash, Jump)
		var dash_dir = (target_unit.global_position - global_position).normalized()
		var original_pos = sprite.position
		var tween = create_tween()
		
		# 1. Wind-up (Tarik badan ke belakang sedikit dan rotasi)
		tween.tween_property(sprite, "position", -dash_dir * 4.0, 0.1)
		tween.parallel().tween_property(sprite, "rotation", -0.4 * sign(dash_dir.x), 0.1)
		
		# 2. Slash (Lompat dan tebas ke depan)
		EventBus.spawn_dash_slash_vfx(global_position, dash_dir)
		tween.tween_property(sprite, "position", dash_dir * 14.0 + Vector2(0, -6.0), 0.05)
		tween.parallel().tween_property(sprite, "rotation", 0.5 * sign(dash_dir.x), 0.05)
		
		# 3. Kembali ke pose awal
		tween.tween_property(sprite, "position", original_pos, 0.15)
		tween.parallel().tween_property(sprite, "rotation", 0.0, 0.15)
		
		# Tambahan efek visual tebasan (Slash) putih menggunakan Hit Particles
		EventBus.spawn_hit_particles(target_unit.global_position + Vector2(0, -10), Color.WHITE)
		
		# HAPUS Physical Knockback karena bikin bug ngadet / ngelag! 
		# (Animasi Tween saja sudah cukup untuk memberikan efek impact)
		
		target_unit.take_damage(dmg)
		
		if target_unit.hp <= 0:
			EventBus.log_event.emit("Enemy killed!", kingdom)
			state = "idle"
			target_unit = null

# ==============================================================================
# LOGIKA KELAPARAN & KETAKUTAN
# ==============================================================================
func _handle_starvation(delta: float):
	if my_kingdom.is_starving:
		hp -= 0.05 * delta
		hp_visible_timer = 2.0
		queue_redraw() # Refresh HP bar
		if hp <= 0:
			starved = true

func _call_for_help(threat: Unit):
	var best_soldier: Unit = null
	var best_dist = Config.HELP_REQUEST_RADIUS * Config.HELP_REQUEST_RADIUS
	# SPATIAL GRID: Hanya cari tentara sekawan dalam radius bantuan
	var world = get_tree().current_scene
	if world and world.has_method("get_units_near"):
		var nearby = world.get_units_near(global_position, Config.HELP_REQUEST_RADIUS)
		for u in nearby:
			if u.kingdom == kingdom and u.armed and u.state not in ["training", "chasing", "defending_base"]:
				var d = global_position.distance_squared_to(u.global_position)
				if d < best_dist:
					best_dist = d
					best_soldier = u
	if best_soldier:
		best_soldier.target_unit = threat
		best_soldier.state = "chasing"

func _handle_passive_fleeing():
	if not armed and state not in ["fleeing", "training", "going_to_smith", "survival", "defending_base", "chasing"]:
		var threat = _nearest_armed_enemy()
		if threat and global_position.distance_to(threat.global_position) <= Config.FLEE_RADIUS:
			carry = 0
			carry_type = ""
			target_res = null
			my_kingdom.job_board.release_unit_jobs(self)
			state = "fleeing"
			target_pos = my_kingdom.base_pos + Vector2(randf_range(-25, 25), randf_range(-25, 25))
			if help_cooldown <= 0:
				_call_for_help(threat)
				help_cooldown = 5.0

# ==============================================================================
# BANTUAN DETEKSI LINGKUNGAN
# ==============================================================================
func _nearest_enemy_in_radius(radius: float) -> Unit:
	var best = null
	var best_dist = radius * radius
	# SPATIAL GRID: Hanya cek unit di kotak-kotak terdekat, bukan seluruh dunia!
	var world = get_tree().current_scene
	if world and world.has_method("get_units_near"):
		var nearby = world.get_units_near(global_position, radius)
		for u in nearby:
			if u.kingdom != kingdom and u.visible:
				var d = global_position.distance_squared_to(u.global_position)
				if d < best_dist:
					best_dist = d
					best = u
	return best

func _nearest_armed_enemy() -> Unit:
	var best = null
	var best_dist = Config.FLEE_RADIUS * Config.FLEE_RADIUS
	# SPATIAL GRID: Hanya cek unit dalam jangkauan FLEE_RADIUS
	var world = get_tree().current_scene
	if world and world.has_method("get_units_near"):
		var nearby = world.get_units_near(global_position, Config.FLEE_RADIUS)
		for u in nearby:
			if u.kingdom != kingdom and u.armed:
				var d = global_position.distance_squared_to(u.global_position)
				if d < best_dist:
					best_dist = d
					best = u
	return best

func _in_enemy_territory() -> bool:
	# Python: d_enemy < d_own (lebih dekat ke musuh = di wilayah musuh)
	var d_own = global_position.distance_to(my_kingdom.base_pos)
	var d_enemy = global_position.distance_to(enemy_kingdom.base_pos)
	return d_enemy < d_own

# ==============================================================================
# HERO MODE
# ==============================================================================
func _tick_hero(delta: float):
	if hp_visible_timer > 0:
		hp_visible_timer -= delta
		
	if hp <= 0:
		is_possessed = false
		sprite.scale = Vector2.ONE
		return
		
	# Bikin pahlawan terlihat besar dan berdenyut
	var pulse = 1.3 + sin(Time.get_ticks_msec() * 0.01) * 0.1
	sprite.scale = Vector2(pulse, pulse)
	
	if dash_timer > 0:
		dash_timer -= delta
		
	var is_dashing = false
	var wants_dash = Input.is_key_pressed(KEY_SPACE) or Input.is_physical_key_pressed(KEY_K)
	
	var can_attack: bool = armed
	var can_dash: bool = true
	
	if can_dash and wants_dash and dash_timer <= 0:
		dash_timer = dash_cooldown
		dash_hit_enemies.clear()
		
		# Bidik arah kursor mouse sebelum dash
		var mouse_pos = get_global_mouse_position()
		if mouse_pos.distance_to(global_position) > 5.0:
			hero_aim_dir = (mouse_pos - global_position).normalized()
			
		velocity = hero_aim_dir * 600.0
		is_dashing = true
		EventBus.spawn_pierce_dash_vfx(global_position, hero_aim_dir)
		AudioManager.play_sfx("hit") # Opsional, beri suara saat dash dimulai
	elif dash_timer > dash_cooldown - 0.2:
		is_dashing = true
		# Continuous trail dihapus agar bersih, diganti dengan burst di awal dash saja
			
		# --- DASH DAMAGE ---
		var w = get_tree().current_scene
		if w and w.has_method("get_units_near"):
			var enemies = w.get_units_near(global_position, 40.0)
			for e in enemies:
				if e.kingdom != kingdom and e.hp > 0 and not dash_hit_enemies.has(e):
					dash_hit_enemies.append(e)
					if e.has_method("take_damage"):
						e.take_damage(2.0)
					else:
						e.hp -= 2.0
						e.hp_visible_timer = 2.0
						e.queue_redraw()
	else:
		# FIX BUG STICKY KEYS: Kita baca langsung dari Input Manager Godot!
		var dir = Vector2.ZERO
		if Input.is_physical_key_pressed(KEY_W): dir.y -= 1
		if Input.is_physical_key_pressed(KEY_S): dir.y += 1
		if Input.is_physical_key_pressed(KEY_A): dir.x -= 1
		if Input.is_physical_key_pressed(KEY_D): dir.x += 1
		
		if dir != Vector2.ZERO:
			dir = dir.normalized()
			
		# Bidik arah kursor mouse
		var mouse_pos = get_global_mouse_position()
		if mouse_pos.distance_to(global_position) > 5.0:
			hero_aim_dir = (mouse_pos - global_position).normalized()
		elif dir != Vector2.ZERO:
			hero_aim_dir = dir
			
		velocity = dir * (current_speed * 1.5)
		
	# Sprite menghadap ke arah aim
	if hero_aim_dir.x < 0: sprite.flip_h = true
	else: sprite.flip_h = false
	
	if slash_timer > 0:
		slash_timer -= delta
		
	var wants_slash = Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) or Input.is_physical_key_pressed(KEY_L)
	
	if can_attack and wants_slash and slash_timer <= 0:
		slash_timer = 0.5
		# Bidik arah kursor mouse sebelum menebas
		var mouse_pos = get_global_mouse_position()
		if mouse_pos.distance_to(global_position) > 5.0:
			hero_aim_dir = (mouse_pos - global_position).normalized()
		_hero_slash(hero_aim_dir)
	elif not armed and wants_slash and slash_timer <= 0:
		slash_timer = 0.5 # cooldown sebentar
		var w = get_tree().current_scene
		if w and w.has_node("Resources"):
			var gathered = false
			for r in w.get_node("Resources").get_children():
				if not r.depleted and global_position.distance_to(r.global_position) < 100.0:
					if r.rtype == "iron" and not has_tool:
						EventBus.spawn_floating_text(global_position, "Need Tool for Iron!", Color.ORANGE)
						gathered = true
						break
					if carry == 0:
						r.deplete()
						carry_type = r.rtype
						carry = Config.RESOURCE_CARRY_AMT
						AudioManager.play_sfx("chop")
						EventBus.spawn_floating_text(global_position, "+1 " + carry_type, Color.GREEN)
						_play_squash_anim()
						gathered = true
					else:
						EventBus.spawn_floating_text(global_position, "Inventory FULL!", Color.ORANGE)
						gathered = true
					break
			if not gathered:
				EventBus.spawn_floating_text(global_position, "No Resource Nearby!", Color.WHITE)
		
	var prev_pos = global_position
	global_position += velocity * delta
	
	# Batasan Area Gunung (Wavy Boundary) untuk Hero
	var mountain_y = Config.get_mountain_bound(global_position.x)
	if global_position.y < mountain_y:
		global_position.y = mountain_y
	
	# Hero Obstacle Collision (Slide & Block)
	var w = get_tree().current_scene
	if w and "obstacles" in w:
		for obs in w.obstacles:
			if is_instance_valid(obs):
				if obs.get("depleted") == true:
					continue
				var rad = obs.get_meta("avoid_radius") if obs.has_meta("avoid_radius") else 50.0
				var hit_rad = rad * 0.7 # Hero bisa agak mepet
				var dist_prev = prev_pos.distance_to(obs.global_position)
				var dist_curr = global_position.distance_to(obs.global_position)
				
				# Mencegah pergerakan mendekati pusat rintangan jika berada dalam hit_rad
				if dist_curr < hit_rad:
					if dist_curr < dist_prev:
						if dist_prev >= hit_rad:
							var push = (global_position - obs.global_position).normalized()
							global_position = obs.global_position + push * hit_rad
						else:
							# Meluncur menyamping jika berada di dalam (proyeksi tangen) agar tidak stuck
							var normal = (global_position - obs.global_position).normalized()
							if dist_curr == 0:
								normal = Vector2(randf_range(-1, 1), randf_range(-1, 1)).normalized()
							var movement = global_position - prev_pos
							var dot = movement.dot(normal)
							if dot < 0:
								global_position = prev_pos + (movement - normal * dot)
					
					
	queue_redraw()
	
	# --- DEPOSIT ---
	w = get_tree().current_scene
	if carry > 0 and w and w.kingdoms.has(kingdom):
		var my_kingdom = w.kingdoms[kingdom]
		if global_position.distance_to(my_kingdom.base_pos) < 80.0:
			if carry_type == "wood": my_kingdom.wood += carry
			elif carry_type == "iron": my_kingdom.iron += carry
			elif carry_type == "food": my_kingdom.food += carry
			carry = 0
			carry_type = ""
			EventBus.spawn_floating_text(global_position, "Deposited", Color.YELLOW)
			
	# --- BUILD MENU POPUP (B KEY) ---
	if Input.is_physical_key_pressed(KEY_B) and not armed and not Engine.has_meta("build_menu_open"):
		_show_build_menu()

var _build_menu_layer: CanvasLayer = null

func _show_build_menu():
	if _build_menu_layer and is_instance_valid(_build_menu_layer):
		return
	Engine.set_meta("build_menu_open", true)
	
	var canvas = CanvasLayer.new()
	canvas.layer = 100
	_build_menu_layer = canvas
	get_tree().current_scene.add_child(canvas)
	
	var panel = PanelContainer.new()
	var style = StyleBoxFlat.new()
	style.bg_color = Color(0.1, 0.1, 0.1, 0.95)
	style.border_color = Color(0.8, 0.6, 0.2)
	style.border_width_left = 4
	style.border_width_right = 4
	style.border_width_top = 4
	style.border_width_bottom = 4
	style.corner_radius_top_left = 10
	style.corner_radius_top_right = 10
	style.corner_radius_bottom_left = 10
	style.corner_radius_bottom_right = 10
	style.content_margin_left = 20
	style.content_margin_right = 20
	style.content_margin_top = 20
	style.content_margin_bottom = 20
	panel.add_theme_stylebox_override("panel", style)
	
	panel.set_anchors_preset(Control.PRESET_CENTER)
	canvas.add_child(panel)
	
	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 15)
	panel.add_child(vbox)
	
	var title = Label.new()
	title.text = "BUILD MENU"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 24)
	vbox.add_child(title)
	
	var k = get_tree().current_scene.kingdoms[kingdom]
	var w_cost = Config.HOUSE_COST["wood"]
	var s_w_cost = Config.SMITH_COST["wood"]
	var s_i_cost = Config.SMITH_COST["iron"]
	var t_cost = Config.TOOL_COST["wood"]
	
	var info = Label.new()
	info.text = "Resources: %d Wood | %d Iron" % [k.wood, k.iron]
	info.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	info.add_theme_color_override("font_color", Color.YELLOW)
	vbox.add_child(info)
	
	var btn_house = Button.new()
	btn_house.text = "🏠 Build House (Cost: %d Wood)" % w_cost
	btn_house.disabled = (k.wood < w_cost)
	btn_house.pressed.connect(func():
		if k.wood >= w_cost:
			k.wood -= w_cost
			k.houses += 1
			EventBus.log_event.emit("House built by Hero!", kingdom)
			var w = get_tree().current_scene
			var b = w.BuildingScene.instantiate()
			b.kingdom = kingdom
			b.btype = "house"
			b.global_position = global_position + Vector2(0, -40)
			w.buildings_container.add_child(b)
		_close_build_menu()
	)
	vbox.add_child(btn_house)
	
	var btn_smith = Button.new()
	btn_smith.text = "⚒ Build Blacksmith (Cost: %d Wood, %d Iron)" % [s_w_cost, s_i_cost]
	btn_smith.disabled = (k.wood < s_w_cost or k.iron < s_i_cost)
	btn_smith.pressed.connect(func():
		if k.wood >= s_w_cost and k.iron >= s_i_cost:
			k.wood -= s_w_cost
			k.iron -= s_i_cost
			k.smiths += 1
			EventBus.log_event.emit("Blacksmith built by Hero!", kingdom)
			var w = get_tree().current_scene
			var b = w.BuildingScene.instantiate()
			b.kingdom = kingdom
			b.btype = "smith"
			b.global_position = global_position + Vector2(0, -40)
			w.buildings_container.add_child(b)
		_close_build_menu()
	)
	vbox.add_child(btn_smith)
	
	var btn_tool = Button.new()
	btn_tool.text = "⛏ Buy Tool (Cost: %d Wood)" % t_cost
	btn_tool.disabled = (k.wood < t_cost or has_tool)
	if has_tool: btn_tool.text = "⛏ Already have Tool"
	btn_tool.pressed.connect(func():
		if k.wood >= t_cost and not has_tool:
			k.wood -= t_cost
			has_tool = true
			_update_texture()
			EventBus.spawn_floating_text(global_position, "Equipped Tool!", Color.YELLOW)
		_close_build_menu()
	)
	vbox.add_child(btn_tool)
	
	var btn_cancel = Button.new()
	btn_cancel.text = "❌ Cancel"
	btn_cancel.pressed.connect(_close_build_menu)
	vbox.add_child(btn_cancel)

func _close_build_menu():
	Engine.set_meta("build_menu_open", false)
	if _build_menu_layer and is_instance_valid(_build_menu_layer):
		_build_menu_layer.queue_free()
		_build_menu_layer = null
	
func _hero_slash(dir: Vector2):
	AudioManager.play_sfx("hit")
	EventBus.spawn_dash_slash_vfx(global_position, dir)
	var w = get_tree().current_scene
	if w and w.has_method("get_units_near"):
		var enemies = w.get_units_near(global_position, 30.0) # Jarak pedang standar
		for e in enemies:
			if e.kingdom != kingdom and e.hp > 0:
				var to_e = (e.global_position - global_position).normalized()
				if dir.dot(to_e) > 0.3:
					if e.has_method("take_damage"):
						e.take_damage(2.0)
					else:
						e.hp -= 2.0
						e.hp_visible_timer = 2.0
						e.queue_redraw()

# ==============================================================================
# COMBAT RECEIVE DAMAGE
# ==============================================================================
func take_damage(amount: float):
	hp -= amount
	hp_visible_timer = 2.0
	queue_redraw() # Refresh HP bar
	
	# Hit Flash & Partikel Darah
	sprite.modulate = Color(2.0, 0.5, 0.5) # Berkedip kemerahan terang
	var tween = create_tween()
	tween.tween_property(sprite, "modulate", Color.WHITE, 0.2)
	
	# Percikan darah & Teks Damage
	EventBus.spawn_hit_particles(global_position, Color.DARK_RED)
	EventBus.spawn_floating_text(global_position, "-%d" % int(amount), Color.RED)
	
func _play_squash_anim():
	var t = create_tween()
	t.tween_property(sprite, "scale", Vector2(1.4, 0.6), 0.05)
	t.tween_property(sprite, "scale", Vector2(1.0, 1.0), 0.15)
