import requests
import cv2
import numpy as np
import sys
from PIL import Image

FRAME_RATE = 5

URL = "https://thisanimedoesnotexist.ai/results/psi-{:}/seed{:}.png"


def getImage(creativity: float, seed: int):
    if creativity < 0.3 or creativity > 2.0:
        return
    creativity_str = str(round(creativity, 1))
    seed_str = str(seed).rjust(5, "0")
    img_url = URL.format(creativity_str, seed_str)
    url_response = requests.get(img_url)
    path_str = "test_" + seed_str + "_" + creativity_str + ".png"
    data = []
    for chunk in url_response:
        data.extend(chunk)
    img_array = np.array(bytearray(data), dtype=np.uint8)
    return cv2.imdecode(img_array, -1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a seed for this to work.")
        exit(1)

    try:
        seed = int(sys.argv[1])
    except:
        print("Seed needs to be a number.")
        exit(1)
    if seed > 99999:
        print("Seed needs to be smaler than.")
        exit(1)

    all_img = []
    for num in range(3, 21):
        all_img.append(getImage(num / 10, seed))
    frameSize = (512, 512)
    seed_str = str(seed).rjust(5, "0")
    out = cv2.VideoWriter(
        "output_video_" + seed_str + ".avi",
        cv2.VideoWriter_fourcc(*"DIVX"),
        FRAME_RATE,
        frameSize,
    )

    out_reversed = cv2.VideoWriter(
        "output_video_" + seed_str + "w_reversed" + ".avi",
        cv2.VideoWriter_fourcc(*"DIVX"),
        FRAME_RATE,
        frameSize,
    )

    temp = all_img.copy()
    temp.reverse()
    img_reversed = all_img.copy()
    img_reversed.extend(temp)
    del temp

    PIL_images = []
    PIL_images_reversed = []
    for img in all_img:
        out.write(img)
        temp = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        PIL_images.append(Image.fromarray(temp))
    for img in img_reversed:
        out_reversed.write(img)
        temp = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        PIL_images_reversed.append(Image.fromarray(temp))
    PIL_images[0].save(
        fp="output_gif_" + seed_str + ".gif",
        format="GIF",
        append_images=PIL_images[1:],
        save_all=True,
        duration=1000 / FRAME_RATE,
        loop=0,
    )
    PIL_images_reversed[0].save(
        fp="output_gif_" + seed_str + "w_reversed" + ".gif",
        format="GIF",
        append_images=PIL_images_reversed[1:],
        save_all=True,
        duration=1000 / FRAME_RATE,
        loop=0,
    )
