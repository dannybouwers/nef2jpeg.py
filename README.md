# nef2jpeg.py
Watch a folder for .NEF files, auto enhance them and convert them to .jpg.

## Usage
nef2jpeg.py [-h] [-f FOLDER] [-s SIZE] [-w WAIT]

## Options

| option | description |
| ------ | ----------- |
| -h, --help | show this help message and exit |
| -f FOLDER, --folder FOLDER | Folder to watch for .NEF files (default .photos) |
| -s SIZE, --size SIZE | Size of a square (in pixels) to fit the output photo's in (optional) |
| -w WAIT, --wait WAIT | Wait time between folder scans (in seconds; default 10) |

## Epilog
The folder and subfolder will be watched.

Auto enhancement is performed using Ying et al's [A New Image Contrast Enhancement Algorithm Using Exposure Fusion Framework](https://github.com/AndyHuang1995/Image-Contrast-Enhancement).

All options can be replaced with an environment variable with the same name. If both are set, the environment variable is used.