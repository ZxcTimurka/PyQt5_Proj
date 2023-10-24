import cv2
import easyocr
import imutils
import numpy as np
from matplotlib import pyplot as pl

img = cv2.imread("n2.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_filter = cv2.bilateralFilter(gray, 11, 17, 17)
edges = cv2.Canny(img_filter, 30, 200)

contours = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

position = None
for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4:
        position = approx
        break

mask = np.zeros(gray.shape[:2], np.uint8)
new_image = cv2.drawContours(mask, [position], 0, 255, -1)
bit_img = cv2.bitwise_and(img, img, mask=mask)
x, y = np.where(mask == 255)
x1, y1 = np.min(x), np.min(y)
x2, y2 = np.max(x), np.max(y)
cropped_image = img[x1:x2, y1:y2]

reader = easyocr.Reader(['ru'])
result = reader.readtext(cropped_image, detail=0)
print(result)

cv2.imwrite('123.jpg', cropped_image)
cv2.imshow("Result", cropped_image)
pl.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
pl.show()
