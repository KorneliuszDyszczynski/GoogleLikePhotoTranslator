# Text Recognition and Translation with CharNet and ChatGPT
This project performs text recognition and translation on images by leveraging the CharNet model for scene text detection, OpenAI's ChatGPT for translating recognized text, and OpenCV/Pillow for image manipulation. The process involves extracting text from images, translating it into a target language (default: Polish), and rendering the translated text onto the image. This project is a simple after-hours play, done mostly in one sitting, making it an enjoyable and straightforward way to experiment with text recognition and language translation on images.

## Early Test Results


## Features
- **Text Recognition**: Utilizes the CharNet model to detect and recognize text from images, even in complex scenes.
- **Text Translation**: Translates the recognized text using OpenAI's ChatGPT, with Polish as the default target language.
- **Post-Processing**: Uses OpenCV and Pillow libraries to manipulate and draw the translated text onto the original image, with a background color for visibility.
- **Customizable Configuration**: All parameters, such as model path, input size, and target language, are configurable through a cfg.py configuration file, providing flexibility for different use cases.

### Install Dependencies
**Important**: Make sure CUDA is installed on your system to fully leverage the capabilities of your GPU.
Once your environment is activated, install PyTorch by following the instructions from the link below:
[PyTorch Installation](https://pytorch.org/get-started/locally/)

Example for Windows and CUDA 12.4 run this command:
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

To install the required dependencies, run the following:
```
pip install -r requirements.txt
```

**Important**: Please download Charnet trained weights from [official repository](https://github.com/msight-tech/research-charnet)

[Alternative link](https://drive.google.com/file/d/19wxT-MtCo5kzf1dbEPQ7ICG4mgqvtLV3/view?usp=sharing)

## Configuration (cfg.py)
The configuration for the project is stored in the cfg.py file. Here, you can define various parameters like input size, model weights, font settings, and translation options.


## Usage
### Running the Code
To run the project, you need to pass the configuration file, image directory, and result directory via the command line. For example:

```
python main.py --config_file path_to_config_file --image_dir path_to_input_images --results_dir path_to_output_images
```
### Command-Line Arguments
- --config_file: The path to the configuration file (cfg.py or a .yaml file).
- --image_dir: The directory containing the input images to process.
- --results_dir: The directory to save the processed images.
### Example Usage
```
python main.py --config_file charnet/config.py --image_dir data/images --results_dir results/
```
