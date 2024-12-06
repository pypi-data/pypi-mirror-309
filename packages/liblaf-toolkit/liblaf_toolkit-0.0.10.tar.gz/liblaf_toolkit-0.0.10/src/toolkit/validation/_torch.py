import pydantic
import torch

Torch = pydantic.BeforeValidator(torch.as_tensor)
