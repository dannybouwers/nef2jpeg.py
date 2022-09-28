# nef2jpeg.py
Watch a folder for .NEF files, auto enhance them and convert them to .jpg.

## Usage
nef2jpeg.py [-h] [-f FOLDER] [-o OUTPUTFOLDER] [-s SIZE] [-w WAIT] [--overwrite OVERWRITE] [--dateprefix] [--runonce]

## Options

| option | description |
| ------ | ----------- |
| -h, --help | show this help message and exit |
| -f FOLDER, --folder FOLDER | Folder to watch for .NEF files (default=./photos) |
| -o OUTPUTFOLDER, --outputfolder OUTPUTFOLDER | Subfolder of the location of a source file to output the the .jpg (optional) |
| -s SIZE, --size SIZE | Size of a square (in pixels) to fit the output photo's in (optional) |
| -w WAIT, --wait WAIT | Wait time between folder scans (in seconds; default=10) |
| --overwrite OVERWRITE | Set if jpegs will be overwritten. "first" will overwrite .jpg at first run, "always" will always overwrite, "skip" will skip photo if jpeg exists (default=skip) |
| --dateprefix | Add the date and time as prefix to the jpeg-filename (optional) |
| --runonce | Scan and convert one time. I.e. do not watch a folder (optional) |

## Epilog
The folder and subfolder will be watched.

Auto enhancement is performed using Ying et al's [A New Image Contrast Enhancement Algorithm Using Exposure Fusion Framework](https://github.com/AndyHuang1995/Image-Contrast-Enhancement).

All options can be replaced with an environment variable with the same name. If both are set, the environment variable is used.

Use Ctrl+c to gracefully quit watching