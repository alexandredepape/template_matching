import numpy as np

from template_matching import icon_displayed


def is_similar(image1, image2):
    return image1.shape == image2.shape and not (np.bitwise_xor(image1, image2).any())


class ChampionIconManager:
    def __init__(self, icon):
        self.icon = icon

    def dashboard_displayed(self, frame):
        displayed, _ = icon_displayed(self.icon, frame)
        return displayed

    def score_changed(self, old_score, frame):
        displayed, new_score = icon_displayed(self.icon, frame)
        return not is_similar(old_score, new_score)
