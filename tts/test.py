from diffusers import DiffusionPipeline
import torch

pipeline = DiffusionPipeline \
  .from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    use_safetensors=True, 
  ) \
  .to("mps")

# Recommended if your computer has < 64 GB of RAM
pipeline.enable_attention_slicing()

prompts = ["An image of a squirrel in Picasso style"]
image = pipeline(prompts).images[0]

image.save("image_of_squirrel_painting.png")