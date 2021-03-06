import os

import numpy as np
import torch as th
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm

EPSILON = 1e-10


def GetData(is_train=True):
    print("Loading data")
    if(is_train):
        dataset_x = np.load(os.path.join("Data", "Train_x.npy"))
        dataset_y = np.load(os.path.join("Data", "Train_y.npy"))
        dataset_x_ = np.load(os.path.join("Data", "Test_x.npy"))
        dataset_y_ = np.load(os.path.join("Data", "Test_y.npy"))
        dataset_x = np.concatenate([dataset_x, dataset_x_])
        dataset_y = np.concatenate([dataset_y, dataset_y_])
    else:
        # dataset_x = np.load(os.path.join("Data", "Validation_x.npy"))
        # dataset_y = np.load(os.path.join("Data", "Validation_y.npy"))
        dataset_x = np.load(os.path.join("Data", "Test_x.npy"))
        dataset_y = np.load(os.path.join("Data", "Test_y.npy"))

    print("Data loaded")

    return dataset_x, dataset_y


def IsBlank(images):
    result = np.zeros(images.shape[0])
    for i in tqdm(range(images.shape[0])):
        image = images[i, ...]
        max_pixel = np.max(image)
        if(max_pixel != 0):
            result[i] = 1
    return result.astype(np.float32)


def MinMaxNormalize(images):
    print("Normalizing")
    dataset = []
    for i in tqdm(range(images.shape[0])):
        image = images[i, ...]
        max_pixel = np.max(image)
        if(max_pixel != 0):
            image = image / max_pixel
        else:
            image = image.astype(np.float32)
        dataset.append(image)
    return np.array(dataset).astype(np.float32)


def GetDataloader(dataset_x, dataset_y, batch_size):
    print(dataset_x.shape)
    dataset = TensorDataset(
        th.from_numpy(np.expand_dims(dataset_x, axis=1)),
        th.from_numpy(dataset_y)
    )

    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True
    )

    return dataloader


def CodeLogger(files):
    full_code = ""
    for file in files:
        with open(file, "r") as file_io:
            full_code += "####################$$$$$$$$$$$$$$$$$$$$ " + \
                file + " $$$$$$$$$$$$$$$$$$$$####################\n"
            code = file_io.readlines()
            for line in code:
                if("api_key" not in line):
                    full_code += line
        if(file != files[-1]):
            full_code += "\n\n"

    return full_code
