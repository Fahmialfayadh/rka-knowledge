extends Node

# Signal global untuk mencatat kejadian perang
signal log_event(message: String, kingdom: String)
signal shake_camera(magnitude: float, duration: float)

func spawn_hit_particles(pos: Vector2, color: Color):
	var p = CPUParticles2D.new()
	p.emitting = true
	p.one_shot = true
	p.explosiveness = 0.9
	p.direction = Vector2(0, -1)
	p.spread = 180
	p.gravity = Vector2(0, 0)
	p.initial_velocity_min = 50.0
	p.initial_velocity_max = 100.0
	p.scale_amount_min = 2.0
	p.scale_amount_max = 4.0
	p.color = color
	p.amount = 10
	p.lifetime = 0.3
	p.global_position = pos
	get_tree().current_scene.add_child(p)
	
	# Hapus otomatis setelah selesai
	var t = get_tree().create_timer(0.4)
	t.timeout.connect(p.queue_free)

func spawn_floating_text(pos: Vector2, text: String, color: Color):
	var ftext = preload("res://Scripts/FloatingText.gd").new()
	ftext.text = text
	ftext.add_theme_color_override("font_color", color)
	ftext.global_position = pos + Vector2(-10, -10) # Offset sedikit ke atas
	ftext.z_index = 100 # Pastikan selalu di atas
	get_tree().current_scene.add_child(ftext)

func spawn_blood_stain(pos: Vector2):
	var s = Polygon2D.new()
	s.color = Color(0.5, 0.0, 0.0, 0.8) # Darah merah gelap transparan
	
	# Bikin bentuk bercak acak
	var points = PackedVector2Array()
	var sides = randi_range(5, 8)
	for i in range(sides):
		var angle = (i / float(sides)) * PI * 2
		var radius = randf_range(4.0, 10.0)
		points.append(Vector2(cos(angle), sin(angle)) * radius)
	
	s.polygon = points
	s.global_position = pos
	s.z_index = -2 # Paling bawah, di atas background tapi di bawah unit
	
	get_tree().current_scene.add_child(s)
	
	# Hilang perlahan setelah 20 detik agar tidak bikin lag/memori penuh
	var tw = s.create_tween()
	tw.tween_interval(20.0)
	tw.tween_property(s, "color", Color(0.5, 0.0, 0.0, 0.0), 5.0)
	tw.tween_callback(s.queue_free)

var _cached_glow_tex: GradientTexture2D = null

func _get_glow_tex() -> GradientTexture2D:
	if _cached_glow_tex: return _cached_glow_tex
	var grad = Gradient.new()
	grad.set_color(0, Color(1, 1, 1, 1))
	grad.set_color(1, Color(1, 1, 1, 0))
	_cached_glow_tex = GradientTexture2D.new()
	_cached_glow_tex.gradient = grad
	_cached_glow_tex.fill = GradientTexture2D.FILL_RADIAL
	_cached_glow_tex.fill_from = Vector2(0.5, 0.5)
	_cached_glow_tex.fill_to = Vector2(0.5, 0.0)
	_cached_glow_tex.width = 64
	_cached_glow_tex.height = 64
	return _cached_glow_tex

func spawn_falling_bomb(target_pos: Vector2, duration: float):
	var shadow = Polygon2D.new()
	var s_points = PackedVector2Array()
	for i in range(16):
		var a = (i / 16.0) * TAU
		s_points.append(Vector2(cos(a) * 30.0, sin(a) * 15.0))
	shadow.polygon = s_points
	shadow.color = Color(0, 0, 0, 0.0)
	shadow.global_position = target_pos
	shadow.z_index = -1
	get_tree().current_scene.add_child(shadow)
	
	var tw_shadow = shadow.create_tween()
	tw_shadow.tween_property(shadow, "color", Color(0, 0, 0, 0.6), duration)
	tw_shadow.parallel().tween_property(shadow, "scale", Vector2(1.5, 1.5), duration)
	tw_shadow.tween_callback(shadow.queue_free)
	
	var meteor = Node2D.new()
	var start_pos = Vector2(target_pos.x + randf_range(-100, 100), -400)
	meteor.global_position = start_pos
	meteor.z_index = 100
	get_tree().current_scene.add_child(meteor)
	
	var bomb_sprite = Sprite2D.new()
	bomb_sprite.texture = load("res://Asset/Sprites/Bomb.png")
	bomb_sprite.scale = Vector2(1.5, 1.5) # Sedikit diperbesar agar jelas
	meteor.add_child(bomb_sprite)
	
	var light = PointLight2D.new()
	light.texture = _get_glow_tex()
	light.color = Color(4.0, 2.0, 0.5, 1.0)
	light.texture_scale = 3.0
	meteor.add_child(light)
	
	var trail = CPUParticles2D.new()
	trail.texture = _get_glow_tex()
	trail.emission_shape = CPUParticles2D.EMISSION_SHAPE_SPHERE
	trail.emission_sphere_radius = 10.0
	trail.gravity = Vector2(0, -50)
	trail.lifetime = 0.4
	trail.amount = 60
	trail.scale_amount_min = 0.5
	trail.scale_amount_max = 1.0
	trail.color = Color(3.0, 1.0, 0.0, 1.0)
	meteor.add_child(trail)
	
	var tw_meteor = meteor.create_tween()
	tw_meteor.tween_property(meteor, "global_position", target_pos, duration).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	tw_meteor.parallel().tween_property(bomb_sprite, "rotation", PI * 4, duration) # Berputar saat jatuh
	tw_meteor.tween_callback(meteor.queue_free)

