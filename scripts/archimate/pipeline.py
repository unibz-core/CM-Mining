import os, json
import archimate.transform
from pathlib import Path

MODELS_DIR = './archimate/models/'
INPUT_DIR = './input/'

def import_models(directory: Path) -> list[dict]:
    models = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            file_path = os.path.join(MODELS_DIR, file)
            with open(file_path, encoding='utf-8') as f:
                models.append(json.load(f))
    return models

def start():
    # model import
    print(f"Importing models from directory '{MODELS_DIR}'...")
    models = import_models(MODELS_DIR)
    print(f"{len(models)} models imported.")

    # create and store graph
    graphs = archimate.transform.create_graph(models, INPUT_DIR)

    # TODO: filters
