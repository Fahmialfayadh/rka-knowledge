extends Area2D
class_name Building

@export var kingdom: String = "red" # "red" atau "blue"
@export var btype: String = "house" # "base", "house", "smith"

var hp: float = 50.0
var hp_visible_timer: float = 0.0
var trainees: int = 0
var _last_trainees: int = -1 # Cache untuk deteksi perubahan
var max_trainees: int = Config.SMITH_MAX_TRAINEES
var spawn_timer: float = 0.0
var _base_inv_scale: float = 1.0

func _ready() -> void:
	add_to_group("buildings")
	if btype == "base":
		hp = Config.BASE_MAX_HP
		
	var sprite = $Sprite2D
	if btype == "house" or btype == "base":
		sprite.texture = preload("res://Asset/Sprites/house.png")
	elif btype == "smith":
		sprite.texture = preload("res://Asset/Sprites/blacksmith.png")
		
	# Tetap beri sedikit warna transparan merah/biru agar kita tahu ini rumah milik siapa
	if kingdom == "red":
		sprite.modulate = Color(1.0, 0.6, 0.6) # Kemerahan
	else:
		sprite.modulate = Color(0.6, 0.6, 1.0) # Kebiruan
		
	# Efek Pop-In (Tumbuh elastis saat dibangun)
	if btype != "base":
		var target_scale = scale # Simpan skala asli yang sudah disetting di Godot Editor
		_base_inv_scale = 1.0 / target_scale.x if target_scale.x > 0 else 1.0
		scale = Vector2.ZERO
		var tween = create_tween()
		tween.tween_property(self, "scale", target_scale, 0.5).set_trans(Tween.TRANS_ELASTIC).set_ease(Tween.EASE_OUT)
		# Kepulan debu pembangunan dan light flash
		EventBus.spawn_building_vfx(global_position, btype)
	else:
		_base_inv_scale = 1.0 / scale.x if scale.x > 0 else 1.0

func _process(delta: float) -> void:
	if hp_visible_timer > 0:
		hp_visible_timer -= delta
		queue_redraw() # Hanya redraw saat HP bar aktif
	
	# Smith: redraw saat jumlah trainee berubah
	if btype == "smith":
		if trainees != _last_trainees:
			_last_trainees = trainees
			queue_redraw()
	
	if btype == "house":
		spawn_timer -= delta
		if spawn_timer <= 0:
			spawn_timer = Config.HOUSE_SPAWN_TIME
			var world = get_tree().current_scene
			if world and world.has_method("_spawn_unit") and world.kingdoms.has(kingdom):
				var k = world.kingdoms[kingdom]
				k.pop += 1
				# Role: 60% gatherer, 20% builder, 20% defender (sama dengan Python _make_unit)
				var r = randf()
				var role = "gatherer"
				if r < 0.2:
					role = "defender"
				elif r < 0.4:
					role = "builder"
				world._spawn_unit(kingdom, global_position, role)
				EventBus.log_event.emit("New " + role + " born!", kingdom)
				AudioManager.play_sfx("spawn")
		
func take_damage(amount: float):
	hp -= amount
	hp_visible_timer = 2.0
	queue_redraw() # Refresh HP bar
	
	# VFX: Teks Damage & Partikel Serpihan Kayu
	EventBus.spawn_floating_text(global_position, "-%d" % int(amount), Color.RED)
	EventBus.spawn_hit_particles(global_position, Color(0.6, 0.4, 0.2)) # Warna coklat kayu
	
	# SFX
	AudioManager.play_sfx("hit")
	
	# Camera Shake (semakin besar bangunan, semakin keras getarannya)
	var shake_power = 2.0 if btype == "base" else 1.0
	EventBus.shake_camera.emit(shake_power, 0.15)
	
	# Hit Flash Bangunan & Partikel
	var sprite = $Sprite2D
	var original_color = Color(1.0, 0.6, 0.6) if kingdom == "red" else Color(0.6, 0.6, 1.0)
	sprite.modulate = Color(2.0, 2.0, 2.0) # Kedip Putih
	var tween = create_tween()
	tween.tween_property(sprite, "modulate", original_color, 0.15)
	
	# Partikel serpihan bangunan
	EventBus.spawn_hit_particles(global_position, Color.DIM_GRAY)
	
	if hp <= 0:
		# Hancur berkeping-keping!
		EventBus.spawn_hit_particles(global_position, Color.GRAY)
		
		if btype == "base":
			EventBus.shake_camera.emit(25.0, 1.5) # Getaran dahsyat
		else:
			EventBus.shake_camera.emit(10.0, 0.3) # Getaran biasa
			
		# Tinggalkan puing-puing hitam hangus di tanah
		var rubble = Sprite2D.new()
		rubble.texture = sprite.texture
		rubble.global_position = global_position
		rubble.modulate = Color.BLACK
		rubble.modulate.a = 0.5
		rubble.z_index = -1 # Di bawah tanah
		get_tree().current_scene.add_child(rubble)
			
		queue_free()
