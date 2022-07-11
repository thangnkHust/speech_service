from pyannote.audio import Audio 
# format wav file to mono channel + sample_rate 16000
audio_load = Audio(sample_rate=16000, mono=True)