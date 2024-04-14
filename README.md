## Overview
### General

All source code is located in `flaresight`. Sample usage of most of the source code can be found in the `sample_usage` directory. 

**Beware** that I've not kept the sample_usage up to date. Much of this code was ported in from a previous python project I was working on, so you may face knick knack import and dependency errors for many of the notebooks. However, only minor fixes should be required to use them. The source code is verified to work.

You can ignore all source code directories except for `data` and `training`. These are the only directories particularly relevant to our project. The rest is just helper code for Google Cloud Platform (GCP) and file system manipulation.

### Installation

I use VSCode and I highly recommend you use it as well. It provides a significantly better notebook experience than Jupyter Notebooks (IMO). You can also use Colab if you really want to but it presents additional environment considerations and setup that I don't like dealing with.

1. Create your [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments)
    - This should be like 2 terminal commands (1 for creating the virtual environment and 1 for activating it). If you're using more commands than this you're doing it wrong

1. Install Python dependencies. <br></br> *Make sure your virtual environment is activated first.*
    ```bash {{ language: 'python' }}
    pip install -r requirements.txt
    ```

1. Install [libmagic](https://github.com/ahupp/python-magic?tab=readme-ov-file#debianubuntu)

### Data

The sensor data used for determining whether there is a fire is located in this repository in the `sensor_data` directory. The object detection data is located in a GCP bucket. You will have to download the data from this bucket (I can set you up with the proper credentials) or from the original source below to be able to use it in this repository.

### Getting Started

For exploring and visualizing the data, navigate to the `flaresight/sample_usage/data` directory. `detection.ipynb` contains code for visualizing yolo-labeled datasets and `localization.ipynb` contains code for exploring the sensor datasets we're using. These are still a work in progress so don't expect too much for now.

I'll also be adding code to the `flaresight/sample_usage/data` directory for sample training code. However, I've yet to do this as of now. I'll update this document when I do.



## Literature
### Surveys
- Survey of Modern Deep Learning Based Object Detection Models (Apr 2021) [[paper](https://www.sciencedirect.com/science/article/abs/pii/S1051200422001312?fr=RR-2&ref=pdf_download&rr=8712ed373c681454)]
- Video Fire Detection Methods Based on Deep Learning: Datasets, Methods, and Future Directions (2023) [[paper](https://www.mdpi.com/2571-6255/6/8/315)]
### Papers
- An Automatic Fire Detection System Based on Deep Convolutional Neural Networks for Low-power, Resource-constrained Devices (2022) [[paper](https://link.springer.com/article/10.1007/s00521-022-07467-z)]
- Machine Learning-Based Fire Detection: A Comprehensive Review and Evaluation of Classification Models (2023) [[paper]](https://joiv.org/index.php/joiv/article/view/2332)

## Sensor Datasets
### Wild
*Datasets that I've found "in the wild". They may or may not be used by researchers but I haven't verified whether they are or aren't.*
- Smoke Detection Dataset: [dataset](https://www.kaggle.com/datasets/deepcontractor/smoke-detection-dataset?resource=download)


## Image / Video Datasets
### Academia
*Datasets that I've found used by researchers in published academic journals.*
- VisiFire: [[dataset](http://signal.ee.bilkent.edu.tr/VisiFire/Demo/SampleClips.html)]
    1. Flame: 13 videos
    1. Smoke: 1 vidoes
    1. Forest Smoke: 21 videos
    1. Other: 2 videos
- VisiFire Annotated: [[paper](https://www.sciencedirect.com/science/article/pii/S2352340922001378)] [[dataset](https://zenodo.org/records/5893854)]
    1. 2,684 annotated frames of 12 commonly used videos from VisiFire dataset
- BoWFire: [[paper](https://arxiv.org/abs/1506.03495)] [[dataset](https://bitbucket.org/gbdi/bowfire-dataset/src/master/)]
    1. Fire: 119 images
        - Buildings, industrial, accidents, riots
    2. No Fire: 107 images
        - Fire-like objects in red or yellow hues
- Corsican Fire: [[paper](https://www.sciencedirect.com/science/article/pii/S0379711217302114)] [[dataset](https://cfdb.univ-corse.fr/donnees_images_page_134_menu,2.htm)]
    - Includes visual descriptions such as flame color, smoke, color, fire distance, etc.
    - Every images includes segmentation mask
    1. Visible Light: 500 images
    1. Visible Light / Near-Infrared: 100 images
    1. Multi-Modal: 5 sequences
- FESB MLID: [[dataset](http://wildfire.fesb.hr/index.php?option=com_content&view=article&id=66%20&Itemid=76)]
    - 11 semantic categories such as smoke, clouds/fog, sunlight, ..., unknown
    - Contains several challenging samples
    1. Natural Landscape: 400 images
- Smoke100k: [[paper](https://ieeexplore-ieee-org.ezproxy.lib.utexas.edu/document/9015309)] [[dataset](https://bigmms.github.io/cheng_gcce19_smoke100k/)]
    - Large-scale *synthetic* smoke dataset
    - Three subsets: Smoke 100k-L, Smoke 100k-M, Smoke 100k-H of varying smoke density
- Video Smoke Detection Dataset: [[dataset](http://staff.ustc.edu.cn/~yfn/vsd.html)]
    1. Smoke: 3 videos
    1. Non-smoke: 3 vidoes
    1. Smoke and Non-smoke: 4 videos
    1. Set 1: 552 smoke | 831 non-smoke images
    1. Set 2: 668 smoke | 817 non-smoke images
    1. Set 3: 2,201 smoke | 8,511 non-smoke images
    1. Set 4: 2,254 smoke | 8,363 non-smoke images
    - None-smoke images exhibit many similarites to the smoke images (color, shape, texture, etc.)
- FLAME Dataset: [[paper](https://www.sciencedirect.com/science/article/pii/S1389128621001201)] [[dataset](https://github.com/AlirezaShamsoshoara/Fire-Detection-UAV-Aerial-Image-Classification-Segmentation-UnmannedAerialVehicle)]
    - Aerial images/videos of burning piled detritus in Northern Arizona forsts
    - Four photographic modes: Normal, Fusion, WhiteHot, GreenHot
    1. Fire: 30,155 images
    1. Non-fire: 17,855 images
- D-Fire Dataset: [[dataset](https://github.com/gaiasd/DFireDataset)]
    - Designed for object-detection-method development (YOLO format labels)
    1. Fire-only: 1,164 images
    1. Smoke-only: 5,867 images
    1. Fire and Smoke: 4,658 images
    1. Negatives: 9,828 images
- DSDF: [[paper](https://www.sciencedirect.com/science/article/pii/S1051200422000719)] [[dataset](https://drive.google.com/file/d/1PuNZ5dfzsdVnn-tnohbhmvvriXSb7LWF/view)]
    1. Non-smoke w/out Fog: 6,528 images
    1. Smoke w/out Fog: 6,907 images
    1. None-Smoke w/ Fog: 1,518 images
    1. Smoke w/ Fog: 3,460 images
- DFS: [[paper](https://link.springer.com/article/10.1007/s11042-022-13580-x)] [[dataset](https://github.com/siyuanwu/DFS-FIRE-SMOKE-Dataset)]
    1. Large Flame: 3,357 images
    1. Medium Flame: 4,722 images
    1. Small Flame: 349 images
    1. Other: 1,034 images
    - "Other" are potential false positive objects such as vehicle lights, sunlight, metal lamps, etc.

### Wild
*Datasets that I've found "in the wild". They may or may not be used by researchers but I haven't verified whether they are or aren't.*
- Fire Detection from Images: [dataset](https://github.com/robmarkcole/fire-detection-from-images)
- Fire and Smoke Dataset: [dataset](https://www.kaggle.com/datasets/dataclusterlabs/fire-and-smoke-dataset?resource=download)
- FIRE Dataset: [dataset](https://www.kaggle.com/datasets/phylake1337/fire-dataset)
- Fire Detection from CCTV: [dataset](https://www.kaggle.com/datasets/ritupande/fire-detection-from-cctv)
- fireNET: [dataset](https://github.com/OlafenwaMoses/FireNET?tab=readme-ov-file)
- Yolov5 Fire Detection [dataset](https://github.com/spacewalk01/yolov5-fire-detection)

### Unavailable
*Datasets that look promising but couldn't be found for download.*
- Flame and Smoke Detection Dataset
    - *This dataset was withdrawn and I can't find it anywhere in which it can be downloaded. Would be clutch if we could find it because it would be very useful.*
    1. 100,000 flame and smoke images from various sources: surveillance cameras, drones, satellite, computer graphics, etc.
