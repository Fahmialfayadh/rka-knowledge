extends CanvasLayer

@onready var event_log_container = $Control/EventLog
@onready var left_vbox = $Control/LeftPanel/VBox
@onready var right_vbox = $Control/RightPanel/VBox
@onready var top_label = $Control/TopPanel/Label

var world_ref = null
var max_log_messages = 8
var _panels_built: bool = false
var _cached_labels: Dictionary = {} # Cache label agar tidak dibuat ulang setiap frame
var retro_font = preload("res://Asset/Fonts/PressStart2P.ttf")

# Variables for Time Controls
var _btn_play_pause: Button
var _btn_speed: Button
var _speed_cycle = [1.0, 2.0, 4.0, 5.0]
var _current_speed_idx = 0
var _power_buttons: Dictionary = {}

var _btn_style_normal: StyleBoxFlat
var _btn_style_hover: StyleBoxFlat
var _btn_style_active: StyleBoxFlat

# Possessed UI variables
var _possessed_panel: PanelContainer
var _possessed_img: TextureRect
var _possessed_title: Label
var _possessed_hp_label: Label
var _possessed_hp_bar: ProgressBar
var _possessed_controls: PanelContainer
var _mouse_left_lbl: Label
var _l_lbl: Label

func _ready():
	$Control.mouse_filter = Control.MOUSE_FILTER_IGNORE
	$Control.set_anchors_preset(Control.PRESET_FULL_RECT, true)
	$Control/EventLog.mouse_filter = Control.MOUSE_FILTER_IGNORE
	
	EventBus.log_event.connect(_on_log_event)
	
	# Bersihkan placeholder
	for child in left_vbox.get_children():
		child.queue_free()
	for child in right_vbox.get_children():
		child.queue_free()
		
	# --- RETRO UI STYLING (9-SLICE TEXTURE) ---
	var retro_panel = StyleBoxTexture.new()
	retro_panel.texture = preload("res://Asset/Sprites/paper_panel.png")
	
	# Margin 9-Slice (Jangan merentangkan pinggiran kertas agar sobekan tetap proporsional)
	retro_panel.texture_margin_left = 25.0
	retro_panel.texture_margin_right = 25.0
	retro_panel.texture_margin_top = 25.0
	retro_panel.texture_margin_bottom = 25.0
	
	$Control/LeftPanel.add_theme_stylebox_override("panel", retro_panel)
	$Control/RightPanel.add_theme_stylebox_override("panel", retro_panel)
	$Control/TopPanel.add_theme_stylebox_override("panel", retro_panel)
	
	# OVERRIDE LAYOUT SECARA MANUAL (Sesuai request user)
	$Control/LeftPanel.set_anchors_preset(Control.PRESET_BOTTOM_LEFT)
	$Control/LeftPanel.offset_left = 20
	$Control/LeftPanel.offset_right = 220
	$Control/LeftPanel.offset_top = -370
	$Control/LeftPanel.offset_bottom = -20
	
	$Control/RightPanel.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	$Control/RightPanel.offset_left = -220
	$Control/RightPanel.offset_right = -20
	$Control/RightPanel.offset_top = -370
	$Control/RightPanel.offset_bottom = -20
	
	# --- NEW TOP NAVIGATION FLOATING BUTTONS ---
	
	# Left Side: Time Controls
	var time_hbox = HBoxContainer.new()
	time_hbox.set_anchors_preset(Control.PRESET_TOP_LEFT, true)
	time_hbox.position = Vector2(20, 20)
	time_hbox.add_theme_constant_override("separation", 10)
	
	_btn_style_normal = StyleBoxFlat.new()
	_btn_style_normal.bg_color = Color("#e8e1dc")
	_btn_style_normal.border_width_left = 2
	_btn_style_normal.border_width_top = 2
	_btn_style_normal.border_width_right = 2
	_btn_style_normal.border_width_bottom = 2
	_btn_style_normal.border_color = Color.BLACK
	_btn_style_normal.shadow_color = Color.BLACK
	_btn_style_normal.shadow_size = 0
	_btn_style_normal.shadow_offset = Vector2(3, 3)
	_btn_style_normal.content_margin_left = 12
	_btn_style_normal.content_margin_right = 12
	_btn_style_normal.content_margin_top = 8
	_btn_style_normal.content_margin_bottom = 8
	
	_btn_style_hover = _btn_style_normal.duplicate()
	_btn_style_hover.bg_color = Color("#ffffff") # Terang saat di-hover
	
	_btn_style_active = _btn_style_normal.duplicate()
	_btn_style_active.bg_color = Color("#1e1b18")
	
	_btn_play_pause = Button.new()
	_btn_speed = Button.new()
	
	var top_font = preload("res://Asset/Fonts/CourierPrime.ttf")
	
	for b in [_btn_play_pause, _btn_speed]:
		b.add_theme_font_override("font", top_font)
		b.add_theme_font_size_override("font_size", 16)
		b.add_theme_color_override("font_color", Color("#1e1b18"))
		b.add_theme_color_override("font_hover_color", Color("#1e1b18"))
		b.add_theme_color_override("font_pressed_color", Color("#e8e1dc"))
		b.add_theme_stylebox_override("normal", _btn_style_normal)
		b.add_theme_stylebox_override("hover", _btn_style_hover)
		b.add_theme_stylebox_override("pressed", _btn_style_active)
		b.custom_minimum_size = Vector2(40, 0)
		time_hbox.add_child(b)
		
	# Logika Play/Pause Toggle
	_btn_play_pause.pressed.connect(func():
		if Engine.time_scale > 0.0:
			Engine.time_scale = 0.0
		else:
			Engine.time_scale = _speed_cycle[_current_speed_idx]
	)
	
	# Logika Fast Forward Cycle
	_btn_speed.pressed.connect(func():
		_current_speed_idx = (_current_speed_idx + 1) % _speed_cycle.size()
		Engine.time_scale = _speed_cycle[_current_speed_idx]
	)
	
	# Pindahkan top_label dari TopPanel yang disembunyikan ke time_hbox
	if top_label and top_label.get_parent():
		top_label.get_parent().remove_child(top_label)
		var time_bg = PanelContainer.new()
		time_bg.add_theme_stylebox_override("panel", _btn_style_normal)
		
		# Styling ulang agar serasi dengan tombol baru
		top_label.add_theme_font_override("font", top_font)
		top_label.add_theme_font_size_override("font_size", 16)
		top_label.add_theme_color_override("font_color", Color("#1e1b18"))
		top_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		
		time_bg.add_child(top_label)
		time_hbox.add_child(time_bg)
	
	$Control.add_child(time_hbox)
	
	# Right Side: God Powers
	var powers_hbox = HBoxContainer.new()
	powers_hbox.set_anchors_preset(Control.PRESET_TOP_RIGHT, true)
	powers_hbox.grow_horizontal = Control.GROW_DIRECTION_BEGIN
	powers_hbox.offset_top = 20
	powers_hbox.offset_right = -20
	powers_hbox.add_theme_constant_override("separation", 10)
	
	var powers = [
		["water", "💧 WATER"], ["mountain", "⛰ MOUNTAIN"],
		["grass", "🟩 ERASER"], ["bomb", "💣 BOMB"],
		["lightning", "⚡ LIGHTNING"], ["spawn_red", "🔴 RED"],
		["spawn_blue", "🔵 BLUE"], ["possess", "👻 POSSESS"]
	]
	
	for p in powers:
		var pid = p[0]
		var btn = Button.new()
		btn.text = p[1]
		btn.add_theme_font_override("font", top_font)
		btn.add_theme_font_size_override("font_size", 14)
		btn.add_theme_color_override("font_color", Color("#1e1b18"))
		btn.add_theme_color_override("font_hover_color", Color("#1e1b18"))
		btn.add_theme_color_override("font_pressed_color", Color("#e8e1dc"))
		btn.add_theme_stylebox_override("normal", _btn_style_normal)
		btn.add_theme_stylebox_override("hover", _btn_style_hover)
		btn.add_theme_stylebox_override("pressed", _btn_style_active)
		btn.pressed.connect(func():
			if world_ref:
				world_ref.active_power = pid if world_ref.active_power != pid else "none"
		)
		powers_hbox.add_child(btn)
		_power_buttons[pid] = btn
		
	$Control.add_child(powers_hbox)
	$Control/TopPanel.visible = false

	# --- POSSESSED UNIT PORTRAIT PANEL ---
	_possessed_panel = PanelContainer.new()
	var poss_bg = StyleBoxTexture.new()
	poss_bg.texture = preload("res://Asset/Sprites/Panel_Possessed.png")
	# Biarkan texture_margin 0 agar scroll teregang secara proporsional
	_possessed_panel.add_theme_stylebox_override("panel", poss_bg)
	_possessed_panel.set_anchors_preset(Control.PRESET_TOP_LEFT)
	_possessed_panel.offset_left = 20
	_possessed_panel.offset_top = 80
	_possessed_panel.offset_right = 260
	_possessed_panel.offset_bottom = 420
	_possessed_panel.visible = false
	
	var poss_vbox = VBoxContainer.new()
	poss_vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	poss_vbox.add_theme_constant_override("separation", 10)
	
	_possessed_title = Label.new()
	_possessed_title.text = "POSSESSED"
	_possessed_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_possessed_title.add_theme_font_override("font", top_font)
	_possessed_title.add_theme_font_size_override("font_size", 14)
	_possessed_title.add_theme_color_override("font_color", Color.BLACK)
	poss_vbox.add_child(_possessed_title)
	
	# Image Container
	var img_panel = PanelContainer.new()
	var img_bg = StyleBoxFlat.new()
	img_bg.bg_color = Color(0, 0, 0, 0.1) # Transparan sedikit
	img_bg.border_width_left = 1
	img_bg.border_width_top = 1
	img_bg.border_width_right = 1
	img_bg.border_width_bottom = 1
	img_bg.border_color = Color.BLACK
	img_panel.add_theme_stylebox_override("panel", img_bg)
	img_panel.custom_minimum_size = Vector2(140, 140) # Dibesarkan lagi sesuai permintaan
	img_panel.size_flags_horizontal = Control.SIZE_SHRINK_CENTER # Jangan meregang ke samping
	
	_possessed_img = TextureRect.new()
	_possessed_img.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_possessed_img.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	img_panel.add_child(_possessed_img)
	poss_vbox.add_child(img_panel)
	
	# HP Info Row
	var hp_vbox = VBoxContainer.new()
	hp_vbox.add_theme_constant_override("separation", 5)
	
	var hp_hbox = HBoxContainer.new()
	var hp_txt = Label.new()
	hp_txt.text = "HP"
	hp_txt.add_theme_font_override("font", top_font)
	hp_txt.add_theme_font_size_override("font_size", 11)
	hp_txt.add_theme_color_override("font_color", Color.BLACK)
	hp_hbox.add_child(hp_txt)
	
	var hp_spacer = Control.new()
	hp_spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	hp_hbox.add_child(hp_spacer)
	
	_possessed_hp_label = Label.new()
	_possessed_hp_label.text = "100/100"
	_possessed_hp_label.add_theme_font_override("font", top_font)
	_possessed_hp_label.add_theme_font_size_override("font_size", 11)
	_possessed_hp_label.add_theme_color_override("font_color", Color.BLACK)
	hp_hbox.add_child(_possessed_hp_label)
	
	hp_vbox.add_child(hp_hbox)
	
	# HP Bar
	_possessed_hp_bar = ProgressBar.new()
	_possessed_hp_bar.custom_minimum_size = Vector2(140, 10)
	_possessed_hp_bar.show_percentage = false
	var bar_bg = StyleBoxFlat.new()
	bar_bg.bg_color = Color.WHITE
	bar_bg.border_width_left = 1
	bar_bg.border_width_top = 1
	bar_bg.border_width_right = 1
	bar_bg.border_width_bottom = 1
	bar_bg.border_color = Color.BLACK
	var bar_fill = StyleBoxFlat.new()
	bar_fill.bg_color = Color("#c42828")
	bar_fill.border_width_left = 1
	bar_fill.border_width_top = 1
	bar_fill.border_width_right = 1
	bar_fill.border_width_bottom = 1
	bar_fill.border_color = Color.TRANSPARENT # Margin in fill
	_possessed_hp_bar.add_theme_stylebox_override("background", bar_bg)
	_possessed_hp_bar.add_theme_stylebox_override("fill", bar_fill)
	
	hp_vbox.add_child(_possessed_hp_bar)
	poss_vbox.add_child(hp_vbox)
	
	# Margin Internal
	var main_margin = MarginContainer.new()
	main_margin.add_theme_constant_override("margin_left", 35)
	main_margin.add_theme_constant_override("margin_right", 35)
	main_margin.add_theme_constant_override("margin_top", 105) # Disesuaikan proporsi
	main_margin.add_theme_constant_override("margin_bottom", 80) # Disesuaikan proporsi
	main_margin.add_child(poss_vbox)
	
	_possessed_panel.add_child(main_margin)
	$Control.add_child(_possessed_panel)
	
	# --- POSSESSED FLOATING CONTROLS (BOTTOM LEFT) ---
	_possessed_controls = PanelContainer.new()
	var clear_panel = StyleBoxFlat.new()
	clear_panel.bg_color = Color(0,0,0, 0.4) # Semi transparan hitam
	clear_panel.corner_radius_top_left = 10
	clear_panel.corner_radius_top_right = 10
	clear_panel.corner_radius_bottom_left = 10
	clear_panel.corner_radius_bottom_right = 10
	clear_panel.content_margin_left = 15
	clear_panel.content_margin_right = 15
	clear_panel.content_margin_top = 10
	clear_panel.content_margin_bottom = 10
	
	_possessed_controls.add_theme_stylebox_override("panel", clear_panel)
	_possessed_controls.set_anchors_preset(Control.PRESET_BOTTOM_LEFT)
	_possessed_controls.offset_left = 240
	_possessed_controls.offset_right = 600
	_possessed_controls.offset_top = -80
	_possessed_controls.offset_bottom = -20
	_possessed_controls.visible = false
	
	var ctrl_hbox = HBoxContainer.new()
	ctrl_hbox.alignment = BoxContainer.ALIGNMENT_CENTER
	ctrl_hbox.add_theme_constant_override("separation", 20)
	
	# WASD Keyboard Layout
	var wasd_grid = GridContainer.new()
	wasd_grid.columns = 3
	wasd_grid.add_theme_constant_override("h_separation", 3)
	wasd_grid.add_theme_constant_override("v_separation", 3)
	
	var key_style = StyleBoxFlat.new()
	key_style.bg_color = Color(0.2, 0.2, 0.2)
	key_style.border_color = Color.BLACK
	key_style.border_width_bottom = 3
	key_style.corner_radius_top_left = 3
	key_style.corner_radius_top_right = 3
	key_style.corner_radius_bottom_left = 3
	key_style.corner_radius_bottom_right = 3
	
	var create_key = func(txt: String):
		var p = PanelContainer.new()
		p.add_theme_stylebox_override("panel", key_style)
		p.custom_minimum_size = Vector2(20, 20)
		if txt == "":
			p.modulate.a = 0
			return p
		var l = Label.new()
		l.text = txt
		if retro_font: l.add_theme_font_override("font", retro_font)
		l.add_theme_font_size_override("font_size", 8)
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		p.add_child(l)
		return p
		
	wasd_grid.add_child(create_key.call(""))
	wasd_grid.add_child(create_key.call("W"))
	wasd_grid.add_child(create_key.call(""))
	wasd_grid.add_child(create_key.call("A"))
	wasd_grid.add_child(create_key.call("S"))
	wasd_grid.add_child(create_key.call("D"))
	
	var wasd_vbox = VBoxContainer.new()
	wasd_vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	wasd_vbox.add_child(wasd_grid)
	
	var lbl_move = Label.new()
	lbl_move.text = "Gerak"
	lbl_move.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if retro_font: lbl_move.add_theme_font_override("font", retro_font)
	lbl_move.add_theme_font_size_override("font_size", 6)
	wasd_vbox.add_child(lbl_move)
	
	ctrl_hbox.add_child(wasd_vbox)
	
	# Mouse Icon Left (Collect / Slash)
	var mouse_left_vbox = VBoxContainer.new()
	mouse_left_vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	
	var mouse_left_icon = TextureRect.new()
	mouse_left_icon.texture = preload("res://Asset/Sprites/hud_mouse_left.png")
	mouse_left_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	mouse_left_icon.custom_minimum_size = Vector2(25, 35)
	mouse_left_icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	mouse_left_vbox.add_child(mouse_left_icon)
	
	_mouse_left_lbl = Label.new()
	_mouse_left_lbl.text = "Ambil"
	_mouse_left_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if retro_font: _mouse_left_lbl.add_theme_font_override("font", retro_font)
	_mouse_left_lbl.add_theme_font_size_override("font_size", 6)
	mouse_left_vbox.add_child(_mouse_left_lbl)
	
	ctrl_hbox.add_child(mouse_left_vbox)

	# Mouse Icon Right (Keluar)
	var mouse_right_vbox = VBoxContainer.new()
	mouse_right_vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	
	var mouse_right_icon = TextureRect.new()
	mouse_right_icon.texture = preload("res://Asset/Sprites/hud_mouse.png")
	mouse_right_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	mouse_right_icon.custom_minimum_size = Vector2(25, 35)
	mouse_right_icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	mouse_right_vbox.add_child(mouse_right_icon)
	
	var mouse_right_lbl = Label.new()
	mouse_right_lbl.text = "Keluar"
	mouse_right_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if retro_font: mouse_right_lbl.add_theme_font_override("font", retro_font)
	mouse_right_lbl.add_theme_font_size_override("font_size", 6)
	mouse_right_vbox.add_child(mouse_right_lbl)
	
	ctrl_hbox.add_child(mouse_right_vbox)
	
	# K and L
	var kl_vbox = VBoxContainer.new()
	kl_vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	kl_vbox.add_theme_constant_override("separation", 5)
	
	var k_hbox = HBoxContainer.new()
	k_hbox.add_child(create_key.call("K"))
	var k_lbl = Label.new()
	k_lbl.text = "Dash"
	if retro_font: k_lbl.add_theme_font_override("font", retro_font)
	k_lbl.add_theme_font_size_override("font_size", 8)
	k_hbox.add_child(k_lbl)
	
	var l_hbox = HBoxContainer.new()
	l_hbox.add_child(create_key.call("L"))
	_l_lbl = Label.new()
	_l_lbl.text = "Ambil"
	if retro_font: _l_lbl.add_theme_font_override("font", retro_font)
	_l_lbl.add_theme_font_size_override("font_size", 8)
	l_hbox.add_child(_l_lbl)
	
	kl_vbox.add_child(k_hbox)
	kl_vbox.add_child(l_hbox)
	
	ctrl_hbox.add_child(kl_vbox)
	
	_possessed_controls.add_child(ctrl_hbox)
	$Control.add_child(_possessed_controls)

