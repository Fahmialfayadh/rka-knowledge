extends Node2D
class_name World

# ==============================================================================
# PRELOAD SCENES (Dicari otomatis dari folder Scenes)
# ==============================================================================
const UnitScene = preload("res://Scenes/unit.tscn")
const ResourceScene = preload("res://Scenes/game_resource.tscn")
const BuildingScene = preload("res://Scenes/building.tscn")

# ==============================================================================
# VARIABEL DUNIA
# ==============================================================================
var kingdoms = {}
var game_over: bool = false
var elapsed_time: float = 0.0
var all_units: Array[Node] = []
var all_buildings: Array[Node] = []

var main_camera: Camera2D = null
var shake_timer: float = 0.0
var shake_magnitude: float = 0.0
var job_update_timer: float = 0.0

# === GOD MODE STATE ===
var active_power: String = "none"
var possessed_unit = null
var input_state: Dictionary = {
	"w": false, "a": false, "s": false, "d": false,
	"mx": 0.0, "my": 0.0,
	"slash": false, "dash": false
}
var obstacles: Array[Node2D] = []
var brush_indicator: Polygon2D = null

# === CAMERA ZOOM ===
const ZOOM_MIN: float = 0.5
const ZOOM_MAX: float = 2.0
const ZOOM_STEP: float = 0.1
var current_zoom: float = 1.0

# === SPATIAL GRID (WorldBox-Style) ===
# Peta dibagi menjadi kotak-kotak virtual berukuran 64px.
# Setiap unit mendaftarkan dirinya ke kotak tempat ia berdiri.
# Saat butuh tetangga, cukup cek 9 kotak sekitar = SUPER CEPAT.
const GRID_CELL_SIZE: int = 64
var spatial_grid: Dictionary = {} # Key: Vector2i, Value: Array[Unit]

@onready var units_container = $Units
@onready var buildings_container = $Buildings
@onready var resources_container = $Resources

func _ready() -> void:
	randomize()
	_setup_background()
	
	main_camera = Camera2D.new()
	main_camera.position = Vector2(Config.WIDTH / 2.0, Config.HEIGHT / 2.0)
	add_child(main_camera)
	main_camera.make_current()
	
	EventBus.shake_camera.connect(_on_shake_camera)
	
	_init_kingdoms()
	_spawn_resources()
	_spawn_initial_bases_and_units()
	
	
	_setup_environment_juice()
	_setup_pause_menu()
	
	brush_indicator = Polygon2D.new()
	var points = PackedVector2Array()
	for i in range(16):
		var a = (i / 16.0) * TAU
		points.append(Vector2(cos(a), sin(a)) * 20.0)
	brush_indicator.polygon = points
	brush_indicator.color = Color(1, 1, 1, 0.3)
	brush_indicator.visible = false
	brush_indicator.z_index = 100
	add_child(brush_indicator)

# ==============================================================================
# PAUSE MENU (ESCAPE MENU)
# ==============================================================================
var pause_overlay: CanvasLayer

func _setup_pause_menu():
	pause_overlay = CanvasLayer.new()
	pause_overlay.layer = 100 # Pastikan di atas semuanya
	pause_overlay.visible = false
	
	var overlay_bg = ColorRect.new()
	overlay_bg.color = Color(0, 0, 0, 0.7)
	overlay_bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	pause_overlay.add_child(overlay_bg)
	
	var center = CenterContainer.new()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	pause_overlay.add_child(center)
	
	var vbox = VBoxContainer.new()
	vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	vbox.add_theme_constant_override("separation", 20)
	center.add_child(vbox)
	
	var lbl_pause = Label.new()
	lbl_pause.text = "PAUSED"
	lbl_pause.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	var retro_font = preload("res://Asset/Fonts/PressStart2P.ttf")
	if retro_font: lbl_pause.add_theme_font_override("font", retro_font)
	lbl_pause.add_theme_font_size_override("font_size", 40)
	lbl_pause.add_theme_color_override("font_color", Color.WHITE)
	lbl_pause.add_theme_color_override("font_outline_color", Color.BLACK)
	lbl_pause.add_theme_constant_override("outline_size", 8)
	vbox.add_child(lbl_pause)
	
	var btn_style = StyleBoxFlat.new()
	btn_style.bg_color = Color(0.15, 0.15, 0.15)
	btn_style.border_width_bottom = 6
	btn_style.border_color = Color.BLACK
	btn_style.corner_radius_top_left = 4
	btn_style.corner_radius_top_right = 4
	btn_style.corner_radius_bottom_left = 4
	btn_style.corner_radius_bottom_right = 4
	
	var btn_resume = Button.new()
	btn_resume.text = "LANJUTKAN"
	var btn_restart = Button.new()
	btn_restart.text = "RESTART"
	var btn_menu = Button.new()
	btn_menu.text = "MENU UTAMA"
	
	for btn in [btn_resume, btn_restart, btn_menu]:
		btn.custom_minimum_size = Vector2(300, 50)
		if retro_font: btn.add_theme_font_override("font", retro_font)
		btn.add_theme_font_size_override("font_size", 16)
		btn.add_theme_color_override("font_color", Color.WHITE)
		btn.add_theme_stylebox_override("normal", btn_style)
		btn.add_theme_stylebox_override("hover", btn_style)
		btn.mouse_entered.connect(func(): btn.modulate = Color(1.2, 1.2, 0.5))
		btn.mouse_exited.connect(func(): btn.modulate = Color.WHITE)
		vbox.add_child(btn)
		
	btn_resume.pressed.connect(func():
		pause_overlay.visible = false
		Engine.time_scale = 1.0
	)
	btn_restart.pressed.connect(func():
		Engine.time_scale = 1.0
		get_tree().reload_current_scene()
	)
	btn_menu.pressed.connect(func():
		Engine.time_scale = 1.0
		get_tree().change_scene_to_file("res://Scenes/MainMenu.tscn")
	)
	
	add_child(pause_overlay)

