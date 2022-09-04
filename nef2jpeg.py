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
            return f'{self.rawfile} saved as {self.target}'
        else:
            return f'{self.rawfile} skipped. {self.target} already exists'

# copy exif
# get date

def main():
    tic = process_time()

    folder ='./samples'

    for root, directories, files in os.walk(folder):
        for f in files:
            if f.lower().endswith('.nef'):
                print(Photo(os.path.join(root, f)).resize(1920).enhance().save())
    
    toc = process_time()
    print(f'Processed in {toc-tic:.4f} sec')

if __name__ == '__main__':
    main()