func _process(delta):
	if not world_ref:
		world_ref = get_tree().current_scene
		return
		
	# Update label tombol berdasarkan status Engine.time_scale
	if Engine.time_scale == 0.0:
		_btn_play_pause.text = " > "
	else:
		_btn_play_pause.text = " || "
	_btn_speed.text = " %dx " % int(_speed_cycle[_current_speed_idx])
		
	top_label.text = "Time: %d s" % int(world_ref.elapsed_time)
	
	# Update active power button highlight
	for pid in _power_buttons.keys():
		var btn = _power_buttons[pid]
		if world_ref.active_power == pid:
			btn.add_theme_stylebox_override("normal", _btn_style_active)
			btn.add_theme_stylebox_override("hover", _btn_style_active)
			btn.add_theme_color_override("font_color", Color("#e8e1dc"))
			btn.add_theme_color_override("font_hover_color", Color("#e8e1dc"))
		else:
			btn.add_theme_stylebox_override("normal", _btn_style_normal)
			btn.add_theme_stylebox_override("hover", _btn_style_hover)
			btn.add_theme_color_override("font_color", Color("#1e1b18"))
			btn.add_theme_color_override("font_hover_color", Color("#1e1b18"))
		btn.modulate = Color.WHITE

	# Update Possessed UI
	if world_ref.possessed_unit and is_instance_valid(world_ref.possessed_unit) and world_ref.possessed_unit.hp > 0:
		_possessed_panel.visible = true
		_possessed_controls.visible = true
		var u = world_ref.possessed_unit
		
		# Update HP di label dan bar
		var current_hp = u.hp if "hp" in u else 100
		var max_hp = u.max_hp if "max_hp" in u else Config.UNIT_MAX_HP
		_possessed_hp_label.text = str(int(current_hp)) + "/" + str(int(max_hp))
		_possessed_hp_bar.max_value = max_hp
		_possessed_hp_bar.value = current_hp
		
		# Set image based on unit
		var is_custom_portrait = false
		var tex
		if u.armed:
			if u.kingdom == "red":
				tex = preload("res://Asset/Sprites/Red_Armored_Possessed (1).png")
				is_custom_portrait = true
			else:
				tex = preload("res://Asset/Sprites/Blue_Armored_Possessed.png")
				is_custom_portrait = true
		elif u.has_tool:
			tex = preload("res://Asset/Sprites/iron_worker_red.png") if u.kingdom == "red" else preload("res://Asset/Sprites/bluepeople.png")
		else:
			if u.kingdom == "blue":
				tex = preload("res://Asset/Sprites/Blue_Biasa_Possessed.png")
				is_custom_portrait = true
			else:
				tex = preload("res://Asset/Sprites/Red_Biasa_Possessed.png")
				is_custom_portrait = true
			
		if is_custom_portrait:
			_possessed_img.texture = tex
		else:
			# Gunakan AtlasTexture untuk memotong setengah badan (crop kaki) untuk sprite bawaan
			var atlas = AtlasTexture.new()
			atlas.atlas = tex
			atlas.region = Rect2(0, 0, tex.get_width(), tex.get_height() * 0.6) # Hanya 60% bagian atas
			_possessed_img.texture = atlas
		
		# Dynamically update the controls helper labels text
		if is_instance_valid(_mouse_left_lbl) and is_instance_valid(_l_lbl):
			if u.armed:
				_mouse_left_lbl.text = "Serang"
				_l_lbl.text = "Slash"
			else:
				_mouse_left_lbl.text = "Ambil"
				_l_lbl.text = "Ambil"
	else:
		_possessed_panel.visible = false
		_possessed_controls.visible = false

	if not _panels_built:
		_build_panels()
		_panels_built = true
	
	_refresh_panel("red", delta)
	_refresh_panel("blue", delta)