func _exit_tree():
	var world = get_tree().current_scene
	if world and world.has_method("_try_build") and world.kingdoms.has(kingdom):
		if btype == "house": world.kingdoms[kingdom].houses -= 1
		elif btype == "smith": world.kingdoms[kingdom].smiths -= 1

# ==============================================================================
# HP BAR & TRAINING INDICATOR via _draw() — DIJAMIN MUNCUL
# ==============================================================================
func _draw():
	# Gunakan base_inv_scale yang dicache agar tidak glitch saat animasi pop-in
	var inv_scale = _base_inv_scale
	var max_hp = Config.BASE_MAX_HP if btype == "base" else 50.0
	
	# Bar diperkecil
	var bar_w = 30.0 * inv_scale if btype == "base" else 24.0 * inv_scale
	var bar_h = 4.0 * inv_scale
	var bar_x = -bar_w / 2.0
	var bar_y = -40.0 * inv_scale # Turunkan sedikit posisinya
	
	if hp_visible_timer > 0 and SettingsManager.show_hp_bar:
		# Hitung alpha untuk fade out
		var alpha = 1.0
		if hp_visible_timer < 0.5:
			alpha = hp_visible_timer / 0.5
			
		# 1. Outline Hitam Solid (Gaya Retro)
		var out_w = bar_w + 2.0 * inv_scale
		var out_h = bar_h + 2.0 * inv_scale
		draw_rect(Rect2(bar_x - inv_scale, bar_y - inv_scale, out_w, out_h), Color(0.0, 0.0, 0.0, alpha))
		
		# 2. Background Merah Gelap (Daging kosong)
		draw_rect(Rect2(bar_x, bar_y, bar_w, bar_h), Color(0.3, 0.0, 0.0, alpha))
		
		# 3. Foreground (Nyawa)
		var ratio = clamp(hp / max_hp, 0.0, 1.0)
		if ratio > 0:
			var fg_color = Color.GREEN if ratio > 0.5 else (Color.YELLOW if ratio > 0.25 else Color.RED)
			fg_color.a = alpha
			draw_rect(Rect2(bar_x, bar_y, bar_w * ratio, bar_h), fg_color)
	
	# Khusus Smith: Teks Training Indicator (Tetap selalu muncul)
	if btype == "smith":
		var font = preload("res://Asset/Fonts/PressStart2P.ttf")
		var text = "[ Latihan: " + str(trainees) + "/5 ]"
		var font_size = int(8.0 * inv_scale) # Harus minimal 8 untuk pixel font
		var text_size = font.get_string_size(text, HORIZONTAL_ALIGNMENT_CENTER, -1, font_size)
		var text_x = -text_size.x / 2.0
		var text_y = bar_y - 8.0 * inv_scale
		# Outline hitam 1 pixel agar tajam
		var outline_offset = 1.0 * inv_scale
		for ox in [-1, 0, 1]:
			for oy in [-1, 0, 1]:
				if ox == 0 and oy == 0: continue
				draw_string(font, Vector2(text_x + ox * outline_offset, text_y + oy * outline_offset), text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, Color.BLACK)
		# Teks putih cerah agar kontras
		draw_string(font, Vector2(text_x, text_y), text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, Color.WHITE)
