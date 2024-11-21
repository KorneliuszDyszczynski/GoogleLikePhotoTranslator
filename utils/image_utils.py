# utils/image_utils.py

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from charnet.config import cfg

def resize(im, size):
    h, w, _ = im.shape
    scale = max(h, w) / float(size)
    image_resize_height = int(round(h / scale / cfg.SIZE_DIVISIBILITY) * cfg.SIZE_DIVISIBILITY)
    image_resize_width = int(round(w / scale / cfg.SIZE_DIVISIBILITY) * cfg.SIZE_DIVISIBILITY)
    scale_h = float(h) / image_resize_height
    scale_w = float(w) / image_resize_width
    im = cv2.resize(im, (image_resize_width, image_resize_height), interpolation=cv2.INTER_LINEAR)
    return im, scale_w, scale_h, w, h

def draw_text_with_background(image, word_instances):
    img_word_ins = Image.fromarray(image)
    draw = ImageDraw.Draw(img_word_ins)
    font = ImageFont.truetype("arial.ttf", size=30)

    for word_ins in word_instances:
        word_bbox = word_ins.bbox
        text = word_ins.text

        # Get bounding box dimensions
        box_width = abs(word_bbox[2] - word_bbox[0])
        box_height = abs(word_bbox[5] - word_bbox[1])

        # Fill the box with a background color
        box_pts = np.array(word_bbox)[:8].reshape((-1, 2)).astype(np.int32)
        polygon = [tuple(pt) for pt in box_pts]
        draw.polygon(polygon, fill=(255, 255, 204))

        font_size = 30
        while True:
            left, top, right, bottom = font.getbbox(text)
            text_width = right - left
            text_height = bottom - top
            if text_width <= box_width * 0.9 and text_height <= box_height * 0.9:
                break
            font_size -= 1
            if font_size < 10:
                font_size = 10
                break
            font = ImageFont.truetype("arial.ttf", size=font_size)

        text_x = int(word_bbox[0] + (box_width - text_width) / 2)
        text_y = int(word_bbox[1] + (box_height - text_height) / 2)

        text_x = max(text_x, word_bbox[0])
        text_y = max(text_y, word_bbox[1])

        draw.text((text_x, text_y), text, font=font, fill=(0, 0, 255))

    return np.array(img_word_ins)