func spawn_explosion_vfx(pos: Vector2):
	var tex = _get_glow_tex()
	
	var light = PointLight2D.new()
	light.texture = tex
	light.color = Color(4.0, 2.0, 0.5, 1.0)
	light.texture_scale = 8.0
	light.global_position = pos
	light.z_index = 50
	get_tree().current_scene.add_child(light)
	var tw_l = light.create_tween()
	tw_l.tween_property(light, "texture_scale", 0.1, 0.4).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw_l.parallel().tween_property(light, "color", Color(4.0, 2.0, 0.5, 0.0), 0.4)
	tw_l.tween_callback(light.queue_free)
	
	var fire = CPUParticles2D.new()
	fire.texture = tex
	fire.emitting = true
	fire.one_shot = true
	fire.explosiveness = 0.95
	fire.spread = 180
	fire.gravity = Vector2(0, 0)
	fire.initial_velocity_min = 200.0
	fire.initial_velocity_max = 300.0
	fire.damping_min = 300.0
	fire.damping_max = 500.0
	fire.scale_amount_min = 1.0
	fire.scale_amount_max = 2.5
	fire.color = Color(4.0, 1.5, 0.0, 1.0)
	fire.amount = 100
	fire.lifetime = 0.6
	fire.global_position = pos
	fire.z_index = 51
	get_tree().current_scene.add_child(fire)
	get_tree().create_timer(1.0).timeout.connect(fire.queue_free)
	
	# Scorch mark (Crater bolong hitam)
	var scorch = Polygon2D.new()
	var s_points = PackedVector2Array()
	for i in range(16):
		var a = (i / 16.0) * TAU
		var r = randf_range(40.0, 60.0)
		s_points.append(Vector2(cos(a), sin(a)) * r)
	scorch.polygon = s_points
	scorch.color = Color(0.02, 0.02, 0.02, 0.9) # Hitam pekat menyerupai lubang
	scorch.global_position = pos
	scorch.z_index = -3
	get_tree().current_scene.add_child(scorch)
	var tw_s = scorch.create_tween()
	tw_s.tween_interval(10.0)
	tw_s.tween_property(scorch, "color", Color(0.02, 0.02, 0.02, 0.0), 3.0)
	tw_s.tween_callback(scorch.queue_free)
	
	# Debu tipis melayang di atas kawah (Lingering smoke)
	var crater_dust = CPUParticles2D.new()
	crater_dust.texture = tex
	crater_dust.emitting = true
	crater_dust.one_shot = true
	crater_dust.explosiveness = 0.0 # Emisi pelan-pelan
	crater_dust.spread = 180
	crater_dust.gravity = Vector2(0, -15) # Melayang naik
	crater_dust.initial_velocity_min = 5.0
	crater_dust.initial_velocity_max = 20.0
	crater_dust.scale_amount_min = 0.3
	crater_dust.scale_amount_max = 1.0
	crater_dust.color = Color(1.0, 0.5, 0.2, 0.4) # Jingga tipis membara
	crater_dust.amount = 40
	crater_dust.lifetime = 5.0 # Tahan 5 detik
	crater_dust.global_position = pos
	crater_dust.z_index = 52
	get_tree().current_scene.add_child(crater_dust)
	get_tree().create_timer(6.0).timeout.connect(crater_dust.queue_free)