func _unhandled_input(event):
	if event.is_action_pressed("ui_cancel"):
		if pause_overlay.visible:
			pause_overlay.visible = false
			Engine.time_scale = 1.0
		else:
			pause_overlay.visible = true
			Engine.time_scale = 0.0
			
	if pause_overlay.visible or game_over: return
	
	if event is InputEventMouseMotion:
		# Camera Panning
		if Input.is_mouse_button_pressed(MOUSE_BUTTON_MIDDLE):
			main_camera.position -= event.relative * (1.0 / current_zoom)
			
		var mpos = get_global_mouse_position()
		input_state["mx"] = mpos.x
		input_state["my"] = mpos.y
		if brush_indicator:
			brush_indicator.global_position = mpos
			brush_indicator.visible = active_power != "none"
			
			var r = 20.0
			if active_power in ["bomb", "lightning"]:
				r = 80.0 if active_power == "bomb" else 40.0
				brush_indicator.color = Color(1, 0, 0, 0.3)
			elif active_power == "possess":
				r = 40.0
				brush_indicator.color = Color(1, 1, 0, 0.3)
			elif active_power == "grass":
				r = 30.0
				brush_indicator.color = Color(1, 0.5, 0.5, 0.3)
			elif active_power in ["water", "mountain"]:
				# Placement validation: hijau jika valid, merah jika invalid
				var valid = _is_valid_placement(mpos)
				brush_indicator.color = Color(0, 1, 0, 0.3) if valid else Color(1, 0, 0, 0.3)
			else:
				brush_indicator.color = Color(1, 1, 1, 0.3)
				
			var pts = PackedVector2Array()
			for i in range(16):
				var a = (i / 16.0) * TAU
				pts.append(Vector2(cos(a), sin(a)) * r)
			brush_indicator.polygon = pts
			
		if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and active_power in ["water", "mountain", "grass"]:
		
			if mpos.y > Config.get_mountain_bound(mpos.x):
				_apply_god_power(active_power, mpos)
			
	elif event is InputEventMouseButton:
		# Camera Zoom (scroll wheel)
		if event.pressed:
			if event.button_index == MOUSE_BUTTON_WHEEL_UP:
				current_zoom = clamp(current_zoom + ZOOM_STEP, ZOOM_MIN, ZOOM_MAX)
				var tw = create_tween()
				tw.tween_property(main_camera, "zoom", Vector2(current_zoom, current_zoom), 0.15)
				return
			elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
				current_zoom = clamp(current_zoom - ZOOM_STEP, ZOOM_MIN, ZOOM_MAX)
				var tw = create_tween()
				tw.tween_property(main_camera, "zoom", Vector2(current_zoom, current_zoom), 0.15)
				return
		
		if event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
			var mpos = get_global_mouse_position()
			if mpos.y < Config.get_mountain_bound(mpos.x):
				return # Dilarang meletakkan god power di area gunung background
			if active_power == "possess":
				if not possessed_unit:
					_apply_god_power(active_power, mpos)
			elif active_power != "none":
				_apply_god_power(active_power, mpos)
		elif event.button_index == MOUSE_BUTTON_RIGHT and event.pressed:
			if possessed_unit:
				if is_instance_valid(possessed_unit):
					possessed_unit.set("is_possessed", false)
				possessed_unit = null

