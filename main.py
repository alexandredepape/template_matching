from cv2.cv2 import imshow, VideoCapture, waitKey, imread

from frame_manager import ChampionIconManager

old_score = None
vidcap = VideoCapture('video.mp4')
success, frame = vidcap.read()
# champion_icon_manager = ChampionIconManager(imread('jarvan.webp'))
champion_icon_manager = ChampionIconManager(imread('aphelios.webp'))

while success:
    imshow("frame", frame)
    waitKey(0)
    if champion_icon_manager.dashboard_displayed(frame):
        score = champion_icon_manager.score_changed(old_score, frame)
        old_score = score


    success, frame = vidcap.read()
