<div align="center">
  <img src="https://raw.githubusercontent.com/Ikomia-hub/skimage_threshold/main/icons/scikit.png" alt="Algorithm icon">
  <h1 align="center">skimage_threshold</h1>
</div>
<br />
<p align="center">
    <a href="https://github.com/Ikomia-hub/skimage_threshold">
        <img alt="Stars" src="https://img.shields.io/github/stars/Ikomia-hub/skimage_threshold">
    </a>
    <a href="https://app.ikomia.ai/hub/">
        <img alt="Website" src="https://img.shields.io/website/http/app.ikomia.ai/en.svg?down_color=red&down_message=offline&up_message=online">
    </a>
    <a href="https://github.com/Ikomia-hub/skimage_threshold/blob/main/LICENSE.md">
        <img alt="GitHub" src="https://img.shields.io/github/license/Ikomia-hub/skimage_threshold.svg?color=blue">
    </a>    
    <br>
    <a href="https://discord.com/invite/82Tnw9UGGc">
        <img alt="Discord community" src="https://img.shields.io/badge/Discord-white?style=social&logo=discord">
    </a> 
</p>

Compilation of well-known thresholding methods from scikit-image library: Otsu, Multi-Otsu, Yen, IsoData, Li, Mean, Minimum, Local, Niblack, Sauvola Triangle, Hysteresis.

![Results](https://raw.githubusercontent.com/Ikomia-hub/skimage_threshold/feat/new_readme/icons/results.png)

## :rocket: Use with Ikomia API

#### 1. Install Ikomia API

We strongly recommend using a virtual environment. If you're not sure where to start, we offer a tutorial [here](https://www.ikomia.ai/blog/a-step-by-step-guide-to-creating-virtual-environments-in-python).

```sh
pip install ikomia
```

#### 2. Create your workflow

[Change the sample image URL to fit algorithm purpose]

```python
from ikomia.dataprocess.workflow import Workflow
from ikomia.utils.displayIO import display

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="skimage_threshold", auto_connect=True)

# Run on your image
wf.run_on(url="https://cdn.pixabay.com/photo/2023/09/10/00/49/lovebird-8244066_960_720.jpg")

# Display result
display(algo.get_output(0).get_image())
```

## :sunny: Use with Ikomia Studio

Ikomia Studio offers a friendly UI with the same features as the API.

- If you haven't started using Ikomia Studio yet, download and install it from [this page](https://www.ikomia.ai/studio).

- For additional guidance on getting started with Ikomia Studio, check out [this blog post](https://www.ikomia.ai/blog/how-to-get-started-with-ikomia-studio).

## :pencil: Set algorithm parameters

- **local_method** (str, default="Otsu"): Method used for thresholding. Must be one of:
  - "Otsu"
  - "Yen"
  - "Iso data"
  - "Li"
  - "Mean"
  - "Minimum"
  - "Local"
  - "Niblack"
  - "Sauvola"
  - "Triangle"
  - "Multi otsu"
  - "Hysteresis"

You can find more information about what these methods do and what are the complementary parameters here [skimage doc](https://scikit-image.org/docs/stable/api/skimage.filters.html)

*Note*: parameter key and value should be in **string format** when added to the dictionary.

```python
from ikomia.dataprocess.workflow import Workflow

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="skimage_threshold", auto_connect=True)

algo.set_parameters({
    "local_model": "Iso data",
    "isodata_nbins": "128",
})

# Run on your image  
wf.run_on(url="https://cdn.pixabay.com/photo/2023/09/10/00/49/lovebird-8244066_960_720.jpg")

```

## :mag: Explore algorithm outputs

Every algorithm produces specific outputs, yet they can be explored them the same way using the Ikomia API. For a more in-depth understanding of managing algorithm outputs, please refer to the [documentation](https://ikomia-dev.github.io/python-api-documentation/advanced_guide/IO_management.html).

```python
from ikomia.dataprocess.workflow import Workflow

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="skimage_threshold", auto_connect=True)

# Run on your image  
wf.run_on(url="https://cdn.pixabay.com/photo/2023/09/10/00/49/lovebird-8244066_960_720.jpg")

# Iterate over outputs
for output in algo.get_outputs():
    # Print information
    print(output)
    # Export it to JSON
    output.to_json()
```