func _build_panels():
	_build_kingdom_panel(left_vbox, "red", "Red Dominion")
	_build_kingdom_panel(right_vbox, "blue", "Blue Covenant")

func _build_kingdom_panel(container: VBoxContainer, kname: String, title: String):
	# Judul
	var lbl_title = Label.new()
	var icon = "X " if kname == "red" else "O " # Icon retro sederhana
	lbl_title.text = icon + title
	lbl_title.add_theme_color_override("font_color", Color.RED if kname == "red" else Color.CORNFLOWER_BLUE)
	lbl_title.add_theme_font_override("font", retro_font)
	lbl_title.add_theme_font_size_override("font_size", 10)
	lbl_title.add_theme_color_override("font_outline_color", Color.BLACK)
	lbl_title.add_theme_constant_override("outline_size", 4)
	container.add_child(lbl_title)
	
	# Alert label (SURVIVAL / UNDER ATTACK)
	var lbl_alert = Label.new()
	lbl_alert.add_theme_font_override("font", retro_font)
	lbl_alert.add_theme_font_size_override("font_size", 8)
	lbl_alert.add_theme_color_override("font_outline_color", Color.BLACK)
	lbl_alert.add_theme_constant_override("outline_size", 4)
	lbl_alert.visible = false
	container.add_child(lbl_alert)
	_cached_labels[kname + "_alert"] = lbl_alert
	
	# Focus label
	var lbl_focus = Label.new()
	lbl_focus.add_theme_font_override("font", retro_font)
	lbl_focus.add_theme_font_size_override("font_size", 8)
	lbl_focus.add_theme_color_override("font_outline_color", Color.BLACK)
	lbl_focus.add_theme_constant_override("outline_size", 4)
	container.add_child(lbl_focus)
	_cached_labels[kname + "_focus"] = lbl_focus
	
	var sep = HSeparator.new()
	container.add_child(sep)
	
	# Stats labels (9 baris)
	var stat_keys = ["base_hp", "pop", "workers", "armed", "wood", "iron", "food", "houses", "smiths"]
	for key in stat_keys:
		var lbl = Label.new()
		lbl.add_theme_font_override("font", retro_font)
		lbl.add_theme_font_size_override("font_size", 8)
		lbl.add_theme_color_override("font_outline_color", Color.BLACK)
		lbl.add_theme_constant_override("outline_size", 4)
		container.add_child(lbl)
		_cached_labels[kname + "_" + key] = lbl
	
	var sep2 = HSeparator.new()
	container.add_child(sep2)
	
	# Urgency bars
	for ukey in ["food", "wood", "iron"]:
		var lbl_u = Label.new()
		lbl_u.add_theme_font_override("font", retro_font)
		lbl_u.add_theme_font_size_override("font_size", 8)
		lbl_u.add_theme_color_override("font_outline_color", Color.BLACK)
		lbl_u.add_theme_constant_override("outline_size", 4)
		container.add_child(lbl_u)
		_cached_labels[kname + "_u_" + ukey + "_lbl"] = lbl_u
		
		var pb = ProgressBar.new()
		pb.max_value = 100.0
		pb.custom_minimum_size = Vector2(0, 12) # Sedikit lebih tebal
		pb.show_percentage = false
		
		var colors = {"food": Color.ORANGE, "wood": Color.SADDLE_BROWN, "iron": Color.SLATE_GRAY}
		
		# Gaya isi bar (Fill) dengan tekstur putih silinder yang diwarnai
		var sb_fill = StyleBoxTexture.new()
		sb_fill.texture = preload("res://Asset/Sprites/bar_fill.png")
		sb_fill.texture_margin_left = 4.0
		sb_fill.texture_margin_right = 4.0
		sb_fill.texture_margin_top = 4.0
		sb_fill.texture_margin_bottom = 4.0
		sb_fill.modulate_color = colors[ukey] # Pewarnaan otomatis
		pb.add_theme_stylebox_override("fill", sb_fill)
		
		# Gaya latar belakang bar (BG) dengan tekstur cekung (Inset Shadow)
		var sb_bg = StyleBoxTexture.new()
		sb_bg.texture = preload("res://Asset/Sprites/bar_bg.png")
		sb_bg.texture_margin_left = 4.0
		sb_bg.texture_margin_right = 4.0
		sb_bg.texture_margin_top = 4.0
		sb_bg.texture_margin_bottom = 4.0
		pb.add_theme_stylebox_override("background", sb_bg)
		
		container.add_child(pb)
		_cached_labels[kname + "_u_" + ukey + "_pb"] = pb

