import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

from PIL import Image
from tqdm import tqdm, trange


def video2slide(filename):


    videoname = './videos/screen.mp4'
    capture = cv2.VideoCapture(videoname)
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    previous_frame = np.zeros((frame_height, frame_width, 3), np.uint8)


    output = Image.fromarray(previous_frame)
    slides = []

    if capture.isOpened():
        for frame_current in tqdm(range(0, frame_count, 100)):
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_current)
            ret, img=capture.read() # img 就是一帧图片

            # print("frame_current: ", frame_current, "total frames: ", frame_count)
            if previous_frame.size != img.size or ssim(previous_frame, img, channel_axis=2) < 0.9:
                slides.append(Image.fromarray(img[: , : , : : -1]))
            previous_frame = img
            # 可以用 cv2.imshow() 查看这一帧，也可以逐帧保存


        output.save("./output/" + filename + ".pdf", "pdf", save_all=True, append_images=slides)
    else:
        print('视频打开失败！')

