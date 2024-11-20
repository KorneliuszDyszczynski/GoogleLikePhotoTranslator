# Copyright (c) Malong Technologies Co., Ltd.
# All rights reserved.
#
# Contact: github@malong.com
#
# This source code is licensed under the LICENSE file in the root directory of this source tree.

import torch
from charnet.modeling.model import CharNet
import cv2, os
import numpy as np
import argparse
from charnet.config import cfg
import matplotlib.pyplot as plt


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
    img_word_ins = image.copy()

    for word_ins in word_instances:
        word_bbox = word_ins.word_bbox
        text = word_ins.text

        # Get bounding box dimensions
        box_width = abs(word_bbox[2] - word_bbox[0])
        box_height = abs(word_bbox[5] - word_bbox[1])

        # Fill the box with a background color (light blue for example)
        box_pts = word_bbox[:8].reshape((-1, 2)).astype(np.int32)
        cv2.fillPoly(img_word_ins, [box_pts], (255, 255, 204))

        # Dynamically calculate font size based on box height and width
        font_scale = min(box_width, box_height) / 40.0  # Scale factor (adjust 30.0 for different font sizes)
        font_scale = max(0.3, font_scale)  # Ensure the font size isn't too small
        font_thickness = int(box_height // 20)  # Adjust font thickness based on box height

        # Calculate text size and position to center the text inside the box
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
        text_width, text_height = text_size

        # Calculate the position to center the text inside the box
        text_x = int(word_bbox[0] + (box_width - text_width) / 2)
        text_y = int(word_bbox[1] + (box_height + text_height) / 2)

        # Draw the text on the image
        cv2.putText(img_word_ins, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), font_thickness)

    return img_word_ins

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test")

    parser.add_argument("config_file", help="path to config file", type=str)
    parser.add_argument("image_dir", type=str)
    parser.add_argument("results_dir", type=str)

    args = parser.parse_args()

    cfg.merge_from_file(args.config_file)
    cfg.freeze()

    print(cfg)

    charnet = CharNet()
    charnet.load_state_dict(torch.load(cfg.WEIGHT))
    charnet.eval()
    charnet.cuda()

    for im_name in sorted(os.listdir(args.image_dir)):
        print("Processing {}...".format(im_name))
        im_file = os.path.join(args.image_dir, im_name)
        im_original = cv2.imread(im_file)
        im, scale_w, scale_h, original_w, original_h = resize(im_original, size=cfg.INPUT_SIZE)
        with torch.no_grad():
            char_bboxes, char_scores, word_instances = charnet(im, scale_w, scale_h, original_w, original_h)
        # Draw the text with background
        im_with_text = draw_text_with_background(im_original, word_instances)

        # Display the image using matplotlib
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(im_with_text, cv2.COLOR_BGR2RGB))
        plt.axis('off')  # Turn off the axes
        plt.title(f"Processed Image: {im_name}")
        plt.show()