func _apply_god_power(power, pos: Vector2):
	# Task 4C: Placement validation guard
	if power in ["water", "mountain"]:
		if not _is_valid_placement(pos):
			return # Tolak placement

	if power == "water" or power == "mountain":
		var obs = Polygon2D.new()
		obs.set_meta("boids_type", power)
		var rad = 55.0
		if power == "mountain": rad = 70.0 # Task 4B: Increased mountain radius
		if power == "water": rad = 130.0
		obs.set_meta("avoid_radius", rad)
		var points = PackedVector2Array()
		for i in range(6):
			var a = (i / 6.0) * TAU
			var r = 15.0 + randf() * 10.0
			points.append(Vector2(cos(a), sin(a)) * r)
		obs.polygon = points
		obs.global_position = pos
		add_child(obs)
		obstacles.append(obs)
		
		if power == "mountain":
			obs.color = Color(0, 0, 0, 0) # Sembunyikan footprint dasar
			var m_sprite = Sprite2D.new()
			var tex = load("res://Asset/Sprites/Mountain.png")
			m_sprite.texture = tex
			# Titik tumpu di bawah agar gunung tumbuh dari dasar
			m_sprite.offset = Vector2(0, -tex.get_height() / 2.0)
			m_sprite.scale = Vector2(0.18, 0.18) # Kecilkan lagi skalanya
			
			# Mulai dari bawah tanah dan transparan
			m_sprite.position = Vector2(0, 50.0)
			m_sprite.modulate.a = 0.0
			obs.add_child(m_sprite)
			
			var tw = create_tween()
			tw.tween_property(m_sprite, "position", Vector2.ZERO, 0.8).set_trans(Tween.TRANS_ELASTIC).set_ease(Tween.EASE_OUT)
			tw.parallel().tween_property(m_sprite, "modulate:a", 1.0, 0.3)
			
			EventBus.shake_camera.emit(1.0, 0.15) # Task 4A: Reduced mountain shake

			
			# Partikel debu tanah menyebar
			var dust = CPUParticles2D.new()
			dust.emitting = true
			dust.one_shot = true
			dust.explosiveness = 0.9
			dust.spread = 180
			dust.gravity = Vector2(0, 0)
			dust.initial_velocity_min = 50.0
			dust.initial_velocity_max = 100.0
			dust.damping_min = 100.0
			dust.damping_max = 150.0
			dust.scale_amount_min = 3.0
			dust.scale_amount_max = 5.0
			dust.color = Color(0.6, 0.5, 0.4, 0.6) # Coklat tanah
			dust.amount = 40
			dust.lifetime = 1.0
			obs.add_child(dust) # Jadikan child dari obs agar mengikuti lokasinya
		elif power == "water":
			# Water (Danau)
			obs.color = Color(0, 0, 0, 0) # Sembunyikan footprint dasar
			var w_sprite = Sprite2D.new()
			var tex = load("res://Asset/Sprites/Water.png")
			w_sprite.texture = tex
			# Offset di tengah
			w_sprite.offset = Vector2.ZERO
			w_sprite.scale = Vector2.ZERO # Mulai dari tidak ada
			w_sprite.modulate.a = 0.0
			obs.add_child(w_sprite)
			
			var tw = create_tween()
			tw.tween_property(w_sprite, "scale", Vector2(1.0, 1.0), 0.8).set_trans(Tween.TRANS_ELASTIC).set_ease(Tween.EASE_OUT)
			tw.parallel().tween_property(w_sprite, "modulate:a", 1.0, 0.4)
			
			# Suara air/splash opsional
			AudioManager.play_sfx("hit") # Pakai sfx hit sementara
			
			# Partikel percikan air (Water Splash)
			var splash = CPUParticles2D.new()
			splash.emitting = true
			splash.one_shot = true
			splash.explosiveness = 0.85
			splash.spread = 180
			splash.gravity = Vector2(0, 0)
			splash.initial_velocity_min = 60.0
			splash.initial_velocity_max = 120.0
			splash.damping_min = 100.0
			splash.damping_max = 150.0
			splash.scale_amount_min = 2.0
			splash.scale_amount_max = 4.0
			splash.color = Color(0.2, 0.8, 1.0, 0.8) # Biru/Cyan cerah
			splash.amount = 30
			splash.lifetime = 0.8
			obs.add_child(splash)
		
	elif power == "grass":
		for o in obstacles:
			if is_instance_valid(o) and o.global_position.distance_to(pos) < 30.0:
				o.queue_free()
		obstacles = obstacles.filter(func(x): return is_instance_valid(x) and not x.is_queued_for_deletion())
		for r in resources_container.get_children():
			if r.global_position.distance_to(pos) < 30.0:
				r.deplete()
				
	elif power == "bomb":
		EventBus.spawn_falling_bomb(pos, 0.8) # Durasi jatuh 0.8 detik
		await get_tree().create_timer(0.8).timeout
		
		EventBus.shake_camera.emit(10.0, 0.5)
		EventBus.spawn_hit_particles(pos, Color.ORANGE)
		EventBus.spawn_explosion_vfx(pos)
		for u in get_units_near(pos, 80.0):
			if u.hp > 0:
				u.take_damage(999)
		for b in all_buildings:
			if is_instance_valid(b) and b.global_position.distance_to(pos) < 80.0:
				b.take_damage(999)
				
	elif power == "lightning":
		EventBus.shake_camera.emit(5.0, 0.2)
		EventBus.spawn_hit_particles(pos, Color.YELLOW)
		EventBus.spawn_lightning_vfx(pos)
		for u in get_units_near(pos, 40.0):
			if u.hp > 0:
				u.take_damage(999)
				
	elif power == "spawn_red":
		_spawn_unit("red", pos, "defender")
		
	elif power == "spawn_blue":
		_spawn_unit("blue", pos, "defender")
		
	elif power == "possess":
		if possessed_unit:
			possessed_unit.set("is_possessed", false)
			possessed_unit = null
			
		var nearest = null
		var min_d = 100.0
		for u in get_units_near(pos, 100.0):
			if u.hp > 0:
				var d = u.global_position.distance_to(pos)
				if d < min_d:
					min_d = d
					nearest = u
					
		if nearest:
			nearest.set("is_possessed", true)
			possessed_unit = nearest
			EventBus.log_event.emit("God possessed a unit!", nearest.kingdom)

