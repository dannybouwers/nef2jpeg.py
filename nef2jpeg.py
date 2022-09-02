import ying
import rawpy
import cv2
from time import process_time
import os

class Photo:
    def __init__(self, name):
        self.rawfile = name
        self.filename = os.path.splitext(os.path.basename(name))[0]
        self.dirname = os.path.dirname(name)

    def __repr__(self):
        return f'File {self.filename} in dir {self.dirname}'

    def open(self):
        with rawpy.imread(self.rawfile) as raw:
            rgbImg = raw.postprocess(use_camera_wb=True)
        
        self.image=cv2.cvtColor(rgbImg, cv2.COLOR_RGB2BGR)
        
        return self

    def resize(self, boxSize):
        f1 = boxSize / self.image.shape[1]
        f2 = boxSize / self.image.shape[0]
        f = min(f1, f2)  # resizing factor
        dim = (int(self.image.shape[1] * f), int(self.image.shape[0] * f))
        self.image = cv2.resize(self.image, dim)

        return self

    def enhance(self):
        self.image = ying.nice(self.image)

        return self

    def save (self, target=None):
        if target is None:
            self.target = os.path.join(self.dirname, f'{self.filename}.jpg' )

        cv2.imwrite(f'{self.target}', self.image)

# copy exif
# get date
# set overwrite

def main():
    tic = process_time()

    p = Photo('samples/_DSC0870.NEF')
    p.open().resize(1920).enhance().save()
    print(p)
    del p

    toc = process_time()
    print('Duur: ', toc-tic, ' sec')

if __name__ == '__main__':
    main()