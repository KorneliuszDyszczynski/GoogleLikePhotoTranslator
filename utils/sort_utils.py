# utils/sort_utils.py

import numpy as np

class MergedInstance:
    def __init__(self, text, bbox):
        self.text = text
        self.bbox = bbox

def sort_boxes(word_instances, y_offset_ratio=0.3):
    boxes = [instance.bbox for instance in word_instances]
    
    levels = []
    for box in boxes:
        xmin, ymin, xmax, ymax = box
        box_height = ymax - ymin
        placed = False
        for level in levels:
            ref_xmin, ref_ymin, ref_xmax, ref_ymax = level[0]
            ref_box_height = ref_ymax - ref_ymin
            if abs(ymin - ref_ymin) <= max(ref_box_height, box_height) * y_offset_ratio:
                level.append(box)
                placed = True
                break
        if not placed:
            levels.append([box])
    
    for level in levels:
        level.sort(key=lambda box: box[0])

    levels.sort(key=lambda level: level[0][1])

    sorted_boxes = [box for level in levels for box in level]

    sorted_word_instances = []
    for sorted_box in sorted_boxes:
        for instance in word_instances:
            if instance.bbox == sorted_box:
                sorted_word_instances.append(instance)
                break
    
    return sorted_word_instances

def merge_texts_in_reading_order(word_instances, horizontal_threshold=40, vertical_threshold_ratio=0.5, vertical_offset_factor=0.5):
    def compute_bbox(box):
        x_coords = box[::2]
        y_coords = box[1::2]
        return min(x_coords), min(y_coords), max(x_coords), max(y_coords)

    for instance in word_instances:
        instance.bbox = compute_bbox(instance.word_bbox)

    word_instances = sort_boxes(word_instances)

    merged_instances = []
    current_text = []
    current_bbox = None

    def add_current_group():
        if current_text:
            merged_instances.append(MergedInstance(
                text=" ".join(current_text),
                bbox=[current_bbox[0], current_bbox[1],
                      current_bbox[2], current_bbox[1], 
                      current_bbox[2], current_bbox[3], 
                      current_bbox[0], current_bbox[3]]
            ))

    for i, instance in enumerate(word_instances):
        if not current_text:
            current_text = [instance.text]
            current_bbox = instance.bbox
            continue

        x1, y1, x2, y2 = instance.bbox
        cur_x1, cur_y1, cur_x2, cur_y2 = current_bbox

        current_height = cur_y2 - cur_y1
        vertical_threshold = current_height * vertical_threshold_ratio

        horizontally_close = x1 - cur_x2 <= horizontal_threshold
        vertically_aligned = abs(y1 - cur_y1) <= vertical_threshold

        if horizontally_close and vertically_aligned:
            current_text.append(instance.text)
            current_bbox = (
                min(cur_x1, x1), min(cur_y1, y1),
                max(cur_x2, x2), max(cur_y2, y2)
            )
        else:
            add_current_group()
            current_text = [instance.text]
            current_bbox = instance.bbox

    add_current_group()

    return merged_instances