# ==============================================================================
# ENVIRONMENT JUICE (DAY/NIGHT, CLOUDS, VIGNETTE)
# ==============================================================================
var cloud_nodes = []
func _setup_environment_juice():
	# 1. Day/Night Cycle (CanvasModulate)
	var canvas_mod = CanvasModulate.new()
	canvas_mod.color = Color.WHITE
	add_child(canvas_mod)
	
	var tw = create_tween().set_loops()
	var day = Color.WHITE
	var sunset = Color(0.9, 0.6, 0.5)
	var night = Color(0.25, 0.25, 0.45) # Malam yang dingin
	
	tw.tween_property(canvas_mod, "color", sunset, 40.0)
	tw.tween_property(canvas_mod, "color", night, 20.0)
	tw.tween_property(canvas_mod, "color", sunset, 20.0)
	tw.tween_property(canvas_mod, "color", day, 30.0)
	
	# 2. Bayangan Awan Bergerak
	for i in range(5):
		var cloud = Polygon2D.new()
		cloud.color = Color(0, 0, 0, 0.15) # Hitam transparan (Bayangan)
		
		# Bikin bentuk awan gumpalan acak
		var points = PackedVector2Array()
		for j in range(8):
			var angle = (j / 8.0) * PI * 2
			var radius = randf_range(50.0, 150.0)
			points.append(Vector2(cos(angle), sin(angle)) * radius)
		cloud.polygon = points
		cloud.global_position = Vector2(randf_range(0, 1152), randf_range(0, 648))
		add_child(cloud)
		cloud_nodes.append(cloud)
	
	# 3. Vignette (Fokus Sinematik)
	var vignette = TextureRect.new()
	vignette.set_anchors_preset(Control.PRESET_FULL_RECT)
	vignette.mouse_filter = Control.MOUSE_FILTER_IGNORE
	vignette.z_index = 50 # Di atas karakter tapi di bawah UI
	
	var grad = Gradient.new()
	grad.set_color(0, Color(0, 0, 0, 0)) # Tengah bolong
	grad.set_color(1, Color(0, 0, 0, 0.6)) # Pinggiran gelap
	var grad_tex = GradientTexture2D.new()
	grad_tex.gradient = grad
	grad_tex.fill = GradientTexture2D.FILL_RADIAL
	grad_tex.fill_from = Vector2(0.5, 0.5)
	grad_tex.fill_to = Vector2(1.0, 1.0)
	vignette.texture = grad_tex
	add_child(vignette)
	
	# Muat layar UI
	var ui_scene = preload("res://Scenes/UI.tscn").instantiate()
	add_child(ui_scene)

func _setup_background():
	var bg = Sprite2D.new()
	bg.texture = preload("res://Asset/Sprites/Map.PNG")
	bg.centered = false # Pasang dari pojok kiri atas
	
	# Karena resolusi gambarnya mungkin beda dengan layar kita, kita paksa penuhi layar:
	var screen_size = get_viewport_rect().size
	var tex_size = bg.texture.get_size()
	bg.scale = Vector2(screen_size.x / tex_size.x, screen_size.y / tex_size.y)
	
	add_child(bg)
	move_child(bg, 0) # Pindahkan ke urutan paling atas di daftar agar ter-render paling belakang

