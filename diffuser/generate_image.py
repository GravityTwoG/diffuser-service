from diffusers import DiffusionPipeline
import torch
import platform
from pathlib import Path

pipeline = DiffusionPipeline \
  .from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32,
    use_safetensors=True, 
  )

if platform.system() == "Windows":
  print("Using GPU")
  # pipeline = pipeline.to("cuda")
  pipeline.enable_xformers_memory_efficient_attention()
  pipeline.enable_sequential_cpu_offload()
else:
  print("Using Apple Silicon MPS")
  pipeline = pipeline.to("mps")


# Recommended if your computer has < 64 GB of RAM
pipeline.enable_attention_slicing()

images_dir = Path('./images')

def generate_image(prompt, image_name, num_images=1):
  prompts = [prompt] * num_images
  images = pipeline(
    prompts, 
    num_inference_steps=25, 
    guidance_scale=7.5,
    safety_checker=None,
  ).images

  for i, image in enumerate(images):
    image_path = images_dir / f"{image_name}.[{i}].png"
    image.save(image_path)


if __name__ == '__main__':
  generate_image(
    "A black and white image",
    "1234",
    1
  )
