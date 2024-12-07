<img src="https://gitlab.com/ml-ppa-derivatives/torchrender3d/-/raw/main/graphics/logo_with_name.png" alt= “PackageLogo” width=50% height=50%>

## Introduction

TorchRender3D is an advanced visualization tool designed for PyTorch developers and researchers to explore the internal structure of custom neural networks specifically CNNs. Leveraging the power of VTK (Visualization Toolkit) for 3D rendering, TorchRender3D enables real-time, interactive visualizations of neural network layers and outputs.

## Requirements

- **Operating Systems**: 
  - macOS, Windows, or Linux (excluding Linux on ARM64 architecture)
  
- **Python Version**: 
  - Python 3.x (>=3.10 recommended)

- **Dependencies**: 
  - [VTK](https://vtk.org) (Visualization Toolkit)
  - [NumPy](https://numpy.org)
  - [PyTorch](https://pytorch.org)

## Features

- Visualize neural network parameters in a 3D space.
- Interactive rendering with support for keyboard and mouse events.
- Capture and save rendered frames as TIFF images for animation purposes.
- Support for different neural network architectures.
- Easy-to-use interface for integrating with existing PyTorch models.

Below is a simple render example of the learnable parameter space of a simple CNN:

<img src="https://gitlab.com/ml-ppa-derivatives/torchrender3d/-/raw/main/graphics/cnn_output.gif" alt= “feature_example” width=30% height=30%>

## Installation

- Clone from gitlab repo as

```bash
git clone https://gitlab.com/ml-ppa-derivatives/torchrender3d.git
```

- Create a virtual environment (recomended but can be skipped) as and activate it

```bash
python -m venv <venv_name>
```

```bash
source <venv_name>/bin/activate
```

- Install using pip from local as 

```bash
pip install -e .
```

- Or from PyPI as 
```bash
pip install torchrender3d 
```

## Implementation

### Plotting network parameters

- Define or import your own neural network developed using pytorch

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchrender3d import PlotNetwork3D

#: Define a simple neural net or import your own model
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()        
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1) 
        self.flatten_method = nn.Flatten()       
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):        
        x = self.pool(F.relu(self.conv1(x)))  # 28x28 -> 14x14 after pool
        x = self.pool(F.relu(self.conv2(x)))  # 14x14 -> 7x7 after pool       
        x = self.flatten_method(x)
        x = F.relu(self.fc1(x))               # Fully connected layer
        x = self.fc2(x)                       # Output layer
        return x

stored_network_params_path = 'path_to_trained_model'
torch.save(model.state_dict(), stored_network_params_path)
```

- Instantiate the model and the model plotter

```python
model = SimpleCNN()    
stored_network_params_path = './example_nets/simplecnn'
torch.save(model.state_dict(), stored_network_params_path)

model_plotter = PlotNetwork3D(
                              neural_network=model,
                              stored_network_params_path=stored_network_params_path, #: can be a random string, but required a valid path for updating feature
                              normalize=False,
                              plot_type='param', # if 'output' then plots the output of each steps in the forward method; elif 'param' then shows the learnable parameters
                              )

```
- Call model plotter to show the plot in 3D

```python
model_plotter()
```
<div align="center">
<img src="https://gitlab.com/ml-ppa-derivatives/torchrender3d/-/raw/main/graphics/simple_cnn_param.gif" alt= “cnn_output” width=30% height=30%>
</div>

- Visualize network parameter evolution during training
```python
#: call it with the 'update_with_timer' parameter and 'timer_interval' (if True) else can be updating by clicking 'u'
model_plotter(update_with_timer = True,timer_interval: int = 5000) 
```

- The plots during each update can be stored as tiff file format, later to visualize as an animation
```python
#: if make_animation==True, then instantiate the model_plotter with 'output_anim_folder' set to a valid path
model_plotter(update_with_timer = True,timer_interval: int = 5000,make_animation=True) 
```

### Plotting output from each layer
- Prepare test data.

```python
from torchvision import datasets, transforms

transform = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,)),  # Normalize grayscale images
    ]
)

test_dataset = datasets.MNIST(
    root="./data", train=False, download=True, transform=transform
)

test_data = np.array([test_dataset[i][0] for i in range(100)])
```

- Instantiating the model_plotter with the parameter plot_type='output'.

```python
model_plotter = PlotNetwork3D(
                              neural_network=model,
                              stored_network_params_path=stored_network_params_path, #: can be a random string, but required a valid path for updating feature
                              normalize=False,
                              plot_type='output', # if 'output' then plots the output of each steps in the forward method; elif 'param' then shows the learnable parameters
                              test_data=test_data,
                              )

```
- run the call method to plot

```python
model_plotter() 
```

<div align="center">
<img src="https://gitlab.com/ml-ppa-derivatives/torchrender3d/-/raw/main/graphics/output_plot.png" alt= “cnn_output” width=30% height=30%>
</div>

- Box-widget feature can be used to expand cnn layers for more detailed view from each kernels. This can be acheived by instantiating the model_plotter with "add_box_widget=True" as shown below:

```python
model_plotter = PlotNetwork3D(
                              neural_network=model,
                              stored_network_params_path=stored_network_params_path, #: can be a random string, but required a valid path for updating feature
                              normalize=False,
                              plot_type='output', # if 'output' then plots the output of each steps in the forward method; elif 'param' then shows the learnable parameters
                              test_data=test_data,
                              add_box_widget=True,
                              box_render_range=[-100, 100, -100, 100, -5, 5], #: Size of the box-widget 
                              box_step=5 #: To traverse the box_widget with step by scrolling
                              )
model_plotter() #: Can be updated manually with press of 'u' while setting the parameter 'update_with_timer=False' 
                #: or automatically 'update_with_timer=True'. time interval can be set with 'timer_interval=3000' for 3 secs

```

<div align="center">
<img src="https://gitlab.com/ml-ppa-derivatives/torchrender3d/-/raw/main/graphics/output_frames_with_box_widget.gif" alt= “cnn_output” width=30% height=30%>
</div>

- animations can me made by setting 'make_animation=True' as shown below:

```python
model_plotter(update_with_timer=True, timer_interval=1000,make_animation=True) 
```


<div align="center">
<img src="https://gitlab.com/ml-ppa-derivatives/torchrender3d/-/raw/main/graphics/cnn_output.gif" alt= “cnn_output” width=30% height=30%>
</div>


## Authors and acknowledgment
**Authors**: Tanumoy Saha   
**Acknowledgment**: We would like to acknowledge PUNCH4NFDI and InterTwin consortium for the funding and the members of TA5 for their valuable support 

## Project 
Initial stage (Beta) of development (Version: 0.1). 
