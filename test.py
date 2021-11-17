import cv2
import numpy as np
import imutils

image = cv2.imread('img1.png')
template = cv2.imread('katarina.png')

(tH, tW) = template.shape[:2]
image_height, image_width = image.shape[:2]

image = image[int(image_height * 0.79):, int(0.47 * image_width):int(0.5275 * image_width)]
# image_height, image_width = image.shape[:2]
rezised = imutils.resize(image, width=int(image_width * 0.2))
cv2.imshow('rezised', rezised)
cv2.waitKey(0)

# load the image, convert it to grayscale, and initialize the
# bookkeeping variable to keep track of the matched region
found = None
# loop over the scales of the image
for scale in np.linspace(0.1, 1, 50)[::-1]:
    print(scale)
    # resize the image according to the scale, and keep track
    # of the ratio of the resizing
    resized = imutils.resize(template, width=int(template.shape[1] * scale))
    cv2.imshow('resized', resized)
    r = template.shape[1] / float(resized.shape[1])
    # if the resized image is smaller than the template, then break
    # from the loop
    if image.shape[0] < resized.shape[0] or image.shape[1] < resized.shape[1]:
        continue
    # detect edges in the resized, grayscale image and apply template
    # matching to find the template in the image
    result = cv2.matchTemplate(image, resized, cv2.TM_CCOEFF_NORMED)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

    # if we have found a new maximum correlation value, then update
    # the bookkeeping variable
    if found is None or maxVal > found[0]:
        found = (maxVal, maxLoc, scale)
        print('maxVal is higher', maxVal, 'with a scale of', scale, 'at', maxLoc)
        (startX, startY) = (int(maxLoc[0]/ 0.2), int(maxLoc[1]/ 0.2))
        (endX, endY) = (int((maxLoc[0] + tW * scale/ 0.2)), int((maxLoc[1] + tH * scale/ 0.2)))
        cv2.rectangle(rezised, (startX, startY), (endX, endY), (0, 0, 255), 1)
        cv2.imshow('rezised', rezised)
        cv2.waitKey(0)
# unpack the bookkeeping variable and compute the (x, y) coordinates
# of the bounding box based on the resized ratio
(_, maxLoc, scale) = found
print(found)
(startX, startY) = (int(maxLoc[0]), int(maxLoc[1]))
(endX, endY) = (int((maxLoc[0] + tW * scale)), int((maxLoc[1] + tH * scale)))
# draw a bounding box around the detected result and display the image
cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 1)
# image = cv2.resize(image, (960, 540))
cv2.imshow("Image", image)
cv2.waitKey(0)