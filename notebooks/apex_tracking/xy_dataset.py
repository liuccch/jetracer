import torch
import os
import glob
import uuid
import PIL.Image
import torch.utils.data
import subprocess
import cv2
import numpy as np


class XYDataset(torch.utils.data.Dataset):
    def __init__(self, directory, transform=None, random_hflip=False):
        super(XYDataset, self).__init__()
        self.directory = directory
        self.transform = transform
        self.refresh()
        self.random_hflip = random_hflip
        
    def __len__(self):
        return len(self.annotations)
    
    def __getitem__(self, idx):
        
        ann = self.annotations[idx]
        image = cv2.imread(ann['image_path'], cv2.IMREAD_COLOR)
        image = PIL.Image.fromarray(image)
        width = image.width
        height = image.height
        if self.transform is not None:
            image = self.transform(image)
        
        x = 2.0 * (ann['x'] / width - 0.5) # -1 left, +1 right
        y = 2.0 * (ann['y'] / height - 0.5) # -1 top, +1 bottom
        
        if self.random_hflip and float(np.random.random(1)) > 0.5:
            image = torch.from_numpy(image.numpy()[..., ::-1].copy())
            x = -x
            
        return image, ann['category_index'], torch.Tensor([x, y])
    
    def _parse(self, path):
        basename = os.path.basename(path)
        items = basename.split('_')
        x = items[0]
        y = items[1]
        return int(x), int(y)
        
    def refresh(self):
        
        self.annotations = []
        for category in self.categories:
            category_index = self.categories.index(category)
            for image_path in glob.glob(os.path.join(self.directory, category, '*.jpg')):
                x, y = self._parse(image_path)
                self.annotations += [{
                    'image_path': image_path,
                    'x': x,
                    'y': y
                }]
        
    def save_entry(self, image, x, y):
        image_filename = '%d_%d_' + str(uuid.uuid1()) + '.jpg'
        with open()
        category_dir = os.path.join(self.directory, category)
        if not os.path.exists(category_dir):
            subprocess.call(['mkdir', '-p', category_dir])
            
        filename = '%d_%d_%s.jpg' % (x, y, str(uuid.uuid1()))
        
        image_path = os.path.join(category_dir, filename)
        cv2.imwrite(image_path, image)
        self.refresh()
        
    def get_count(self, category):
        i = 0
        for a in self.annotations:
            if a['category'] == category:
                i += 1
        return i