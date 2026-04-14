import os
import random

DATASET_PATH = "dataset"

def get_all_classes():
    return sorted([
        folder for folder in os.listdir(DATASET_PATH)
        if os.path.isdir(os.path.join(DATASET_PATH, folder))
    ])

def get_sample_video(class_name):
    class_path = os.path.join(DATASET_PATH, class_name)

    try:
        videos = [
            f for f in os.listdir(class_path)
            if f.lower().endswith((".mp4", ".avi", ".mov"))
        ]
    except Exception as e:
        print(f"Error reading {class_name}: {e}")
        return None

    if not videos:
        return None

    return os.path.join(class_path, random.choice(videos))