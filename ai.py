class LicensePlateDetector:
    def __init__(self):
        from roboflow import Roboflow
        rf = Roboflow(api_key="kDPogOFw5AbqDr95ytoZ")
        project = rf.workspace().project("license-plates-kwudy")
        self.model = project.version(5).model

    def run(self, file_path):
        self.file_path = file_path
        result = self.model.predict(self.file_path, confidence=60, overlap=30).json()
        self.coords = []
        for prediction in result['predictions']:
            x1 = prediction['x'] - prediction['width'] // 2
            y1 = prediction['y'] - prediction['height'] // 2
            x2 = x1 + prediction['width']
            y2 = y1 + prediction['height']
            self.coords.append([round(x1), round(y1), round(x2), round(y2)])
        return len(self.coords)

    def show(self):
        from PIL import Image
        image = Image.open(self.file_path)
        for i in self.coords:
            cropped_image = image.crop(i)
            cropped_image.show()

    def reader(self):
        import easyocr
        import cv2
        import re
        from db import CarNumber

        img = cv2.imread(self.file_path)
        reader = easyocr.Reader(['ru'])
        texts = []
        n = CarNumber()
        for i in self.coords:
            cropped_image = img[i[1]:i[3], i[0]:i[2]]
            gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
            text = reader.readtext(cropped_image, detail=0)
            text = (max(text, key=len))
            text = re.sub(r"\d+$", "", text)
            n.main(text)
            texts.append(text)
        n.get_car_numbers()
        return texts