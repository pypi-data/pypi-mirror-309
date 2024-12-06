
# BinaExperts SDK

The BinaExperts SDK is a comprehensive computer vision toolkit, providing essential tools for dataset management, conversion, and data processing. While initially focused on seamless format conversion (COCO, YOLO, etc.), the SDK is designed to grow into a full-featured suite for computer vision tasks.

## Installation

You can install the BinaExperts SDK directly from PyPI using `pip`:

```bash
pip install binaexperts
```
## Usage

Once you've installed the BinaExperts SDK, you can start converting datasets between different formats. Here's how to use the SDK:

### Basic Example

```python
import binaexperts
convertor = binaexperts.Convertor()

# Convert COCO format to YOLO format
convertor.convert(
    target_format='yolo',
    source_path='path/to/source_format_dataset.zip', 
    target_path='path/to/target_format_dataset.zip' #Optional
)
```
### Advanced Examples
#### Example: Dynamic Data Augmentation for Model Robustness and Conversion to COCO Format
##### Use Case:
The user wants to dynamically apply transformations (e.g., flipping, rotating, adjusting brightness) to a YOLO dataset, enhancing model robustness, and then convert the augmented dataset to COCO format.
##### Solution code:

```python
import io
from PIL import Image
import random
import numpy as np
import binaexperts

# Initialize convertor
convertor = binaexperts.Convertor()

# Define the target format
target_format = 'coco'

# Paths
source_path = 'path/to/yolo_dataset.zip'
destination_path = 'path/to/augmented_coco_dataset.zip'

# Perform the initial conversion to COCO format
with open(source_path, 'rb') as src, io.BytesIO() as temp_buffer:
    convertor.convert(target_format, src, temp_buffer)
    temp_buffer.seek(0)

    # Load the in-memory COCO data
    coco_data = temp_buffer.getvalue()

# Augment the image data in-memory
augmented_images = []
for image_data in coco_data['images']:
    image_content = io.BytesIO(image_data['image_content'])
    image = Image.open(image_content)

    # Random transformations
    if random.choice([True, False]):
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    if random.choice([True, False]):
        image = image.rotate(random.randint(-25, 25))
    brightness_factor = random.uniform(0.5, 1.5)
    image = Image.fromarray(np.clip(np.array(image) * brightness_factor, 0, 255).astype(np.uint8))

    # Update image data
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    image_data['image_content'] = img_byte_arr.getvalue()
    augmented_images.append(image_data)

coco_data['images'] = augmented_images

# Save the augmented dataset to the final destination
with open(destination_path, 'wb') as dest:
    convertor.convert(target_format, target_format, io.BytesIO(coco_data), dest)
```
#### IO Support
This SDK supports both file-based and in-memory IO operations, allowing you to perform conversions without needing to write intermediate files to disk. This is especially useful in scenarios where data needs to be processed on-the-fly or in serverless environments.

#### Example: Converting with In-Memory Data
In this example, we demonstrate how to use the SDK to convert a dataset directly from an in-memory BytesIO object and obtain the result in memory, without writing to disk.

##### Use Case:
A user needs to read a YOLO dataset from an in-memory BytesIO stream, convert it to COCO format, and retrieve the output as a BytesIO object to avoid intermediate file handling.
##### Code Solution:
```python
import io
import binaexperts

# Simulate an in-memory YOLO dataset as a BytesIO object
yolo_dataset_io = io.BytesIO()
# Assuming yolo_dataset_zip_content is the binary content of a YOLO zip file
yolo_dataset_io.write(yolo_dataset_zip_content)
yolo_dataset_io.seek(0)  # Reset to the beginning

# Initialize the Convertor
convertor = binaexperts.Convertor()

# Perform the conversion from YOLO to COCO format using in-memory IO
output_coco_io = convertor.convert(
    target_format='coco',
    source=yolo_dataset_io,  # Input as BytesIO
    destination=None  # Output will be a BytesIO object
)

# Access the converted COCO dataset in memory
coco_data = output_coco_io.getvalue()

# further processing or sending `coco_data` over a network...
```

## Supported Formats

The BinaExperts SDK currently supports the following formats:

- COCO
- YOLO
- BinaExperts

## Features
- Dataset Conversion: Seamless conversion between COCO, YOLO, and BinaExperts formats.
- Modular Design: Easily extendable to support new formats and datasets in the future.
- This SDK supports both file-based and in-memory IO operations.

## Future Roadmap
- Local Inference: Add support for local inference with trained models directly within the SDK.
- Live Inference: Future versions will support live inference from video streams or camera inputs.
- Auto Training: Automatic training workflows with model selection, hyperparameter tuning, and training pipelines.
- Dataset Validation: Automatic validation of dataset integrity, including checks for missing annotations, corrupted images, and data consistency.
- Additional Format Support: Future support for additional dataset formats, expanding beyond COCO, YOLO, and BinaExperts.
- We Welcome Your Suggestions: We encourage you to provide suggestions for additional features you would like to see in the SDK.

## Project Structure

```plaintext
binaexperts_sdk/
│
├── binaexperts/
│   ├── __init__.py
│   ├── convertors/
│   │   ├── __init__.py
│   │   ├── base.py                   # Base class for converters
│   │   ├── const.py                  # Constants used for dataset conversion settings and formats
│   │   ├── convertor.py              # Main class for managing dataset conversions
│   ├── schema/
│   │   ├── __init__.py
│   │   ├── coco.json                 # Schema for COCO format
│   │   ├── yolo.json                 # Schema for YOLO format
│   │   ├── binaexperts.json          # Schema for BinaExperts format
│   │   ├── normalizer.json           # Schema for Normalizer format
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── utils.py
│ 
│
├── setup.py                          # Setup script for packaging the SDK
├── README.md                         # Project documentation
└── requirements.txt                  # Python dependencies

```
## Future Project Structure

```plaintext
binaexperts_sdk/
│
├── binaexperts/
│   ├── __init__.py
│   ├── convertors/
│   │   ├── __init__.py
│   │   ├── base.py                   # Base class for converters
│   │   ├── const.py                  # Constants used for dataset conversion settings and formats
│   │   ├── convertor.py              # Main class for managing dataset conversions
│   │   ├── inference.py              # Main class for local and live inferences
│   ├── schema/
│   │   ├── __init__.py
│   │   ├── coco.json                 # Schema for COCO format
│   │   ├── yolo.json                 # Schema for YOLO format
│   │   ├── binaexperts.json          # Schema for BinaExperts format
│   │   ├── normalizer.json           # Schema for Normalizer format
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── utils.py                  # Utility functions
│   │   ├── loadhelpers.py            # Load helper functions
│ 
│
├── setup.py                          # Setup script for packaging the SDK
├── README.md                         # Project documentation
└── requirements.txt                  # Python dependencies

```

## Contribution
The BinaExperts SDK was designed and developed by Nastaran Dab, who also serves as the project’s team leader.
If you are interested in contributing, please reach out to the project team for guidelines.

## Acknowledgments
Thank you from the BinaExperts team for your support of this project!
Made with dedication and innovation by Nastaran Dab.

## License
This project is licensed under the MIT License. 