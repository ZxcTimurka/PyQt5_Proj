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
            self.coords.append([round(x1), round(y1), round(x2), round(y2)])
        print(f'{len(self.coords)} detected')

    def show(self):
        from PIL import Image
        image = Image.open(self.file_path)
        for i in self.coords:
            cropped_image = image.crop(i)
            cropped_image.show()

    def reader(self):
        import easyocr
        import cv2
        img = cv2.imread(self.file_path)
        reader = easyocr.Reader(['ru'])
        for i in self.coords:
            cropped_image = img[i[1]:i[3], i[0]:i[2]]
            cv2.imshow('123', cropped_image)
            gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
            cv2.imshow('123', gray)
            print(reader.readtext(gray, detail=0))
            cv2.waitKey(0)


ai = LicensePlateDetector('imgs/n2.jpg')
ai.run()
ai.reader()