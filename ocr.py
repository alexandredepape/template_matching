import cv2
import numpy as np
import imutils

image = cv2.imread('img.png')
image_height, image_width = image.shape[:2]
template = cv2.imread('katarina.png')
(tH, tW) = template.shape[:2]

rescale_factor = 0.0314814814814815 * tW
resized = imutils.resize(template, width=int(template.shape[1] / rescale_factor))
(tH, tW) = resized.shape[:2]

result = cv2.matchTemplate(image, resized, cv2.TM_CCORR_NORMED )
(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)


(startX, startY) = (int(maxLoc[0]), int(maxLoc[1]))
(endX, endY) = (int((maxLoc[0] + tW)), int((maxLoc[1] + tH)))
# draw a bounding box around the detected result and display the image
cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 1)
# image = cv2.resize(image, (960, 540))
image = imutils.resize(image, width=int(result.shape[1] * 0.5))

cv2.imshow("Image", image)
cv2.waitKey(0)
