# from pyaudio import paInt16

# Signal processing
SAMPLE_RATE = 16000
PREEMPHASIS_ALPHA = 0.97
FRAME_LEN = 0.025
FRAME_STEP = 0.01
NUM_FFT = 512
BUCKET_STEP = 1
MAX_SEC = 10

# Model
WEIGHTS_FILE = "src/core/speaker_identification/models/weights.h5"
COST_METRIC = "cosine"  # euclidean or cosine
INPUT_SHAPE=(NUM_FFT,None,1)
