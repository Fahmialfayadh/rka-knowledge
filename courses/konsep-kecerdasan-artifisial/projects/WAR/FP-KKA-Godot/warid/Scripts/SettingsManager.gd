extends Node

const SAVE_PATH = "user://settings.cfg"
var config = ConfigFile.new()

# Settings Variables
var volume_master: float = 1.0 # 0.0 to 1.0
var is_fullscreen: bool = false
var is_vsync: bool = true
var show_hp_bar: bool = true

func _ready():
	_load_settings()
	_apply_all_settings()

func _load_settings():
	if config.load(SAVE_PATH) == OK:
		volume_master = config.get_value("Audio", "volume_master", 1.0)
		is_fullscreen = config.get_value("Display", "fullscreen", false)
		is_vsync = config.get_value("Display", "vsync", true)
		show_hp_bar = config.get_value("Gameplay", "show_hp_bar", true)
	else:
		_save_settings() # Create default file

func _save_settings():
	config.set_value("Audio", "volume_master", volume_master)
	config.set_value("Display", "fullscreen", is_fullscreen)
	config.set_value("Display", "vsync", is_vsync)
	config.set_value("Gameplay", "show_hp_bar", show_hp_bar)
	config.save(SAVE_PATH)

func set_volume_master(value: float):
	volume_master = clamp(value, 0.0, 1.0)
	_apply_audio()
	_save_settings()

func set_fullscreen(value: bool):
	is_fullscreen = value
	_apply_display()
	_save_settings()

func set_vsync(value: bool):
	is_vsync = value
	_apply_display()
	_save_settings()
	
func set_show_hp_bar(value: bool):
	show_hp_bar = value
	_save_settings()

func _apply_all_settings():
	_apply_audio()
	_apply_display()

func _apply_audio():
	# Konversi linear (0-1) ke desibel (-80 ke 0)
	var db = linear_to_db(volume_master)
	if volume_master <= 0.01:
		db = -80.0
	var bus_index = AudioServer.get_bus_index("Master")
	AudioServer.set_bus_volume_db(bus_index, db)
	AudioServer.set_bus_mute(bus_index, volume_master <= 0.01)

func _apply_display():
	if is_fullscreen:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_FULLSCREEN)
	else:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		
	if is_vsync:
		DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED)
	else:
		DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
