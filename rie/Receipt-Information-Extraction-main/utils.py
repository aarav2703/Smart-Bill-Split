import os
from time import time
import datetime
import numpy as np
from skimage import io
import cv2
import yaml
from functools import wraps
import requests


class Progress:
    """Progress bar"""

    def __init__(self, i_list):
        self.__list = list(i_list)
        self.total = len(self.__list)
        self.current = -1
        self.__bar_length = 0
        self.__begin_time = time()
        self.__start = 0
        self.__recently = []

    def __iter__(self):
        return self

    def __next__(self):
        self.__update()
        if self.current < self.total:
            return self.__list[self.current]
        raise StopIteration

    def __update_bar_length(self, bar):
        terminal_length = os.get_terminal_size()[0]
        external_bar_length = int(len(bar) - self.__bar_length)
        self.__bar_length = terminal_length - external_bar_length - 2

    def __per_sec(self):
        prev = time()
        time_diff = prev - self.__start
        if time_diff <= 0:  # Avoid division by zero or negative time differences
            return 0.1  # Assign a small positive value to prevent calculation errors
        ps = 1 / time_diff
        self.__recently.pop(0) if len(self.__recently) >= 100 else None
        self.__recently.append(ps) if ps <= 100 else None
        self.__start = prev
        return max(np.mean(self.__recently), 0.1)  # Ensure non-zero average

    def __time_left(self):
        ps = self.__per_sec()
        if ps == 0:  # Avoid division by zero
            return "Calculating..."
        sec_left = round((self.total - self.current) / ps)
        sec_left = min(sec_left, 999999999)  # Clamp to avoid OverflowError
        time_format = datetime.timedelta(seconds=sec_left)
        return time_format

    def __time_total(self):
        sec_total = round(time() - self.__begin_time)
        time_format = datetime.timedelta(seconds=sec_total)
        return time_format

    def __bar(self):
        percent = self.current / self.total
        completed = int(percent * self.__bar_length) * "█"
        padding = int(self.__bar_length - len(completed)) * "."
        return f"Progress: {self.current}/{self.total} |{completed}{padding}| {int(percent * 100)}% in {self.__time_left()} > {self.__time_total()}"

    def __update(self):
        """Finish current state and move to next state"""
        self.current += 1
        bar = self.__bar()
        ending = "\n" if self.current == self.total else "\r"
        self.__update_bar_length(bar)
        print(bar, end=ending)


def crop_background(image, grayscale=False):
    """Crop black background only"""
    if not type(image).__module__ == np.__name__:
        img_arr = io.imread(image, True)
    else:
        img_arr = image
    gray = img_arr[:, :, 0] if img_arr.ndim > 2 else img_arr
    _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    x, y, w, h = cv2.boundingRect(thresholded)
    output = (gray if grayscale else image)[y : y + h, x : x + w]
    return output


def load_config(config_name, args=None):
    """Load config file"""
    with open("config.yaml") as f:
        config = yaml.full_load(f)[config_name]
    if args is not None:
        for arg, value in args.__dict__.items():
            if value is not None:
                config[arg] = value
    return config


def measure(func):
    """Measure the runtime"""

    @wraps(func)
    def _time(*args, **kwargs):
        start = time()
        try:
            return func(*args, **kwargs)
        finally:
            end_ = time() - start
            print(f"Done {func.__name__} in {round(end_, 2)}s")

    return _time


def download_weight(model_name, url=False):
    models = {
        "rotate_180.pkl": "1laOUDHBEOtazXM20x2DCXIZ7zBH4uWWB",
        "craft_mlt_25k.pth": "1fBUOVdtv4r6UM4rOTjaZpamcs3UIwzj_",
        "craft_refiner_CTW1500.pth": "1QC0hXbyNX-yW69g42RR0ZB74L6jqdRDg",
    }
    if not url:
        url = f"https://drive.google.com/uc?export=download&id={models[model_name]}"
    else:
        url = model_name
        model_name = model_name.split("/")[-1]
    os.mkdir("weights") if not os.path.exists("weights") else None
    weight_path = f"weights/{model_name}"
    if os.path.exists(weight_path):
        return weight_path
    print(f"Weight '{model_name}' not found, requesting...", end="\r")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        weight_folder = "weights"
        os.mkdir(weight_folder) if not os.path.exists(weight_folder) else None
        weight_path = f"{weight_folder}/{model_name}"
        with open(weight_path, "wb") as f:
            print(f"Downloading weight into '{weight_path}'")
            for chunk in Progress(r.iter_content(chunk_size=1000)):
                f.write(chunk)
    return weight_path
