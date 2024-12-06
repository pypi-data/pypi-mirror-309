import os
from availai.datasets.dataset import Dataset

dataset_path = os.path.sep.join(
    [os.getcwd(), "tests", "datasets", "football-players-detection"]
)
api_key_path = os.path.sep.join(
    [os.getcwd(), "tests", "datasets", "roboflow_api_key.txt"]
)
print("Dataset path: ", dataset_path)
print("API key path: ", api_key_path)

dataset = Dataset(
    path=dataset_path, name="football-player", project_name="football-players-detection"
)

dataset.download_from_roboflow(
    model_format="yolov8",
    api_key=api_key_path,
    workspace="roboflow-jvuqo",
    project_name="football-players-detection-3zvbc",
)

# Copy dataset
dataset.copy_to(os.path.sep.join([dataset_path + "-copy"]))
