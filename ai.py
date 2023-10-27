import cv2
from PIL import Image
from roboflow import Roboflow


class Ai:
    def __init__(self):
        rf = Roboflow(api_key="kDPogOFw5AbqDr95ytoZ")
        project = rf.workspace().project("license-plates-kwudy")
        self.model = project.version(5).model

    def run(self, file_path):
        image = Image.open(file_path)
        result = self.model.predict(file_path, confidence=60, overlap=30).json()

        for i in range(len(result['predictions'])):
            x1 = result['predictions'][i]['x'] - result['predictions'][i]['width'] // 2
            y1 = result['predictions'][i]['y'] - result['predictions'][i]['height'] // 2
            x2 = x1 + result['predictions'][i]['width']
            y2 = y1 + result['predictions'][i]['height']

            cropped_image = image.crop((x1, y1, x2, y2))
            cropped_image.show()