func _on_shake_camera(mag: float, dur: float):
	shake_magnitude = mag
	shake_timer = dur

func _process(delta: float) -> void:
	if game_over:
		return
		
	elapsed_time += delta
	
	# Gerakkan bayangan awan
	for cloud in cloud_nodes:
		cloud.global_position.x += 10.0 * delta # Bergerak pelan ke kanan
		if cloud.global_position.x > 1152 + 200:
			cloud.global_position.x = -200
			cloud.global_position.y = randf_range(0, 648)
	
	if shake_timer > 0:
		shake_timer -= delta
		main_camera.offset = Vector2(randf_range(-shake_magnitude, shake_magnitude), randf_range(-shake_magnitude, shake_magnitude))
	else:
		if main_camera:
			main_camera.offset = Vector2.ZERO
			
	if game_over: return
	
	all_units = units_container.get_children()
	all_buildings = buildings_container.get_children()
	
	# Update Spatial Grid setiap frame (sangat murah: O(N) sekali jalan)
	_update_spatial_grid()
	
	# Update otak kedua kerajaan
	kingdoms["red"].evaluate_utilities(kingdoms["blue"], all_units, delta)
	kingdoms["blue"].evaluate_utilities(kingdoms["red"], all_units, delta)

	# CSP Job Scheduler — periodik batch assignment (timer dikelola internal Kingdom)
	kingdoms["red"].tick_csp(delta, all_units, all_buildings)
	kingdoms["blue"].tick_csp(delta, all_units, all_buildings)
	
	# Update papan pekerjaan secara berkala (setiap 0.5 detik) agar tidak membebani CPU
	job_update_timer -= delta
	if job_update_timer <= 0:
		job_update_timer = 0.5
		var res_nodes = resources_container.get_children()
		kingdoms["red"].job_board.update_jobs(kingdoms["red"], res_nodes)
		kingdoms["blue"].job_board.update_jobs(kingdoms["blue"], res_nodes)
	
	# Hitung total populasi hidup & alat
	var r_alive = 0
	var b_alive = 0
	var r_tools = 0
	var b_tools = 0
	for u in all_units:
		if not is_instance_valid(u) or u.is_queued_for_deletion(): continue
		if u.hp > 0:
			if u.kingdom == "red": 
				r_alive += 1
				if u.has_tool: r_tools += 1
			elif u.kingdom == "blue": 
				b_alive += 1
				if u.has_tool: b_tools += 1
			
	kingdoms["red"].pop = r_alive
	kingdoms["red"].active_tools = r_tools
	kingdoms["blue"].pop = b_alive
	kingdoms["blue"].active_tools = b_tools
	
	# Cek Game Over: Base hancur ATAU populasi punah
	var red_base_dead = (kingdoms["red"].base_node == null or not is_instance_valid(kingdoms["red"].base_node) or kingdoms["red"].base_node.hp <= 0)
	var blue_base_dead = (kingdoms["blue"].base_node == null or not is_instance_valid(kingdoms["blue"].base_node) or kingdoms["blue"].base_node.hp <= 0)
	
	# Hitung sisa bangunan untuk syarat kemenangan absolut
	var r_buildings = 0
	var b_buildings = 0
	for b in all_buildings:
		if is_instance_valid(b) and not b.is_queued_for_deletion() and b.hp > 0:
			if b.kingdom == "red": r_buildings += 1
			elif b.kingdom == "blue": b_buildings += 1
	
	# Kemenangan hanya terjadi jika base HANCUR dan SEMUA bangunan RATA, atau semua warganya MATI dan tidak ada rumah tersisa untuk bertelur.
	if (red_base_dead and r_buildings == 0) or (r_alive <= 0 and r_buildings == 0):
		_end_game("Blue Wins!")
	elif (blue_base_dead and b_buildings == 0) or (b_alive <= 0 and b_buildings == 0):
		_end_game("Red Wins!")

# ==============================================================================
# PEMBUATAN PETA (MAP GENERATION)
# ==============================================================================
func _init_kingdoms():
	var center_y = Config.SIM_Y + Config.SIM_H / 2
	# Base Merah di kiri, Base Biru di kanan
	kingdoms["red"] = Kingdom.new("red", Vector2(Config.SIM_X + 80, center_y))
	kingdoms["blue"] = Kingdom.new("blue", Vector2(Config.SIM_X + Config.SIM_W - 80, center_y))

