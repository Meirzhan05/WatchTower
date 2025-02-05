import os
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")

# Train the model
train_results = model.train(
    data="coco8.yaml",  # path to dataset YAML
    epochs=2,  # number of training epochs
    imgsz=640,  # training image size
    device="cpu",  # device to run on, i.e. device=0 or device=0,1,2,3 or device=cpu
)

# model.track(source=0, show=True,)

# Evaluate model performance on the validation set
metrics = model.val()

image_path = os.path.join(os.path.dirname(__file__), "yacht.jpg")


# Perform object detection on an image
results = model(image_path)
results[0].show()

# Export the model to ONNX format
path = model.export(format="onnx")  # return path to exported model