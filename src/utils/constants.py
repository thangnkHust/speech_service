# record status
PENDING = 1
STARTED = 2
SUCCESS = 3
FAILURE = 4

# split long audio (second)
TIME_PER_SPLIT = 10

# Load device server
import torch
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu").type