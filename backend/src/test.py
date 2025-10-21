import torch

# Check if CUDA is available
print("CUDA available:", torch.cuda.is_available())

# Number of GPUs
print("Number of GPUs:", torch.cuda.device_count())

# Name of GPU
if torch.cuda.is_available():
    print("GPU Name:", torch.cuda.get_device_name(0))