func _spawn_resources():
	for _i in range(Config.INIT_RESOURCES):
		var rtype = Config.RESOURCE_TYPES[randi() % Config.RESOURCE_TYPES.size()]
		var pos = _get_valid_resource_pos()
		var r = ResourceScene.instantiate()
		r.rtype = rtype
		r.global_position = pos
		resources_container.add_child(r)

func _get_valid_resource_pos() -> Vector2:
	# Cari posisi yang tidak menabrak pangkalan
	while true:
		var rx = randf_range(Config.SIM_X + 20, Config.SIM_X + Config.SIM_W - 20)
		var ry = randf_range(Config.SIM_Y + 20, Config.SIM_Y + Config.SIM_H - 20)
		var pos = Vector2(rx, ry)
		
		var d_red = pos.distance_to(kingdoms["red"].base_pos)
		var d_blue = pos.distance_to(kingdoms["blue"].base_pos)
		if d_red > 100.0 and d_blue > 100.0:
			return pos
	return Vector2.ZERO

func _spawn_initial_bases_and_units():
	for kname in kingdoms.keys():
		var k = kingdoms[kname]
		
		# Spawn Markas (Base)
		var base_bld = BuildingScene.instantiate()
		base_bld.kingdom = kname
		base_bld.btype = "base"
		base_bld.global_position = k.base_pos
		
		buildings_container.add_child(base_bld)
		k.base_node = base_bld
		
		# Spawn Awal Pekerja (10 Pekerja per Kingdom)
		# Meniru rasio pasti dari Python (60% Gatherer, 20% Builder, 20% Defender)
		var role_pool = []
		for i in range(6): role_pool.append("gatherer")
		for i in range(2): role_pool.append("builder")
		for i in range(2): role_pool.append("defender")
		role_pool.shuffle()
		
		var pop_limit = Config.INIT_POP_RED if kname == "red" else Config.INIT_POP_BLUE
		for i in range(pop_limit):
			var role = role_pool[i % role_pool.size()]
			_spawn_unit(kname, k.base_pos + Vector2(randf_range(-30, 30), randf_range(-30, 30)), role)

func _spawn_unit(kname: String, pos: Vector2, role: String = "gatherer"):
	var u = UnitScene.instantiate()
	u.kingdom = kname
	u.global_position = pos
	u.role = role
	
	# Injeksi referensi kerajaan ke unit
	u.my_kingdom = kingdoms[kname]
	u.enemy_kingdom = kingdoms["blue" if kname == "red" else "red"]
	
	units_container.add_child(u)

