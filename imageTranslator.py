# main.py

import os
import argparse
import cv2
import torch
from charnet.modeling.model import CharNet
from utils.image_utils import resize, draw_text_with_background
from utils.sort_utils import merge_texts_in_reading_order, sort_boxes
from translation.translategpt import translate
from charnet.config import cfg

def process_images(args):
    charnet = CharNet()
    charnet.load_state_dict(torch.load(cfg.WEIGHT))
    charnet.eval()
    charnet.cuda()

    for im_name in sorted(os.listdir(args.image_dir)):
        print(f"Processing {im_name}...")
        im_file = os.path.join(args.image_dir, im_name)
        im_original = cv2.imread(im_file)
        im, scale_w, scale_h, original_w, original_h = resize(im_original, size=cfg.INPUT_SIZE)
        
        with torch.no_grad():
            char_bboxes, char_scores, word_instances = charnet(im, scale_w, scale_h, original_w, original_h)
        
        merged = merge_texts_in_reading_order(word_instances)
        
        for instance in merged:
            instance.text = translate(instance.text, "Polish")

        # Draw the text with background
        im_with_text = draw_text_with_background(im_original, merged)
        
        # Save the processed image
        save_path = os.path.join(args.results_dir, im_name)
        cv2.imwrite(save_path, im_with_text)

def main():
    parser = argparse.ArgumentParser(description="Test")
    parser.add_argument("config_file", help="path to config file", type=str)
    parser.add_argument("image_dir", type=str)
    parser.add_argument("results_dir", type=str)
    args = parser.parse_args()

    cfg.merge_from_file(args.config_file)
    cfg.freeze()

    process_images(args)

if __name__ == '__main__':
    main()