func _refresh_panel(kname: String, delta: float):
	if not world_ref.kingdoms.has(kname):
		return
	var k = world_ref.kingdoms[kname]
	
	# Alert
	var alert_lbl = _cached_labels.get(kname + "_alert")
	if alert_lbl:
		if k.survival_mode:
			alert_lbl.text = "☠ SURVIVAL MODE"
			alert_lbl.add_theme_color_override("font_color", Color.PURPLE)
			alert_lbl.visible = true
		elif k.base_under_attack:
			alert_lbl.text = "⚠ BASE UNDER ATTACK"
			alert_lbl.add_theme_color_override("font_color", Color.ORANGE_RED)
			alert_lbl.visible = true
		else:
			alert_lbl.visible = false
	
	# Focus (dengan efek kedip-kedip / pulsating warna jika Assault)
	var focus_lbl = _cached_labels.get(kname + "_focus")
	if focus_lbl:
		focus_lbl.text = "FOCUS: " + k.focus
		if k.focus == "ASSAULT":
			focus_lbl.add_theme_color_override("font_color", Color.RED)
			# Efek membesar-mengecil berdenyut
			var pulse = 1.0 + sin(Time.get_ticks_msec() * 0.005) * 0.2
			focus_lbl.scale = Vector2(pulse, pulse)
		else:
			focus_lbl.add_theme_color_override("font_color", Color.WHITE)
			focus_lbl.scale = Vector2.ONE
	
	# Stats
	var base_hp_val = k.base_node.hp if (k.base_node and is_instance_valid(k.base_node)) else 0
	var stat_values = {
		"base_hp": "Base HP: %d/%d" % [int(base_hp_val), Config.BASE_MAX_HP],
		"pop": "Population: %d" % k.pop,
		"workers": "Workers: %d" % (k.pop - k.armed),
		"armed": "Armed: %d" % k.armed,
		"wood": "Wood: %d" % k.wood,
		"iron": "Iron: %d" % k.iron,
		"food": "Food: %d" % k.food,
		"houses": "Houses: %d" % k.houses,
		"smiths": "Smiths: %d" % k.smiths,
	}
	for key in stat_values:
		var lbl = _cached_labels.get(kname + "_" + key)
		if lbl:
			lbl.text = stat_values[key]
	
	# Urgency
	for ukey in ["food", "wood", "iron"]:
		var u_val = 0.0
		if ukey == "food": u_val = k.u_food
		elif ukey == "wood": u_val = k.u_wood
		elif ukey == "iron": u_val = k.u_iron
		
		var lbl_u = _cached_labels.get(kname + "_u_" + ukey + "_lbl")
		if lbl_u:
			lbl_u.text = ukey.capitalize() + " Urgency"
		var pb = _cached_labels.get(kname + "_u_" + ukey + "_pb")
		if pb:
			# Tween manual pakai lerp biar pergerakan barnya mulus
			pb.value = lerp(pb.value, float(clamp(u_val, 0, 100)), delta * 5.0)

