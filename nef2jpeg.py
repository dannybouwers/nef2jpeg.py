import ying
import rawpy
import cv2
from time import process_time, sleep
from datetime import datetime
import os
from exiftool import ExifToolHelper
import subprocess
import signal
import argparse

class Photo:
    def __init__(self, name):
        self.rawfile = name
        self.filename = os.path.splitext(os.path.basename(name))[0]
        self.dirname = os.path.dirname(name)
        self.target = os.path.join(self.dirname, f'{self.filename}.jpg')
        self.doOverwrite = False
        self.doEnhance = False
        self.boxSize = None

    def __str__(self) -> str:
        m = f'File {self.rawfile} with name {self.filename} in dir {self.dirname} will be opened'
        m = f'{m}\nThe photo will be resized to fit a {self.boxSize}x{self.boxSize}px box.' if self.boxSize else m
        m = f'{m}\nThe photo will be enhanced using Ying New Image Contrast Enhancement' if self.doEnhance else m
        m = f'{m}\nIt will be saved as {self.target}'

        if self.doOverwrite:
            m = f'{m}\nThe file will be overwritten if it already exists'
        else:
            m = f'{m}\nIf the file already exists, processing will be omitted and the file will not be overwritten'

        return m

    def __repr__(self) -> str:
        m = f'Photo("{self.rawfile}")'
        m = f'{m}.resize({self.boxSize})' if self.boxSize else m
        m = f'{m}.enhance()' if self.doEnhance else m
        m = f'{m}.overwrite()' if self.doOverwrite else m
        return m

    def resize(self, boxSize) -> 'Photo':
        self.boxSize = boxSize
        return self

    def __resize(self):
        f1 = self.boxSize / self.image.shape[1]
        f2 = self.boxSize / self.image.shape[0]
        f = min(f1, f2)  # resizing factor
        dim = (int(self.image.shape[1] * f), int(self.image.shape[0] * f))
        self.image = cv2.resize(self.image, dim)

        return self

    def enhance(self) -> 'Photo':
        self.doEnhance = True
        return self

    def __enhance(self):
        self.image = ying.nice(self.image)
        return self

    def overwrite(self) -> 'Photo':
        self.doOverwrite = True
        return self

    def checkExists(self) -> bool:
        return os.path.exists(self.target)

    def getExifTag(self, tag='File:FileName'):
        with ExifToolHelper() as et:
            t = et.get_tags(self.rawfile, tag)
            return t[0][tag]

    def prefixDateTime(self) -> 'Photo':
        t = self.getExifTag('EXIF:DateTimeOriginal')
        dt = datetime.strptime(t, '%Y:%m:%d %H:%M:%S')
        prefix = dt.strftime('%Y%m%d_%H%M%S')
        self.target = os.path.join(self.dirname, f'{prefix}{self.filename}.jpg')
        return self

    def copyExif(self):
        result = subprocess.run(['exiftool', '-quiet', '-overwrite_original', '-TagsFromFile', self.rawfile, '--Orientation', self.target], check=True)
        return result.returncode

    def open(self):
        with rawpy.imread(self.rawfile) as raw:
            rgbImg = raw.postprocess(use_camera_wb=True)
        
        self.image=cv2.cvtColor(rgbImg, cv2.COLOR_RGB2BGR)
        
        if self.boxSize:
            self.__resize()

        if self.doEnhance:
            self.__enhance()

        return self.image

    def save (self, target=None) -> str:
        if target is not None:
            self.target = target

        if not self.checkExists() or self.doOverwrite:
            self.open()
            cv2.imwrite(f'{self.target}', self.image)
            self.copyExif()
            return f'{self.rawfile} saved as {self.target}'
        else:
            return f'{self.rawfile} skipped. {self.target} already exists'

run = True

def signalHandler(signal, frame):
    global run
    print("Save photo's and stop watching...")
    run = False

def watch(folder, secs:float=10, size:int=None, prevFiles:set=None):
    if prevFiles is None:
        prevFiles=set()

    signal.signal(signal.SIGINT, signalHandler)
    while run:
        currFiles = set()
        for root, directories, files in os.walk(folder):
            for f in files:
                if f.lower().endswith('.nef'):
                    currFiles.add(os.path.join(root, f))

        for p in currFiles.difference(prevFiles):
            nicePhoto = Photo(p).enhance().prefixDateTime()

            if size:
                nicePhoto = nicePhoto.resize(size)

            print(nicePhoto.save())
        
        sleep(secs)
        watch(folder, secs, size, currFiles)

def main():
    epilog="""The folder and subfolder will be watched.
    Auto enhancement is performed using Ying et al's A New Image Contrast Enhancement Algorithm Using Exposure Fusion Framework.
    All options can be replaced with an environment variable with the same name. If both are set, the environment variable is used."""
    parser = argparse.ArgumentParser(description='Watch a folder for .NEF files, auto enhance them and convert them to .jpg.', epilog=epilog)
    parser.add_argument('-f', '--folder', default='./photos', help='Folder to watch for .NEF files (default .photos)')
    parser.add_argument('-s', '--size', type=int, help="Size of a square (in pixels) to fit the output photo's in (optional)")
    parser.add_argument('-w', '--wait', type=int, default=10, help='Wait time between folder scans (in seconds; default 10)')
    args = parser.parse_args()

    folder = os.environ.get('FOLDER') if os.environ.get('FOLDER') else args.folder
    size = os.environ.get('SIZE') if os.environ.get('SIZE') else args.size
    wait = os.environ.get('WAIT') if os.environ.get('WAIT') else args.wait
    
    tic = process_time()

    print(f'Start watching {folder}')
    watch(folder=folder, secs=wait, size=size)
    
    toc = process_time()
    print(f'Watched {folder} for {toc-tic:.4f} seconds')

if __name__ == '__main__':
    main()