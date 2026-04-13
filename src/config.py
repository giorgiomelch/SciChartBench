"""
Configurazione centralizzata dei path per il benchmark sota_chart_to_table.

Funzionamento:
- In locale: tutti i path sono relativi alla root del progetto.
- Su Google Colab: il progetto è clonato in /content/sota_chart_to_table.
  I pesi e gli output (predictions, metrics, reports) vengono salvati su
  Google Drive impostando la variabile d'ambiente DRIVE_BASE_DIR prima di
  eseguire qualsiasi script, oppure passando --drive-path a run_benchmark.py.

Esempio Colab:
    import os
    os.environ["DRIVE_BASE_DIR"] = "/content/drive/MyDrive/MioProgetto"
    # oppure: python run_benchmark.py --drive-path /content/drive/MyDrive/MioProgetto
"""

import os
from pathlib import Path

# --- Rilevamento ambiente ---

_is_colab = Path("/content").exists() and Path("/content/sota_chart_to_table").exists()

if _is_colab:
    PROJECT_ROOT = Path("/content/sota_chart_to_table")
else:
    # Due livelli sopra src/config.py
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

# --- Drive base (opzionale) ---

_drive_env = os.environ.get("DRIVE_BASE_DIR")
DRIVE_BASE_DIR: Path | None = Path(_drive_env) if _drive_env else None

# --- Path di input (sempre locali al progetto) ---

IMAGES_DIR = PROJECT_ROOT / "data" / "images"
GROUNDTRUTH_DIR = PROJECT_ROOT / "data" / "groundtruth"

# --- Path di output e pesi (su Drive se disponibile, altrimenti locali) ---

_out_base: Path = DRIVE_BASE_DIR if DRIVE_BASE_DIR is not None else PROJECT_ROOT

WEIGHTS_DIR = _out_base / "weights"
PREDICTIONS_DIR = _out_base / "outputs" / "predictions"
METRICS_DIR = _out_base / "outputs" / "metrics"
REPORTS_DIR = _out_base / "outputs" / "reports"
