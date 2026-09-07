extends Label
class_name FloatingText

var velocity: Vector2
var lifetime: float = 1.0
var timer: float = 0.0

func _ready():
	# Menggunakan font retro dan styling dasar
	var retro_font = preload("res://Asset/Fonts/PressStart2P.ttf")
	add_theme_font_override("font", retro_font)
	add_theme_font_size_override("font_size", 8)
	add_theme_color_override("font_outline_color", Color.BLACK)
	add_theme_constant_override("outline_size", 4)
	
	velocity = Vector2(randf_range(-15, 15), -40) # Melayang ke atas
	
func _process(delta):
	global_position += velocity * delta
	timer += delta
	
	# Fade out (menghilang perlahan)
	modulate.a = 1.0 - (timer / lifetime)
	
	if timer >= lifetime:
		queue_free()
