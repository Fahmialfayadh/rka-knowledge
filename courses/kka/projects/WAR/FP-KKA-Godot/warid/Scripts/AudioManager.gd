extends Node

var hit_snd = preload("res://Asset/Audio/hit.wav")
var chop_snd = preload("res://Asset/Audio/chop.wav")
var die_snd = preload("res://Asset/Audio/die.wav")
var spawn_snd = preload("res://Asset/Audio/spawn.wav")

var audio_pool = []
const POOL_SIZE = 15

func _ready():
	# Siapkan pool player agar tidak kepotong saat banyak suara bersamaan
	for i in range(POOL_SIZE):
		var p = AudioStreamPlayer.new()
		add_child(p)
		audio_pool.append(p)
		
	# Setup BGM Player
	var bgm_stream = preload("res://Asset/Audio/bgm_theme.ogg")
	if bgm_stream is AudioStreamOggVorbis:
		bgm_stream.loop = true
	var bgm_player = AudioStreamPlayer.new()
	bgm_player.stream = bgm_stream
	bgm_player.volume_db = -10.0 # BGM jangan terlalu keras
	add_child(bgm_player)
	bgm_player.play()

func play_sfx(sfx_name: String):
	var snd = null
	if sfx_name == "hit": snd = hit_snd
	elif sfx_name == "chop": snd = chop_snd
	elif sfx_name == "die": snd = die_snd
	elif sfx_name == "spawn": snd = spawn_snd
	
	if snd:
		for p in audio_pool:
			if not p.playing:
				p.stream = snd
				p.volume_db = randf_range(-10.0, -5.0)
				p.pitch_scale = randf_range(0.8, 1.2) # Pitch acak biar gak monoton
				p.play()
				return
