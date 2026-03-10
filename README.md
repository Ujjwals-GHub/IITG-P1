# Object Detection Assistant for the Visually Impaired

This is a simple Python project meant for a college assignment. It uses a pre-trained
MobileNet SSD object detection model with OpenCV to identify objects in front of a
camera and speak warnings to help blind users avoid obstacles.

## Structure

```
project/
└── src/
    ├── model.py        # helper to load DNN model
    ├── detector.py     # functions to perform detection
    └── main.py         # run the camera loop and speak warnings
```

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Download the pre-trained weights and config for MobileNet SSD. You can get them from OpenCV's GitHub:  
   - `MobileNetSSD_deploy.caffemodel` (about 25 MB) –
     https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/MobileNetSSD_deploy.caffemodel  
   - `MobileNetSSD_deploy.prototxt.txt` (model architecture) –
     https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/MobileNetSSD_deploy.prototxt.txt  
   Download each file (use the “Download” button or right‑click → Save As) and place
   them in the project root or update the paths in `src/model.py` if you put them
   elsewhere.
3. Run the system:
   ```bash
   python src/main.py
   ```

### Notes
- The code is intentionally simple and verbose to make it easy to understand.
- This project doesn't include real training code; it uses a pre-trained model from OpenCV's
  DNN module. There is a toy example of what training might look like in `src/train_simple.py`.
  That script does not produce a usable detector but is written to illustrate the general flow.

### Training & datasets
If you decide to train your own detector instead of using the supplied model, you
will need a labelled dataset containing the objects you care about. Common public
datasets used for object detection include:

- **COCO (Common Objects in Context)** – a large dataset with 80 everyday object
  categories such as `person`, `bicycle`, `car`, `dog`, etc. Good general-purpose
  dataset, and the pre‑trained MobileNet SSD used here was trained on COCO.
- **Pascal VOC** – smaller than COCO, with 20 categories, often used for simple
  academic experiments.
- **Open Images** – very large, with hundreds of classes and many images, but more
  complex to work with.

> Since this is your first time, the easiest way to get started is to use an
> existing training framework rather than building everything from scratch.

#### Option A – TensorFlow Object Detection API (recommended)
1. Follow the [official setup guide](https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html)
   to install the API and its dependencies (TensorFlow 2.x, protobuf, etc.).
2. Download a **pre‑configured model** from the [model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md)
   such as `ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8`. This gives you a
   pipeline configuration file and a checkpoint with COCO weights.
3. Use the `create_coco_tf_record.py` script included in the API to convert the
   COCO JSON annotations to TFRecord files:
   ```bash
   python models/research/object_detection/dataset_tools/create_coco_tf_record.py \
       --logtostderr \
       --dataset_dir=/path/to/coco \
       --output_dir=/path/to/output \
       --split=train
   ```
4. Edit the model's `pipeline.config` to point to your TFRecords, label map, and
   set `num_classes` (80 for full COCO or fewer if you filter).
5. Run training with the provided script:
   ```bash
   python models/research/object_detection/model_main_tf2.py \
       --pipeline_config_path=/path/to/pipeline.config \
       --model_dir=/path/to/train_dir \
       --num_train_steps=20000
   ```
6. After training you can export a frozen inference graph and use it with the
   `src/detector.py` code by replacing the model loading logic.

This approach handles all the messy details (anchors, loss functions, data
pipeline) for you. There are many tutorials and example configs online; just
search “TensorFlow Object Detection API COCO training.”

#### Option B – Lightweight custom script
If you really want to write your own training code, you can start from
`src/train_simple.py` and expand it. A very simple sequence would be:

1. Use `tensorflow_datasets` to download COCO and iterate through examples.
   ```python
   import tensorflow_datasets as tfds
   dataset, info = tfds.load('coco/2017', split='train', with_info=True)
   ```
2. Build a tiny Keras model (e.g. MobileNet backbone + a few conv layers) that
   predicts bounding boxes and class logits for a fixed set of anchors.
3. Write a custom loss that combines classification and box regression.
4. Call `model.fit(dataset.batch(8), epochs=10)` and save the weights.

This custom route requires more work and is suitable once you understand the
fundamentals. The existing `train_simple.py` is intentionally minimal; feel free
to rename or expand it as you learn.

You can also create your own dataset by collecting images and annotating them with
bounding boxes (tools like [LabelImg](https://github.com/tzutalin/labelImg) are
popular). The labels must then be converted to the format expected by your training
framework (e.g. TensorFlow Record files for TensorFlow, or `.txt` files for Darknet).

The `src/train_simple.py` file shows a trivial training loop and is just for
illustration; training a real detector involves data preprocessing, data augmentation,
and using a proper architecture (e.g. SSD, YOLO, Faster‑RCNN) with enough examples.

## Acknowledgements
The object detection model is based on MobileNet SSD and COCO classes.
