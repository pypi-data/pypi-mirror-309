import sys
import platform
from skbuild import setup
from setuptools import setup, find_packages

os_system = platform.system().lower()
py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
arch = platform.machine()
if arch == "x86_64":
    arch_label = "amd64"
elif arch in ("ARM64", "AARCH64"):
    arch_label = "arm64"
else:
    arch_label = "unknown"

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

if os_system == "linux" and arch == 'ARM64':
    raise RuntimeError(f"Unsupported OS and chip comaptibility for vtk as: {os_system,arch} combination not available")


setup(
    name='torchrender3d',
    #version=f'0.0.7+{os_system}.{arch}',
    version='0.0.7',
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=['numpy==2.1.3', 'torch==2.5.1','torchvision==0.20.1', 'vtk==9.2.6', 'tqdm==4.66.6'],
    #install_requires=['numpy>=1.21.0', 'torch==2.4.1','torchvision>=0.16.0', 'vtk==9.3.1', 'tqdm==4.66.6'],
    author='Tanumoy Saha',
    author_email='sahat@htw-berlin.de',
    description='TorchRender3D is an advanced visualization tool designed for PyTorch developers and researchers to explore the internal structure of custom neural networks specifically CNNs. Leveraging the power of VTK (Visualization Toolkit) for 3D rendering, TorchRender3D enables real-time, interactive visualizations of neural network layers and outputs.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/ml-ppa-derivatives/torchrender3d',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
    ],
    python_requires='>=3.10'
)