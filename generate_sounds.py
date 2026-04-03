import base64
import wave
import struct
import math
import json

def generate_wav_data_uri(freq, duration_ms, wave_type='sine'):
    sample_rate = 44100
    num_samples = int(sample_rate * (duration_ms / 1000.0))
    
    # Generate PCM data
    audio_data = []
    for i in range(num_samples):
        t = float(i) / sample_rate
        # Apply an exponential envelope to make it sound like a quick "tick" or "click"
        envelope = math.exp(-t * (1000.0 / duration_ms * 5.0))
        
        if wave_type == 'sine':
            val = math.sin(2.0 * math.pi * freq * t)
        elif wave_type == 'square':
            val = 1.0 if math.sin(2.0 * math.pi * freq * t) > 0 else -1.0
        elif wave_type == 'saw':
            val = 2.0 * (freq * t - math.floor(freq * t + 0.5))
        elif wave_type == 'noise':
            import random
            val = random.uniform(-1, 1)
        
        val = val * envelope * 0.5 # 50% volume
        
        # Convert to 16-bit PCM integer
        packed_val = int(val * 32767.0)
        audio_data.append(packed_val)
        
    # Create WAV in memory
    import io
    wav_io = io.BytesIO()
    with wave.open(wav_io, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        frame_data = b''.join(struct.pack('<h', sample) for sample in audio_data)
        wav_file.writeframes(frame_data)
        
    wav_bytes = wav_io.getvalue()
    b64_str = base64.b64encode(wav_bytes).decode('utf-8')
    return f"data:audio/wav;base64,{b64_str}"

sounds = []
# Generate 20 variants
configs = [
    ("Sci-Fi Click", 800, 30, 'square'),
    ("Deep Pop", 200, 40, 'sine'),
    ("Tiny Tick", 2000, 20, 'sine'),
    ("Space Beep", 1200, 50, 'sine'),
    ("Low Thump", 100, 60, 'square'),
    ("High Chime", 1800, 40, 'saw'),
    ("Static Tap", 500, 30, 'noise'),
    ("Digital Coin", 1500, 80, 'sine'),
    ("Subtle Dot", 600, 25, 'sine'),
    ("Hollow Tap", 300, 50, 'saw'),
    ("Harsh Click", 1000, 20, 'square'),
    ("Muted Blip", 400, 35, 'sine'),
    ("Laser Drop", 2500, 40, 'sine'),
    ("Warm Pluck", 700, 60, 'sine'),
    ("Retro Jump", 900, 70, 'square'),
    ("Glass Ping", 3000, 40, 'sine'),
    ("Soft Thud", 150, 40, 'square'),
    ("Mechanical Switch", 500, 30, 'square'),
    ("Clean Pop", 1100, 40, 'sine'),
    ("Tiny Zap", 2200, 30, 'saw')
]

for name, freq, dur, wtype in configs:
    uri = generate_wav_data_uri(freq, dur, wtype)
    sounds.append({"name": name, "url": uri})

with open('generated_sounds.json', 'w') as f:
    json.dump(sounds, f)

print("Generated.")
