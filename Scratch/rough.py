#import torch
#torch.add(1, 2)

import torch

# Create tensors from the numbers
x = torch.tensor([1])
y = torch.tensor([2])

# Add them together
result = torch.add(x, y)

print(result) # Output: tensor([3])