func _end_game(winner_msg: String):
	game_over = true
	print("GAME OVER! ", winner_msg)
	
	# Layar Kemenangan (Victory Overlay)
	var overlay = CanvasLayer.new()
	overlay.layer = 100 # Di atas segalanya
	
	# Latar belakang gelap transparan (Animasi Fade-in)
	var bg = ColorRect.new()
	bg.color = Color(0, 0, 0, 0.0)
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	overlay.add_child(bg)
	
	var tw_bg = create_tween()
	tw_bg.tween_property(bg, "color:a", 0.8, 1.0)
	
	# Kontainer tengah
	var center = CenterContainer.new()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	overlay.add_child(center)
	
	# Papan Pengumuman (Panel Kertas Tua)
	var panel = PanelContainer.new()
	var retro_panel = StyleBoxFlat.new()
	retro_panel.bg_color = Color(0.8, 0.7, 0.5) # Warna perkamen / kertas tua
	retro_panel.border_width_left = 8
	retro_panel.border_width_top = 8
	retro_panel.border_width_right = 8
	retro_panel.border_width_bottom = 8
	retro_panel.border_color = Color.BLACK
	retro_panel.content_margin_left = 40.0
	retro_panel.content_margin_right = 40.0
	retro_panel.content_margin_top = 40.0
	retro_panel.content_margin_bottom = 40.0
	panel.add_theme_stylebox_override("panel", retro_panel)
	
	# Animasi Panel Pop-In Elastic
	panel.scale = Vector2.ZERO
	panel.pivot_offset = Vector2(250, 150) # Asumsi ukuran tengah
	var tw_panel = create_tween()
	tw_panel.tween_property(panel, "scale", Vector2.ONE, 0.8).set_trans(Tween.TRANS_ELASTIC).set_ease(Tween.EASE_OUT).set_delay(0.5)
	
	center.add_child(panel)
	
	var vbox = VBoxContainer.new()
	vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	vbox.add_theme_constant_override("separation", 20)
	panel.add_child(vbox)
	
	var retro_font = preload("res://Asset/Fonts/PressStart2P.ttf")
	
	# Teks "GAME OVER"
	var lbl_go = Label.new()
	lbl_go.text = "GAME OVER"
	lbl_go.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if retro_font: lbl_go.add_theme_font_override("font", retro_font)
	lbl_go.add_theme_font_size_override("font_size", 40)
	lbl_go.add_theme_color_override("font_color", Color.BLACK)
	lbl_go.add_theme_color_override("font_shadow_color", Color(0,0,0,0.3))
	lbl_go.add_theme_constant_override("shadow_offset_x", 4)
	lbl_go.add_theme_constant_override("shadow_offset_y", 4)
	vbox.add_child(lbl_go)
	
	# Teks Pemenang
	var lbl_winner = Label.new()
	lbl_winner.text = winner_msg
	lbl_winner.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if retro_font: lbl_winner.add_theme_font_override("font", retro_font)
	lbl_winner.add_theme_font_size_override("font_size", 24)
	var win_color = Color.RED if "Red" in winner_msg else Color.CORNFLOWER_BLUE
	lbl_winner.add_theme_color_override("font_color", win_color)
	lbl_winner.add_theme_color_override("font_outline_color", Color.BLACK)
	lbl_winner.add_theme_constant_override("outline_size", 6)
	vbox.add_child(lbl_winner)
	
	# Statistik waktu
	var lbl_time = Label.new()
	lbl_time.text = "Durasi: %d mnt %d dtk" % [int(elapsed_time) / 60, int(elapsed_time) % 60]
	lbl_time.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if retro_font: lbl_time.add_theme_font_override("font", retro_font)
	lbl_time.add_theme_font_size_override("font_size", 12)
	lbl_time.add_theme_color_override("font_color", Color(0.2, 0.2, 0.2)) # Abu-abu tua agar rapi
	vbox.add_child(lbl_time)
	
	# Spacer
	var spacer = Control.new()
	spacer.custom_minimum_size = Vector2(0, 10)
	vbox.add_child(spacer)
	
	# Wadah tombol agar rapi
	var btn_vbox = VBoxContainer.new()
	btn_vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	btn_vbox.add_theme_constant_override("separation", 10)
	
	var btn_style = StyleBoxFlat.new()
	btn_style.bg_color = Color(0.15, 0.15, 0.15)
	btn_style.border_width_bottom = 6
	btn_style.border_color = Color.BLACK
	btn_style.corner_radius_top_left = 4
	btn_style.corner_radius_top_right = 4
	btn_style.corner_radius_bottom_left = 4
	btn_style.corner_radius_bottom_right = 4
	
	# Tombol Play Again
	var btn_restart = Button.new()
	btn_restart.text = "MAIN LAGI"
	btn_restart.custom_minimum_size = Vector2(200, 40)
	if retro_font: btn_restart.add_theme_font_override("font", retro_font)
	btn_restart.add_theme_font_size_override("font_size", 16)
	btn_restart.add_theme_color_override("font_color", Color.WHITE)
	btn_restart.add_theme_stylebox_override("normal", btn_style)
	btn_restart.add_theme_stylebox_override("hover", btn_style)
	btn_restart.mouse_entered.connect(func(): btn_restart.modulate = Color(1.2, 1.2, 0.5))
	btn_restart.mouse_exited.connect(func(): btn_restart.modulate = Color.WHITE)
	btn_restart.pressed.connect(func(): get_tree().reload_current_scene())
	btn_vbox.add_child(btn_restart)
	
	# Tombol Kembali Ke Menu
	var btn_menu = Button.new()
	btn_menu.text = "MENU UTAMA"
	btn_menu.custom_minimum_size = Vector2(200, 40)
	if retro_font: btn_menu.add_theme_font_override("font", retro_font)
	btn_menu.add_theme_font_size_override("font_size", 16)
	btn_menu.add_theme_color_override("font_color", Color.WHITE)
	btn_menu.add_theme_stylebox_override("normal", btn_style)
	btn_menu.add_theme_stylebox_override("hover", btn_style)
	btn_menu.mouse_entered.connect(func(): btn_menu.modulate = Color(1.2, 1.2, 0.5))
	btn_menu.mouse_exited.connect(func(): btn_menu.modulate = Color.WHITE)
	btn_menu.pressed.connect(func():
		Engine.time_scale = 1.0 # Kembalikan waktu ke normal sebelum ganti scene!
		get_tree().change_scene_to_file("res://Scenes/MainMenu.tscn")
	)
	btn_vbox.add_child(btn_menu)
	
	vbox.add_child(btn_vbox)
	
	get_tree().current_scene.add_child(overlay)
	
	# Perlambat permainan menjadi slow-motion
	Engine.time_scale = 0.1