func spawn_lightning_vfx(pos: Vector2):
	var tex = _get_glow_tex()
	
	var light = PointLight2D.new()
	light.texture = tex
	light.color = Color(2.0, 4.0, 5.0, 1.0)
	light.texture_scale = 10.0
	light.global_position = pos
	light.z_index = 100
	get_tree().current_scene.add_child(light)
	var tw_l = light.create_tween()
	tw_l.tween_property(light, "texture_scale", 0.1, 0.2)
	tw_l.parallel().tween_property(light, "color", Color(2.0, 4.0, 5.0, 0.0), 0.2)
	tw_l.tween_callback(light.queue_free)
	
	var bolt = Sprite2D.new()
	var tex_bolt = load("res://Asset/Sprites/Lightning.png")
	bolt.texture = tex_bolt
	# Pivot di bagian bawah agar tepat menyambar posisi mouse
	bolt.offset = Vector2(0, -tex_bolt.get_height() / 2.0)
	bolt.global_position = pos
	bolt.z_index = 100
	
	# Tambahkan warna HDR agar menyala terang
	bolt.modulate = Color(2.0, 2.0, 3.0, 1.0) 
	get_tree().current_scene.add_child(bolt)
	
	var tw_bolt = bolt.create_tween()
	tw_bolt.tween_property(bolt, "scale", Vector2(1.2, 1.0), 0.05)
	tw_bolt.tween_property(bolt, "scale", Vector2(0.2, 1.0), 0.15)
	tw_bolt.parallel().tween_property(bolt, "modulate:a", 0.0, 0.15)
	tw_bolt.tween_callback(bolt.queue_free)
	
	var sparks = CPUParticles2D.new()
	sparks.texture = tex
	sparks.emitting = true
	sparks.one_shot = true
	sparks.explosiveness = 0.95
	sparks.spread = 180
	sparks.gravity = Vector2(0, 300)
	sparks.initial_velocity_min = 100.0
	sparks.initial_velocity_max = 300.0
	sparks.scale_amount_min = 0.2
	sparks.scale_amount_max = 0.5
	sparks.color = Color(2.0, 4.0, 5.0, 1.0)
	sparks.amount = 30
	sparks.lifetime = 0.5
	sparks.global_position = pos
	sparks.z_index = 102
	get_tree().current_scene.add_child(sparks)
	get_tree().create_timer(0.6).timeout.connect(sparks.queue_free)
	
	var flash = ColorRect.new()
	flash.color = Color(1, 1, 1, 0.6)
	flash.set_anchors_preset(Control.PRESET_FULL_RECT)
	flash.z_index = 200
	get_tree().current_scene.add_child(flash)
	
	var tw_f = flash.create_tween()
	tw_f.tween_property(flash, "color", Color(1, 1, 1, 0), 0.15)
	tw_f.tween_callback(flash.queue_free)

func spawn_building_vfx(pos: Vector2, btype: String):
	var tex = _get_glow_tex()
	
	var light = PointLight2D.new()
	light.texture = tex
	light.color = Color(3.0, 2.5, 1.5, 1.0)
	light.texture_scale = 3.0 if btype != "base" else 6.0
	light.global_position = pos
	light.z_index = 50
	get_tree().current_scene.add_child(light)
	var tw_l = light.create_tween()
	tw_l.tween_property(light, "texture_scale", 0.1, 0.5).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw_l.parallel().tween_property(light, "color", Color(3.0, 2.5, 1.5, 0.0), 0.5)
	tw_l.tween_callback(light.queue_free)
	
	shake_camera.emit(2.0, 0.2)

func spawn_pierce_dash_vfx(pos: Vector2, dash_dir: Vector2):
	var slash = Line2D.new()
	slash.default_color = Color(2.0, 4.0, 4.0, 1.0) # Cyan lurus
	slash.width = 15.0
	slash.z_index = 100
	slash.add_point(pos)
	slash.add_point(pos + dash_dir * 120.0) # Garis tembus 120px
	get_tree().current_scene.add_child(slash)
	
	var tw = slash.create_tween()
	tw.tween_property(slash, "width", 0.0, 0.2)
	tw.parallel().tween_property(slash, "default_color:a", 0.0, 0.2)
	tw.tween_callback(slash.queue_free)

func spawn_dash_slash_vfx(pos: Vector2, dash_dir: Vector2):
	var slash = Line2D.new()
	slash.default_color = Color(3.0, 4.0, 4.0, 1.0) # HDR Putih Kebiruan (Sword Glow)
	slash.width = 12.0 # Lebih tipis layaknya pedang normal
	slash.z_index = 100
	
	var steps = 12
	var angle = dash_dir.angle()
	# Bentuk sabit jarak dekat
	for i in range(steps + 1):
		var t = (float(i) / steps) - 0.5
		var a = angle + t * PI * 0.8
		var r = 18.0 # Jarak pedang pendek (18px)
		slash.add_point(Vector2(cos(a), sin(a)) * r)
		
	slash.global_position = pos + dash_dir * 12.0
	get_tree().current_scene.add_child(slash)
	
	var tw = slash.create_tween()
	tw.tween_property(slash, "width", 0.0, 0.15)
	tw.parallel().tween_property(slash, "default_color:a", 0.0, 0.15)
	tw.parallel().tween_property(slash, "scale", Vector2(1.5, 1.5), 0.15)
	tw.parallel().tween_property(slash, "global_position", slash.global_position + dash_dir * 10.0, 0.15)
	tw.tween_callback(slash.queue_free)
