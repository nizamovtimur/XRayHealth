import io
import torchvision.transforms as transforms
from PIL import Image

classes = ("NORMAL", "PNEUMONIA")


def transform_image(image_bytes):
    transform = transforms.Compose(
        [transforms.Resize((512, 512)),
         transforms.Grayscale(),
         transforms.ToTensor(),
         transforms.Normalize(0.5, 0.5)])
    image = Image.open(io.BytesIO(image_bytes))
    return transform(image).unsqueeze(0)


def get_prediction(image_bytes, model):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    return classes[y_hat.item()]
