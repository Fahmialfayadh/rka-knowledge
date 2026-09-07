extends Control

var cloud_nodes = []
var main_vbox: VBoxContainer
var pregame_box: Control
var pop_red: int = 15
var pop_blue: int = 15
var lbl_pop_red: Label
var lbl_pop_blue: Label

func _ready():
	# Latar Belakang (Map dengan warna agak gelap)
	var bg = Sprite2D.new()
	bg.texture = preload("res://Asset/Sprites/Map.PNG")
	bg.centered = false
	var screen_size = get_viewport_rect().size
	var tex_size = bg.texture.get_size()
	if tex_size.x > 0:
		bg.scale = Vector2(screen_size.x / tex_size.x, screen_size.y / tex_size.y)
	bg.modulate = Color(0.6, 0.6, 0.7) # Agak gelap kebiruan
	add_child(bg)
	
	# Awan Bergerak (Atmosphere Juice)
	for i in range(10):
		var cloud = Polygon2D.new()
		cloud.color = Color(1.0, 1.0, 1.0, randf_range(0.1, 0.3)) # Putih transparan
		
		# Bikin bentuk awan gumpalan acak
		var points = PackedVector2Array()
		for j in range(8):
			var angle = (j / 8.0) * PI * 2
			var radius = randf_range(50.0, 200.0)
			points.append(Vector2(cos(angle), sin(angle)) * radius)
		cloud.polygon = points
		cloud.global_position = Vector2(randf_range(0, screen_size.x), randf_range(0, screen_size.y))
		add_child(cloud)
		cloud_nodes.append(cloud)
	
	# UI Container
	var center = CenterContainer.new()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(center)
	
	main_vbox = VBoxContainer.new()
	main_vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	main_vbox.add_theme_constant_override("separation", 30)
	center.add_child(main_vbox)
	
	var retro_font = preload("res://Asset/Fonts/PressStart2P.ttf")
	
	# Wrapper untuk Judul & Subjudul agar posisinya bisa dimanipulasi tanpa merusak layout VBox
	var title_wrapper = Control.new()
	title_wrapper.custom_minimum_size = Vector2(800, 150)
	main_vbox.add_child(title_wrapper)
	
	var title_box = VBoxContainer.new()
	title_box.set_anchors_preset(Control.PRESET_FULL_RECT)
	title_box.alignment = BoxContainer.ALIGNMENT_CENTER
	title_wrapper.add_child(title_box)
	
	# Judul Game
	var lbl_title = Label.new()
	lbl_title.text = "WARID"
	lbl_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if retro_font: lbl_title.add_theme_font_override("font", retro_font)
	lbl_title.add_theme_font_size_override("font_size", 80)
	lbl_title.add_theme_color_override("font_color", Color(0.9, 0.2, 0.2)) # Merah Epik
	lbl_title.add_theme_color_override("font_shadow_color", Color.BLACK)
	lbl_title.add_theme_constant_override("shadow_offset_x", 8)
	lbl_title.add_theme_constant_override("shadow_offset_y", 8)
	lbl_title.add_theme_constant_override("outline_size", 10)
	lbl_title.add_theme_color_override("font_outline_color", Color.BLACK)
	title_box.add_child(lbl_title)
	
	# Subjudul
	var lbl_sub = Label.new()
	lbl_sub.text = "War of Farid"
	lbl_sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if retro_font: lbl_sub.add_theme_font_override("font", retro_font)
	lbl_sub.add_theme_font_size_override("font_size", 32)
	lbl_sub.add_theme_color_override("font_color", Color(0.8, 0.8, 0.8))
	lbl_sub.add_theme_color_override("font_shadow_color", Color.BLACK)
	lbl_sub.add_theme_constant_override("shadow_offset_x", 4)
	lbl_sub.add_theme_constant_override("shadow_offset_y", 4)
	title_box.add_child(lbl_sub)
	
	# Efek melayang KHUSUS untuk teks judul (tidak akan merusak posisi tombol)
	var tw = create_tween().set_loops()
	tw.tween_property(title_box, "position:y", -10.0, 2.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tw.tween_property(title_box, "position:y", 10.0, 2.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	
	# Spacer
	var spacer = Control.new()
	spacer.custom_minimum_size = Vector2(0, 50)
	main_vbox.add_child(spacer)
	
	# HBox untuk membuat baris tombol
	var btn_vbox = VBoxContainer.new()
	btn_vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	btn_vbox.add_theme_constant_override("separation", 15)
	main_vbox.add_child(btn_vbox)
	
	# Tombol Mulai
	var btn_start = Button.new()
	btn_start.text = "MULAI SIMULASI"
	btn_start.custom_minimum_size = Vector2(300, 50) # Diperpendek!
	if retro_font: btn_start.add_theme_font_override("font", retro_font)
	btn_start.add_theme_font_size_override("font_size", 20)
	_style_button(btn_start)
	
	btn_start.pressed.connect(func(): 
		main_vbox.visible = false
		_setup_pregame_overlay()
	)
	btn_vbox.add_child(btn_start)
	
	# Tombol Pengaturan
	var btn_settings = Button.new()
	btn_settings.text = "PENGATURAN"
	btn_settings.custom_minimum_size = Vector2(300, 50)
	if retro_font: btn_settings.add_theme_font_override("font", retro_font)
	btn_settings.add_theme_font_size_override("font_size", 20)
	_style_button(btn_settings)
	btn_vbox.add_child(btn_settings)
	
	# Tombol Kredit
	var btn_credits = Button.new()
	btn_credits.text = "KREDIT"
	btn_credits.custom_minimum_size = Vector2(300, 50)
	if retro_font: btn_credits.add_theme_font_override("font", retro_font)
	btn_credits.add_theme_font_size_override("font_size", 20)
	_style_button(btn_credits)
	btn_vbox.add_child(btn_credits)
	
	# Tombol Keluar
	var btn_exit = Button.new()
	btn_exit.text = "KELUAR"
	btn_exit.custom_minimum_size = Vector2(300, 50)
	if retro_font: btn_exit.add_theme_font_override("font", retro_font)
	btn_exit.add_theme_font_size_override("font_size", 20)
	_style_button(btn_exit)
	
	btn_exit.pressed.connect(func():
		get_tree().quit()
	)
	btn_vbox.add_child(btn_exit)
	
	# Hapus animasi melayang pada seluruh kontainer karena terasa aneh
	
	# ==========================================================================
	# HALAMAN KREDIT
	# ==========================================================================
	var credits_box = VBoxContainer.new()
	credits_box.alignment = BoxContainer.ALIGNMENT_CENTER
	credits_box.add_theme_constant_override("separation", 20)
	credits_box.visible = false
	center.add_child(credits_box)
	
	var lbl_credit_title = Label.new()
	lbl_credit_title.text = "KREDIT"
	lbl_credit_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if retro_font: lbl_credit_title.add_theme_font_override("font", retro_font)
	lbl_credit_title.add_theme_font_size_override("font_size", 40)
	lbl_credit_title.add_theme_color_override("font_color", Color(0.9, 0.8, 0.2))
	credits_box.add_child(lbl_credit_title)
	
	var lbl_credit_text = Label.new()
	lbl_credit_text.text = "Game ini dirancang khusus oleh\n\nDeveloper: Kelompok 10"
	lbl_credit_text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if retro_font: lbl_credit_text.add_theme_font_override("font", retro_font)
	lbl_credit_text.add_theme_font_size_override("font_size", 16)
	lbl_credit_text.add_theme_color_override("font_color", Color.WHITE)
	credits_box.add_child(lbl_credit_text)
	
	var spacer_cr = Control.new()
	spacer_cr.custom_minimum_size = Vector2(0, 30)
	credits_box.add_child(spacer_cr)
	
	var btn_back = Button.new()
	btn_back.text = "KEMBALI"
	btn_back.custom_minimum_size = Vector2(200, 50)
	if retro_font: btn_back.add_theme_font_override("font", retro_font)
	btn_back.add_theme_font_size_override("font_size", 20)
	_style_button(btn_back)
	btn_back.pressed.connect(func():
		credits_box.visible = false
		main_vbox.visible = true
	)
	credits_box.add_child(btn_back)
	
	btn_credits.pressed.connect(func():
		main_vbox.visible = false
		credits_box.visible = true
	)
	
	# ==========================================================================
	# HALAMAN PENGATURAN
	# ==========================================================================
	var settings_box = VBoxContainer.new()
	settings_box.alignment = BoxContainer.ALIGNMENT_CENTER
	settings_box.add_theme_constant_override("separation", 20)
	settings_box.visible = false
	center.add_child(settings_box)
	
	var lbl_set = Label.new()
	lbl_set.text = "PENGATURAN"
	lbl_set.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if retro_font: lbl_set.add_theme_font_override("font", retro_font)
	lbl_set.add_theme_font_size_override("font_size", 40)
	lbl_set.add_theme_color_override("font_color", Color(0.9, 0.8, 0.2))
	settings_box.add_child(lbl_set)
	
	var grid_set = GridContainer.new()
	grid_set.columns = 2
	grid_set.add_theme_constant_override("h_separation", 20)
	grid_set.add_theme_constant_override("v_separation", 15)
	settings_box.add_child(grid_set)
	
	# Volume
	var lbl_vol = Label.new()
	lbl_vol.text = "Volume Master:"
	if retro_font: lbl_vol.add_theme_font_override("font", retro_font)
	grid_set.add_child(lbl_vol)
	
	var sld_vol = HSlider.new()
	sld_vol.custom_minimum_size = Vector2(200, 20)
	sld_vol.max_value = 1.0
	sld_vol.step = 0.05
	sld_vol.value = SettingsManager.volume_master
	sld_vol.value_changed.connect(func(val): SettingsManager.set_volume_master(val))
	grid_set.add_child(sld_vol)
	
	# Fullscreen
	var lbl_fs = Label.new()
	lbl_fs.text = "Layar Penuh:"
	if retro_font: lbl_fs.add_theme_font_override("font", retro_font)
	grid_set.add_child(lbl_fs)
	
	var chk_fs = CheckButton.new()
	chk_fs.button_pressed = SettingsManager.is_fullscreen
	chk_fs.toggled.connect(func(val): SettingsManager.set_fullscreen(val))
	grid_set.add_child(chk_fs)
	
	# VSync
	var lbl_vsync = Label.new()
	lbl_vsync.text = "V-Sync:"
	if retro_font: lbl_vsync.add_theme_font_override("font", retro_font)
	grid_set.add_child(lbl_vsync)
	
	var chk_vsync = CheckButton.new()
	chk_vsync.button_pressed = SettingsManager.is_vsync
	chk_vsync.toggled.connect(func(val): SettingsManager.set_vsync(val))
	grid_set.add_child(chk_vsync)
	
	# HP Bar
	var lbl_hp = Label.new()
	lbl_hp.text = "Tampilkan Darah:"
	if retro_font: lbl_hp.add_theme_font_override("font", retro_font)
	grid_set.add_child(lbl_hp)
	
	var chk_hp = CheckButton.new()
	chk_hp.button_pressed = SettingsManager.show_hp_bar
	chk_hp.toggled.connect(func(val): SettingsManager.set_show_hp_bar(val))
	grid_set.add_child(chk_hp)
	
	# Info Kontrol
	var lbl_controls = Label.new()
	lbl_controls.text = "\n[ INFO KONTROL ]\nESC: Jeda (Pause)\n\n[ GOD MODE ]\nKlik Kiri: Gunakan Kekuatan\n\n[ POSSESS MODE ]\nWASD: Bergerak\nL: Tebasan Pedang\nK: Melesat (Dash)\nKlik Kanan After Posessed: Melepas Kontrol Unit"
	lbl_controls.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if retro_font: lbl_controls.add_theme_font_override("font", retro_font)
	lbl_controls.add_theme_font_size_override("font_size", 14)
	settings_box.add_child(lbl_controls)
	
	var spacer_set = Control.new()
	spacer_set.custom_minimum_size = Vector2(0, 30)
	settings_box.add_child(spacer_set)
	
	var btn_back2 = Button.new()
	btn_back2.text = "KEMBALI"
	btn_back2.custom_minimum_size = Vector2(200, 50)
	if retro_font: btn_back2.add_theme_font_override("font", retro_font)
	btn_back2.add_theme_font_size_override("font_size", 20)
	_style_button(btn_back2)
	btn_back2.pressed.connect(func():
		settings_box.visible = false
		main_vbox.visible = true
	)
	settings_box.add_child(btn_back2)
	
	btn_settings.pressed.connect(func():
		main_vbox.visible = false
		settings_box.visible = true
	)

func _style_button(btn: Button):
	var style = StyleBoxFlat.new()
	style.bg_color = Color(0.15, 0.15, 0.15)
	style.border_width_bottom = 6
	style.border_color = Color.BLACK
	style.corner_radius_top_left = 8
	style.corner_radius_top_right = 8
	style.corner_radius_bottom_left = 8
	style.corner_radius_bottom_right = 8
	
	btn.add_theme_stylebox_override("normal", style)
	btn.add_theme_stylebox_override("hover", style)
	btn.add_theme_color_override("font_color", Color.WHITE)
	
	btn.mouse_entered.connect(func(): btn.modulate = Color(1.3, 1.3, 0.5))
	btn.mouse_exited.connect(func(): btn.modulate = Color.WHITE)

func _process(delta: float):
	# Gerakkan awan di background
	for cloud in cloud_nodes:
		cloud.position.x += 15.0 * delta
		if cloud.position.x > get_viewport_rect().size.x + 200:
			cloud.position.x = -200
			cloud.position.y = randf_range(0, get_viewport_rect().size.y)

# ==============================================================================
# PRE-GAME SETUP (CARTOONISH UI)
# ==============================================================================
func _setup_pregame_overlay():
	var retro_font = preload("res://Asset/Fonts/PressStart2P.ttf")
	
	if pregame_box != null:
		pregame_box.visible = true
		return
		
	pregame_box = Control.new()
	pregame_box.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(pregame_box)
	
	# Background dim
	var dim = ColorRect.new()
	dim.color = Color(0, 0, 0, 0.7)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	pregame_box.add_child(dim)
	
	# Scroll Raksasa
	var scroll_bg = TextureRect.new()
	scroll_bg.texture = preload("res://Asset/Sprites/scroll_wide.png")
	scroll_bg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	scroll_bg.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	scroll_bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	pregame_box.add_child(scroll_bg)
	
	var center = CenterContainer.new()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	pregame_box.add_child(center)
	
	var margin = MarginContainer.new()
	margin.add_theme_constant_override("margin_top", 80) # Dinaikkan lebih banyak agar pas di tengah scroll
	center.add_child(margin)
	
	var vbox = VBoxContainer.new()
	vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	vbox.add_theme_constant_override("separation", 30)
	margin.add_child(vbox)
	
	# Judul
	var lbl_title = Label.new()
	lbl_title.text = "ATUR PASUKAN"
	lbl_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if retro_font: lbl_title.add_theme_font_override("font", retro_font)
	lbl_title.add_theme_font_size_override("font_size", 28) # Dikecilkan
	lbl_title.add_theme_color_override("font_color", Color(1, 0.8, 0.2))
	lbl_title.add_theme_color_override("font_outline_color", Color.BLACK)
	lbl_title.add_theme_constant_override("outline_size", 8)
	lbl_title.add_theme_constant_override("shadow_offset_y", 4)
	lbl_title.add_theme_color_override("font_shadow_color", Color(0,0,0,0.5))
	vbox.add_child(lbl_title)
	
	# HBox untuk 2 Panel Tablet Batu
	var hbox_panels = HBoxContainer.new()
	hbox_panels.alignment = BoxContainer.ALIGNMENT_CENTER
	hbox_panels.add_theme_constant_override("separation", 80) # Jarak antar tim diperlebar
	vbox.add_child(hbox_panels)
	
	# ----- PANEL MERAH -----
	var panel_red = PanelContainer.new()
	panel_red.custom_minimum_size = Vector2(250, 280) # Dikecilkan lagi
	var sb_red = StyleBoxTexture.new()
	sb_red.texture = preload("res://Asset/Sprites/panel_red_handdrawn.png")
	sb_red.modulate_color = Color(1, 1, 1, 0.9) # Sedikit transparan agar menyatu dengan kertas
	panel_red.add_theme_stylebox_override("panel", sb_red)
	hbox_panels.add_child(panel_red)
	
	var vbox_red = VBoxContainer.new()
	vbox_red.alignment = BoxContainer.ALIGNMENT_CENTER
	vbox_red.add_theme_constant_override("separation", 10)
	panel_red.add_child(vbox_red)
	
	var lbl_r_team = Label.new()
	lbl_r_team.text = "TIM MERAH"
	lbl_r_team.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if retro_font: lbl_r_team.add_theme_font_override("font", retro_font)
	lbl_r_team.add_theme_font_size_override("font_size", 16)
	lbl_r_team.add_theme_color_override("font_outline_color", Color.BLACK)
	lbl_r_team.add_theme_constant_override("outline_size", 4)
	vbox_red.add_child(lbl_r_team)
	
	var img_r = TextureRect.new()
	img_r.texture = preload("res://Asset/Sprites/Red_Biasa_Possessed.png")
	img_r.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	img_r.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	img_r.custom_minimum_size = Vector2(160, 160)
	vbox_red.add_child(img_r)
	
	var hbox_r_btn = HBoxContainer.new()
	hbox_r_btn.alignment = BoxContainer.ALIGNMENT_CENTER
	hbox_r_btn.add_theme_constant_override("separation", 15)
	vbox_red.add_child(hbox_r_btn)
	
	var btn_r_min = _create_cartoon_btn("-", retro_font)
	lbl_pop_red = Label.new()
	lbl_pop_red.text = str(pop_red)
	if retro_font: lbl_pop_red.add_theme_font_override("font", retro_font)
	lbl_pop_red.add_theme_font_size_override("font_size", 20)
	lbl_pop_red.add_theme_color_override("font_outline_color", Color.BLACK)
	lbl_pop_red.add_theme_constant_override("outline_size", 4)
	var btn_r_plus = _create_cartoon_btn("+", retro_font)
	
	btn_r_min.pressed.connect(func(): pop_red = max(5, pop_red - 5); lbl_pop_red.text = str(pop_red))
	btn_r_plus.pressed.connect(func(): pop_red = min(100, pop_red + 5); lbl_pop_red.text = str(pop_red))
	
	hbox_r_btn.add_child(btn_r_min)
	hbox_r_btn.add_child(lbl_pop_red)
	hbox_r_btn.add_child(btn_r_plus)
	
	# ----- PANEL BIRU -----
	var panel_blue = PanelContainer.new()
	panel_blue.custom_minimum_size = Vector2(250, 280) # Dikecilkan lagi
	var sb_blue = StyleBoxTexture.new()
	sb_blue.texture = preload("res://Asset/Sprites/panel_blue_handdrawn.png")
	sb_blue.modulate_color = Color(1, 1, 1, 0.9) # Sedikit transparan agar menyatu dengan kertas
	panel_blue.add_theme_stylebox_override("panel", sb_blue)
	hbox_panels.add_child(panel_blue)
	
	var vbox_blue = VBoxContainer.new()
	vbox_blue.alignment = BoxContainer.ALIGNMENT_CENTER
	vbox_blue.add_theme_constant_override("separation", 10)
	panel_blue.add_child(vbox_blue)
	
	var lbl_b_team = Label.new()
	lbl_b_team.text = "TIM BIRU"
	lbl_b_team.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	if retro_font: lbl_b_team.add_theme_font_override("font", retro_font)
	lbl_b_team.add_theme_font_size_override("font_size", 16)
	lbl_b_team.add_theme_color_override("font_outline_color", Color.BLACK)
	lbl_b_team.add_theme_constant_override("outline_size", 4)
	vbox_blue.add_child(lbl_b_team)
	
	var img_b = TextureRect.new()
	img_b.texture = preload("res://Asset/Sprites/Blue_Biasa_Possessed.png")
	img_b.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	img_b.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	img_b.custom_minimum_size = Vector2(160, 160)
	vbox_blue.add_child(img_b)
	
	var hbox_b_btn = HBoxContainer.new()
	hbox_b_btn.alignment = BoxContainer.ALIGNMENT_CENTER
	hbox_b_btn.add_theme_constant_override("separation", 15)
	vbox_blue.add_child(hbox_b_btn)
	
	var btn_b_min = _create_cartoon_btn("-", retro_font)
	lbl_pop_blue = Label.new()
	lbl_pop_blue.text = str(pop_blue)
	if retro_font: lbl_pop_blue.add_theme_font_override("font", retro_font)
	lbl_pop_blue.add_theme_font_size_override("font_size", 20)
	lbl_pop_blue.add_theme_color_override("font_outline_color", Color.BLACK)
	lbl_pop_blue.add_theme_constant_override("outline_size", 4)
	var btn_b_plus = _create_cartoon_btn("+", retro_font)
	
	btn_b_min.pressed.connect(func(): pop_blue = max(5, pop_blue - 5); lbl_pop_blue.text = str(pop_blue))
	btn_b_plus.pressed.connect(func(): pop_blue = min(100, pop_blue + 5); lbl_pop_blue.text = str(pop_blue))
	
	hbox_b_btn.add_child(btn_b_min)
	hbox_b_btn.add_child(lbl_pop_blue)
	hbox_b_btn.add_child(btn_b_plus)
	
	# --- STYLING TOMBOL BAWAH ---
	var sb_play = StyleBoxFlat.new()
	sb_play.bg_color = Color(1.0, 0.7, 0.1) # Emas
	sb_play.border_width_left = 4; sb_play.border_width_right = 4
	sb_play.border_width_top = 4; sb_play.border_width_bottom = 4
	sb_play.border_color = Color.BLACK
	sb_play.corner_radius_top_left = 8; sb_play.corner_radius_top_right = 8
	sb_play.corner_radius_bottom_left = 8; sb_play.corner_radius_bottom_right = 8
	sb_play.shadow_color = Color(0,0,0,0.5)
	sb_play.shadow_size = 0; sb_play.shadow_offset = Vector2(4, 4)
	
	var sb_play_h = sb_play.duplicate()
	sb_play_h.bg_color = Color(1.0, 0.9, 0.3)
	
	var sb_back = sb_play.duplicate()
	sb_back.bg_color = Color(0.9, 0.9, 0.9) # Putih keabu-abuan
	
	# HBox untuk menyusun bersebelahan
	var hbox_bottom = HBoxContainer.new()
	hbox_bottom.alignment = BoxContainer.ALIGNMENT_CENTER
	hbox_bottom.add_theme_constant_override("separation", 50)
	vbox.add_child(hbox_bottom)
	
	# Tombol Kembali (Di Kiri)
	var btn_back = Button.new()
	btn_back.text = "KEMBALI"
	btn_back.custom_minimum_size = Vector2(240, 35)
	if retro_font: btn_back.add_theme_font_override("font", retro_font)
	btn_back.add_theme_font_size_override("font_size", 10)
	btn_back.add_theme_stylebox_override("normal", sb_back)
	btn_back.add_theme_stylebox_override("hover", sb_play_h)
	btn_back.add_theme_color_override("font_color", Color.BLACK)
	btn_back.add_theme_color_override("font_hover_color", Color.BLACK)
	btn_back.pressed.connect(func():
		pregame_box.visible = false
		main_vbox.visible = true
	)
	hbox_bottom.add_child(btn_back)
	
	# TOMBOL START JOURNEY (Di Kanan)
	var btn_play = Button.new()
	btn_play.text = "MULAI PERANG!"
	btn_play.custom_minimum_size = Vector2(240, 40)
	if retro_font: btn_play.add_theme_font_override("font", retro_font)
	btn_play.add_theme_font_size_override("font_size", 14)
	btn_play.add_theme_stylebox_override("normal", sb_play)
	btn_play.add_theme_stylebox_override("hover", sb_play_h)
	btn_play.add_theme_color_override("font_color", Color.BLACK)
	btn_play.add_theme_color_override("font_hover_color", Color.BLACK)
	btn_play.pressed.connect(func():
		Config.set("INIT_POP_RED", pop_red)
		Config.set("INIT_POP_BLUE", pop_blue)
		get_tree().change_scene_to_file("res://Scenes/main.tscn")
	)
	hbox_bottom.add_child(btn_play)

func _create_cartoon_btn(txt: String, custom_font: Font = null) -> Button:
	var b = Button.new()
	b.text = txt
	b.custom_minimum_size = Vector2(40, 40)
	if custom_font: b.add_theme_font_override("font", custom_font)
	b.add_theme_font_size_override("font_size", 20)
	
	var sb = StyleBoxFlat.new()
	sb.bg_color = Color.WHITE
	sb.border_width_left = 4; sb.border_width_right = 4
	sb.border_width_top = 4; sb.border_width_bottom = 4
	sb.border_color = Color.BLACK
	sb.corner_radius_top_left = 25; sb.corner_radius_top_right = 25
	sb.corner_radius_bottom_left = 25; sb.corner_radius_bottom_right = 25
	sb.shadow_color = Color(0,0,0,0.5)
	sb.shadow_size = 0; sb.shadow_offset = Vector2(4, 4)
	
	b.add_theme_stylebox_override("normal", sb)
	var sb_h = sb.duplicate()
	sb_h.bg_color = Color(1.0, 1.0, 1.0)
	b.add_theme_stylebox_override("hover", sb_h)
	b.add_theme_color_override("font_color", Color.BLACK)
	
	return b
