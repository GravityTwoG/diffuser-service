from diffusers import DiffusionPipeline
import torch
import platform

pipeline = DiffusionPipeline \
  .from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float32,
    use_safetensors=True, 
  ) \

if platform.system() == "Windows":
  print("Using GPU")
  # pipeline = pipeline.to("cuda")
  pipeline.enable_xformers_memory_efficient_attention()
else:
  print("Using Apple Silicon MPS")
  pipeline = pipeline.to("mps")

pipeline.enable_sequential_cpu_offload()

# Recommended if your computer has < 64 GB of RAM
pipeline.enable_attention_slicing()

def produce_image(prompt, image_name, num_images=1):
  prompts = [prompt] * num_images
  images = pipeline(prompts).images

  for i, image in enumerate(images):
    image.save(f"./output/{image_name}.[{i}].png")

produce_image(
  "An image of a squirrel robot",
  "an_image_of_a_squirrel",
  1
)
# produce_image(
#   "An image of a squirrel in Picasso style", 
#   "image_of_squirrel_painting",
#   1
# )