func _on_log_event(message: String, kingdom: String):
	var lbl = Label.new()
	lbl.text = "[%s] %s" % [kingdom.to_upper(), message]
	lbl.add_theme_color_override("font_color", Color.RED if kingdom == "red" else Color.CORNFLOWER_BLUE)
	lbl.add_theme_font_override("font", retro_font)
	lbl.add_theme_font_size_override("font_size", 8)
	lbl.add_theme_color_override("font_outline_color", Color.BLACK)
	lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	event_log_container.add_child(lbl)
	event_log_container.move_child(lbl, 0) # Taruh di paling atas
	
	# Efek Slide-In (Masuk dari kiri)
	var t_pos = lbl.position
	lbl.position.x -= 100
	lbl.modulate.a = 0.0
	var tw = create_tween()
	tw.tween_property(lbl, "position:x", t_pos.x, 0.3).set_trans(Tween.TRANS_SINE)
	tw.parallel().tween_property(lbl, "modulate:a", 1.0, 0.3)
	
	# HILANG OTOMATIS SETELAH 3 DETIK
	tw.tween_interval(3.0)
	tw.tween_property(lbl, "modulate:a", 0.0, 0.5)
	tw.tween_callback(lbl.queue_free)
	
	if event_log_container.get_child_count() > 5:
		var oldest = event_log_container.get_child(event_log_container.get_child_count() - 1)
		if is_instance_valid(oldest):
			oldest.queue_free()
