class LicensePlateDetector:
    def __init__(self, file_path):
        from roboflow import Roboflow
        rf = Roboflow(api_key="kDPogOFw5AbqDr95ytoZ")
        project = rf.workspace().project("license-plates-kwudy")
        self.model = project.version(5).model
        self.file_path = file_path

    def run(self):
        result = self.model.predict(self.file_path, confidence=60, overlap=30).json()
        self.coords = []
        for prediction in result['predictions']:
            x1 = prediction['x'] - prediction['width'] // 2
            y1 = prediction['y'] - prediction['height'] // 2
            x2 = x1 + prediction['width']
            y2 = y1 + prediction['height']
            self.coords.append([x1, y1, x2, y2])
        print(f'{len(self.coords)} detected')

    def show(self):
        from PIL import Image
        image = Image.open(self.file_path)
        for i in self.coords:
            cropped_image = image.crop(i)
            cropped_image.show()