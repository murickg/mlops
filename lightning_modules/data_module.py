import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from torchvision.datasets import MNIST
from pytorch_lightning import LightningDataModule
from traceofmatrix import TraceOfMatrix
import numpy as np


class MNISTDataset(Dataset):
    def __init__(self, data_dir, train=True, transform=None, download=False):
        self.data = MNIST(root=data_dir, train=train, download=True)
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # Загружаем изображение и метку
        image, label = self.data[idx]
        if self.transform:
            image = self.transform(image)

        # Вычисляем след
        matrix_size = 10
        matrix_a = np.random.rand(matrix_size, matrix_size)
        list_a = matrix_a.tolist()
        trace = TraceOfMatrix.traceOfMatrix(list_a, matrix_size)

        return image, label


class MNISTDataModule(LightningDataModule):
    def __init__(self, data_dir, batch_size):
        super().__init__()
        self.val_dataset = None
        self.train_dataset = None
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.transform = transforms.Compose([
            transforms.ToTensor(),
        ])

    def setup(self, stage=None):
        self.train_dataset = MNISTDataset(self.data_dir, train=True, transform=self.transform, download=True)
        self.val_dataset = MNISTDataset(self.data_dir, train=False, transform=self.transform, download=True)

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size)
