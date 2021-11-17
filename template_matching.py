import numpy as np
from cv2.cv2 import imread, matchTemplate, TM_CCORR_NORMED, minMaxLoc, rectangle, imshow, waitKey, imwrite
from imutils import resize


def icon_displayed(champion_icon, image):
    image_height, image_width = image.shape[:2]

    image = image[int(image_height * 0.79):, int(0.3125 * image_width):int(0.6875 * image_width)]
    image_height, image_width = image.shape[:2]

    # imshow('ee', image)
    # waitKey(0)
    (tH, tW) = champion_icon.shape[:2]

    # resized_template = get_resized_template(tW, champion_icon)
    # imshow("resized_template", resized_template)
    # (tH, tW) = resized_template.shape[:2]

    found = None
    max_scale = image_height / tH
    min_scale = 24 / tH
    # loop over the scales of the image
    for scale in np.linspace(min_scale, max_scale, 100)[::-1]:
        print(scale)
        # resize the image according to the scale, and keep track
        # of the ratio of the resizing
        resized = resize(champion_icon, width=int(champion_icon.shape[1] * scale))
        # imshow('resized', resized)
        # if the resized image is smaller than the template, then break
        # from the loop
        if image.shape[0] < resized.shape[0] or image.shape[1] < resized.shape[1]:
            print("image.shape[0] < resized.shape[0] or image.shape[1] < resized.shape[1]")
            continue
        # detect edges in the resized, grayscale image and apply template
        # matching to find the template in the image
        result = matchTemplate(image, resized, TM_CCORR_NORMED)
        (_, maxVal, _, maxLoc) = minMaxLoc(result)

        # if we have found a new maximum correlation value, then update
        # the bookkeeping variable
        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, scale)
            print('maxVal is higher', maxVal, 'with a scale of', scale, 'at', maxLoc)
            # (startX, startY) = (int(maxLoc[0]), int(maxLoc[1]))
            # (endX, endY) = (int((maxLoc[0] + tW * scale)), int((maxLoc[1] + tH * scale)))
            # result = image.copy()
            # rectangle(result, (startX, startY), (endX, endY), (0, 0, 255), 1)
            # resized = imutils.resize(result, width=int(result.shape[1] * 0.5))
    (_, maxLoc, scale) = found
    (startX, startY) = (int(maxLoc[0]), int(maxLoc[1]))
    (endX, endY) = (int((maxLoc[0] + tW * scale)), int((maxLoc[1] + tH * scale)))
    # draw a bounding box around the detected result and display the image
    rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 1)
    # image = resize(image, width=int(result.shape[1] * 0.5))

    imshow("Image", image)
    waitKey(0)
    print(maxVal)
    if maxVal < 0.85:
        return False, None
    left = (startX + ((endX - startX) / 2)) < image_width / 2
    print(left)
    if left:
        score_start_x = int(startX - 0.06 * image_width)
        score = image[startY:endY, score_start_x:int(score_start_x + image_width * 0.03)]
    else:
        score = image[startY:endY, int(startX + 0.13 * image_width):int(startX + image_width * 0.2)]
    imshow("score", score)
    waitKey(0)
    imwrite('score.png', score)

    return True, score


# def get_resized_template(tW, template):
#     rescale_factor = ICON_RATIO * tW
#     resized_template = resize(template, width=int(template.shape[1] / rescale_factor))
#     return resized_template


print(icon_displayed(imread('fiora.png'), imread('img.png')))
# print(icon_displayed(imread('aphelios.webp'), imread('img.png')))
