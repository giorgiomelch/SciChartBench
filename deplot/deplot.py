from transformers import AutoProcessor, Pix2StructForConditionalGeneration
from PIL import Image
from pathlib import Path
import torch

def load_model_and_processor():
    model_name = "google/deplot"
    model = Pix2StructForConditionalGeneration.from_pretrained(model_name)
    processor = AutoProcessor.from_pretrained(model_name)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()
    print(f"Device in uso: {device}")
    return model, processor, device

def process_images(paths, destination_dir, model, processor, device):
    dest_path = Path(destination_dir)
    dest_path.mkdir(parents=True, exist_ok=True)

    for p in paths:
        img_path = Path(p)
        
        if not img_path.exists():
            print(f"Salto: {img_path} (File non trovato)")
            continue

        try:
            image = Image.open(img_path).convert("RGB")
            
            inputs = processor(images=image, text="Generate underlying data table of the figure below:", return_tensors="pt").to(device)
            with torch.no_grad():
                predictions = model.generate(**inputs, max_new_tokens=512)
            result = processor.decode(predictions[0], skip_special_tokens=True).replace("<0x0A>", "\n")
            
            output_file = dest_path / f"{img_path.stem}.txt"
            output_file.write_text(result, encoding="utf-8")
            print(f"Processato con successo: {img_path.name} -> {output_file.name}")
            
        except Exception as e:
            print(f"Errore durante l'elaborazione di {img_path.name}: {e}")