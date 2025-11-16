from diffusers import StableDiffusionPipeline
import torch

# load model (this downloads automatically from Hugging Face)
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")  # if you have a GPU, otherwise use "cpu"
# pipe=pipe.to("cpu")

prompt = "a cute robot learning to code"
image = pipe(prompt).images[0]

image.save("output.png")
print("Image saved as output.png")
