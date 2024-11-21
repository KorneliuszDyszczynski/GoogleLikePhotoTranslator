# config.py
from yacs.config import CfgNode as CN

cfg = CN()

# General settings
cfg.INPUT_SIZE = 800  # The size to which input images will be resized
cfg.SIZE_DIVISIBILITY = 32  # Ensures that the image dimensions are divisible by this value
cfg.WEIGHT = "path_to_pretrained_weights.pth"  # Path to the pre-trained model weights
cfg.FONTS_PATH = "arial.ttf"  # Path to the font used for text drawing

# Model configuration
cfg.MODEL = CN()
cfg.MODEL.TYPE = "CharNet"  # Model type (in case there are multiple models in the future)
cfg.MODEL.FEATURE_DIM = 512  # Feature dimension (based on CharNet's architecture)
cfg.MODEL.BACKBONE = "resnet50"  # Backbone model used for feature extraction
cfg.MODEL.PRETRAINED = True  # Whether to use a pre-trained backbone

# Image processing settings
cfg.IMAGE = CN()
cfg.IMAGE.RESIZE_MODE = "scale"  # Mode of resizing (could be 'scale' or 'crop')
cfg.IMAGE.RESIZE_METHOD = "linear"  # Method for resizing (linear, nearest, etc.)

# Post-processing settings
cfg.POSTPROCESSING = CN()
cfg.POSTPROCESSING.DRAW_TEXT_COLOR = (0, 0, 255)  # Color for the text (RGB)
cfg.POSTPROCESSING.BACKGROUND_COLOR = (255, 255, 204)  # Background color for the text box (RGB)
cfg.POSTPROCESSING.FONT_SIZE = 30  # Initial font size used for text drawing

# Translation settings
cfg.TRANSLATION = CN()
cfg.TRANSLATION.TARGET_LANGUAGE = "Polish"  # Default target language for translation

# Horizontal and vertical thresholds used in sorting and merging word instances
cfg.SORTING = CN()
cfg.SORTING.HORIZONTAL_THRESHOLD = 40  # Maximum horizontal gap for merging
cfg.SORTING.VERTICAL_THRESHOLD_RATIO = 0.5  # Ratio to determine vertical alignment for merging
cfg.SORTING.VERTICAL_OFFSET_FACTOR = 0.5  # Factor to adjust the vertical offset for large letters

# Other configurations can be added as necessary

cfg.freeze()  # Freeze the configuration to prevent accidental modification
