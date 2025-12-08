import streamlit as st
from PIL import Image
import torch
from transformers import ViTForImageClassification, ViTImageProcessor

st.title("Offline Image Recognition")

@st.cache_resource
def load_model():
    processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")
    model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")
    return processor, model

processor, model = load_model()

image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if image_file:
    img = Image.open(image_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    inputs = processor(images=img, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    pred_id = logits.argmax(-1).item()
    label = model.config.id2label[pred_id]

    st.success(f"Prediction: {label}")
