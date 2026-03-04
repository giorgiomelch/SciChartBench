import os
import json
from PIL import Image
from pathlib import Path
from google import genai
from google.genai import types
import prompts

   
DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_API_KEY_ENV_VAR = "GEMINI_API_KEY"

PROMPT2CHARTCLASS = {
    "area": prompts.PROMPT_AreaLineBarHistogramScatter,
    "line": prompts.PROMPT_AreaLineBarHistogramScatter,
    "bar": prompts.PROMPT_AreaLineBarHistogramScatter,
    "histogram": prompts.PROMPT_AreaLineBarHistogramScatter,      
    "scatter": prompts.PROMPT_AreaLineBarHistogramScatter,
    "radar": prompts.PROMPT_Radar,
    "pie": prompts.PROMPT_Pie,
    "venn": prompts.PROMPT_Venn,
    "box": prompts.PROMPT_Box,
    "errorpoint": prompts.PROMPT_Errorpoint,
    "violin": prompts.PROMPT_Violin,
    "bubble": prompts.PROMPT_Bubble                 
}


def setup_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API Key non trovata. Imposta la variabile d'ambiente GEMINI_API_KEY.")
    return genai.Client(api_key=api_key)

def processa_singolo_grafico(client, percorso_immagine, prompt_testo, file_output):
    try:
        with Image.open(percorso_immagine) as immagine:
            config = types.GenerateContentConfig(
                response_mime_type="application/json"
            )
            response = client.models.generate_content(
                model=DEFAULT_MODEL,
                contents=[prompt_testo, immagine],
                config=config
            )

        dati_json = json.loads(response.text)
        file_output.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_output, 'w', encoding='utf-8') as f:
            json.dump(dati_json, f, ensure_ascii=False, indent=4)
            
        print(f"Completato: {percorso_immagine.name} -> {file_output.name}")
    
    except json.JSONDecodeError:
        print(f"Errore JSON su {percorso_immagine.name}. Output grezzo:\n{response.text}")
    except Exception as e:
        print(f"Errore API/Sistema su {percorso_immagine.name}: {e}")

def pred_pmc():
    client = setup_gemini()
    path_to_pmc_data = Path("data/pmc")
    output_path = Path("predictions/Gemini/pmc")

    if not path_to_pmc_data.exists():
        print(f"Errore: Percorso {path_to_pmc_data} non trovato.")
        return

    for chart_class in path_to_pmc_data.iterdir():
        if not chart_class.is_dir() or chart_class.name not in PROMPT2CHARTCLASS:
            continue
            
        prompt = PROMPT2CHARTCLASS[chart_class.name]
        
        for difficulty in chart_class.iterdir():
            if not difficulty.is_dir():
                continue
            
            immagini = list(difficulty.iterdir())
            print(f"\n--- Elaborazione: {chart_class.name}/{difficulty.name} ({len(immagini)} file) ---")
            
            for image_path in immagini:
                if not image_path.is_file() or image_path.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
                    continue
                
                file_output = output_path / chart_class.name / difficulty.name / f"{image_path.stem}.json"
                if file_output.exists():
                    print(f"Skip: {image_path.name} (Già processato)")
                    continue
                    
                processa_singolo_grafico(client, image_path, prompt, file_output)

def pred_synthetic():
    client = setup_gemini()
    path_to_synthetic_data = Path("data/synthetic")
    output_path = Path("predictions/Gemini/synthetic")

    if not path_to_synthetic_data.exists():
        print(f"Errore: Percorso {path_to_synthetic_data} non trovato.")
        return

    for chart_class in path_to_synthetic_data.iterdir():

        if not chart_class.is_dir() or chart_class.name not in PROMPT2CHARTCLASS:
            continue
        immagini = list(chart_class.iterdir())
        print(f"\n--- Elaborazione: {chart_class.name} ({len(immagini)} file) ---")
            
        prompt = PROMPT2CHARTCLASS[chart_class.name]
        
        for image_path in chart_class.iterdir():
            immagini = list(chart_class.iterdir())
    
            if not image_path.is_file() or image_path.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
                continue
            
            file_output = output_path / chart_class.name / f"{image_path.stem}.json"
            if file_output.exists():
                print(f"Skip: {image_path.name} (Già processato)")
                continue
                    
            processa_singolo_grafico(client, image_path, prompt, file_output)

if __name__ == "__main__":
    #pred_pmc()
    pred_synthetic()
        