# ==============================================================================
# SISTEM PEMBANGUNAN (BUILDING SYSTEM)
# ==============================================================================
func _try_build(kname: String):
	var k = kingdoms[kname]
	var sign = 1 if kname == "red" else -1
	
	var has_empty_smith = false
	for b in buildings_container.get_children():
		if b.kingdom == kname and b.btype == "smith" and b.trainees < b.max_trainees:
			has_empty_smith = true
			break
			
	var can_build_smith = (not has_empty_smith and k.wood >= Config.SMITH_COST["wood"] and k.iron >= Config.SMITH_COST["iron"])
	var can_build_house = (k.wood >= Config.HOUSE_COST["wood"])
	
	var want_smith = k.u_iron > 40.0
	var want_house = k.u_wood > 30.0
	var want_smith_building = want_smith and not has_empty_smith
	
	var build_smith = func():
		k.wood -= Config.SMITH_COST["wood"]
		k.iron -= Config.SMITH_COST["iron"]
		k.smiths += 1
		EventBus.log_event.emit("Blacksmith built!", kname)
		var bx = k.base_pos.x + sign * 60 + randf_range(-15, 15)
		var by = k.base_pos.y - 30 + randf_range(-20, 20)
		
		var b = BuildingScene.instantiate()
		b.kingdom = kname
		b.btype = "smith"
		b.global_position = Vector2(bx, by)
		buildings_container.add_child(b)
		
	var build_house = func():
		k.wood -= Config.HOUSE_COST["wood"]
		k.houses += 1
		EventBus.log_event.emit("House built!", kname)
		var bx = k.base_pos.x + sign * 40 + randf_range(-20, 20)
		var by = k.base_pos.y + randf_range(-40, 40)
		
		var b = BuildingScene.instantiate()
		b.kingdom = kname
		b.btype = "house"
		b.global_position = Vector2(bx, by)
		buildings_container.add_child(b)
		
	if k.focus == "WOOD" and want_house:
		if can_build_house:
			build_house.call()
		elif can_build_smith and want_smith_building:
			# Jangan menunggu kayu terkumpul selamanya jika bisa bikin smith sekarang!
			build_smith.call()
	elif k.focus == "IRON" and want_smith_building:
		if can_build_smith:
			build_smith.call()
		elif can_build_house and want_house:
			build_house.call()
	else:
		if can_build_smith and want_smith_building:
			build_smith.call()
		elif can_build_house and want_house:
			build_house.call()

# ==============================================================================
# SPATIAL GRID (WorldBox-Style Optimization)
# ==============================================================================

## Memperbarui grid spasial — dipanggil sekali per frame di _process()
func _update_spatial_grid():
	spatial_grid.clear()
	for u in all_units:
		if not is_instance_valid(u) or u.is_queued_for_deletion() or u.hp <= 0 or not u.visible:
			continue
		var cx = int(u.global_position.x) / GRID_CELL_SIZE
		var cy = int(u.global_position.y) / GRID_CELL_SIZE
		var cell = Vector2i(cx, cy)
		if not spatial_grid.has(cell):
			spatial_grid[cell] = []
		spatial_grid[cell].append(u)

## Mengambil unit-unit terdekat dalam radius — JAUH LEBIH CEPAT dari loop seluruh dunia!
func get_units_near(pos: Vector2, radius: float) -> Array:
	var result = []
	var cell_radius = int(radius / GRID_CELL_SIZE) + 1
	var center_cx = int(pos.x) / GRID_CELL_SIZE
	var center_cy = int(pos.y) / GRID_CELL_SIZE
	var radius_sq = radius * radius
	
	for dx in range(-cell_radius, cell_radius + 1):
		for dy in range(-cell_radius, cell_radius + 1):
			var cell = Vector2i(center_cx + dx, center_cy + dy)
			if spatial_grid.has(cell):
				for u in spatial_grid[cell]:
					if is_instance_valid(u) and not u.is_queued_for_deletion() and u.hp > 0:
						if pos.distance_squared_to(u.global_position) <= radius_sq:
							result.append(u)
	return result

# ==============================================================================
# PLACEMENT VALIDATION
# ==============================================================================
func _is_valid_placement(pos: Vector2) -> bool:
	# Cek 1: Ada unit di posisi ini?
	var nearby_units = get_units_near(pos, 25.0)
	if not nearby_units.is_empty():
		return false

	# Cek 2: Overlap dengan base (red atau blue)?
	for kname in kingdoms:
		if is_instance_valid(kingdoms[kname].base_node):
			if pos.distance_to(kingdoms[kname].base_pos) < 60.0:
				return false

	return true
