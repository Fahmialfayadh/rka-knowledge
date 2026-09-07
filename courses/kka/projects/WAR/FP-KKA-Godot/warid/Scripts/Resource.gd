extends Area2D
class_name GameResource

@export var rtype: String = "wood" # Pilihan: wood, iron, food
var depleted: bool = false
var respawn_timer: float = 0.0

func _ready() -> void:
	add_to_group("resources")
	
	var sprite = $Sprite2D
	if rtype == "wood":
		sprite.texture = preload("res://Asset/Sprites/tree.png")
	elif rtype == "iron":
		sprite.texture = preload("res://Asset/Sprites/iron_ baru.png")
	elif rtype == "food":
		sprite.texture = preload("res://Asset/Sprites/Daging.png")
		sprite.scale = Vector2(3.0, 3.0) # Bikin dagingnya JUMBO!
		
	# Efek Bounce
	var t_scale = scale
	scale = Vector2.ZERO
	var tw = create_tween()
	tw.tween_property(self, "scale", t_scale, 0.5).set_trans(Tween.TRANS_ELASTIC).set_ease(Tween.EASE_OUT)

func deplete():
	depleted = true
	visible = false
	respawn_timer = randf_range(Config.RESPAWN_TIME_MIN, Config.RESPAWN_TIME_MAX)

func _process(delta: float) -> void:
	if depleted:
		respawn_timer -= delta
		if respawn_timer <= 0:
			var world = get_tree().current_scene
			if world.has_method("_get_valid_resource_pos"):
				global_position = world._get_valid_resource_pos()
			depleted = false
			visible = true
			
			var cur_scale = scale
			scale = Vector2.ZERO
			var tw = create_tween()
			tw.tween_property(self, "scale", cur_scale, 0.5).set_trans(Tween.TRANS_ELASTIC).set_ease(Tween.EASE_OUT)

func respawn(new_pos: Vector2):
	depleted = false
	visible = true
	global_position = new_pos
