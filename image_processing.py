import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import matplotlib
import matplotlib.pyplot as plt
import math
from collections import Counter
from pylab import savefig
import cv2
import os
import random
from skimage import io
matplotlib.use("Agg")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_IMG_FOLDER = os.path.join(APP_ROOT, "static/img")


def grayscale():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r = img_arr[:, :, 0]
    g = img_arr[:, :, 1]
    b = img_arr[:, :, 2]
    new_arr = r.astype(int) + g.astype(int) + b.astype(int)
    new_arr = (new_arr/3).astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")
    new_img.save("static/img/img_grayscale.jpg")


def is_grey_scale(img_path):
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    for i in range(w):
        for j in range(h):
            r, g, b = im.getpixel((i, j))
            if r != g != b:
                return False
    return True


def zoomin():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    img_arr = np.asarray(img)
    new_size = ((img_arr.shape[0] * 2),
                (img_arr.shape[1] * 2), img_arr.shape[2])
    new_arr = np.full(new_size, 255)
    new_arr.setflags(write=1)

    r = img_arr[:, :, 0]
    g = img_arr[:, :, 1]
    b = img_arr[:, :, 2]

    new_r = []
    new_g = []
    new_b = []

    for row in range(len(r)):
        temp_r = []
        temp_g = []
        temp_b = []
        for i in r[row]:
            temp_r.extend([i, i])
        for j in g[row]:
            temp_g.extend([j, j])
        for k in b[row]:
            temp_b.extend([k, k])
        for _ in (0, 1):
            new_r.append(temp_r)
            new_g.append(temp_g)
            new_b.append(temp_b)

    for i in range(len(new_arr)):
        for j in range(len(new_arr[i])):
            new_arr[i, j, 0] = new_r[i][j]
            new_arr[i, j, 1] = new_g[i][j]
            new_arr[i, j, 2] = new_b[i][j]

    new_arr = new_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def zoomout():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    x, y = img.size
    new_arr = Image.new("RGB", (int(x / 2), int(y / 2)))
    r = [0, 0, 0, 0]
    g = [0, 0, 0, 0]
    b = [0, 0, 0, 0]

    for i in range(0, int(x/2)):
        for j in range(0, int(y/2)):
            r[0], g[0], b[0] = img.getpixel((2 * i, 2 * j))
            r[1], g[1], b[1] = img.getpixel((2 * i + 1, 2 * j))
            r[2], g[2], b[2] = img.getpixel((2 * i, 2 * j + 1))
            r[3], g[3], b[3] = img.getpixel((2 * i + 1, 2 * j + 1))
            new_arr.putpixel((int(i), int(j)), (int((r[0] + r[1] + r[2] + r[3]) / 4), int(
                (g[0] + g[1] + g[2] + g[3]) / 4), int((b[0] + b[1] + b[2] + b[3]) / 4)))
    new_arr = np.uint8(new_arr)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_left():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((0, 0), (0, 50)), 'constant')[:, 50:]
    g = np.pad(g, ((0, 0), (0, 50)), 'constant')[:, 50:]
    b = np.pad(b, ((0, 0), (0, 50)), 'constant')[:, 50:]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_right():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((0, 0), (50, 0)), 'constant')[:, :-50]
    g = np.pad(g, ((0, 0), (50, 0)), 'constant')[:, :-50]
    b = np.pad(b, ((0, 0), (50, 0)), 'constant')[:, :-50]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_up():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((0, 50), (0, 0)), 'constant')[50:, :]
    g = np.pad(g, ((0, 50), (0, 0)), 'constant')[50:, :]
    b = np.pad(b, ((0, 50), (0, 0)), 'constant')[50:, :]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_down():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((50, 0), (0, 0)), 'constant')[0:-50, :]
    g = np.pad(g, ((50, 0), (0, 0)), 'constant')[0:-50, :]
    b = np.pad(b, ((50, 0), (0, 0)), 'constant')[0:-50, :]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_addition():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img).astype('uint16')
    img_arr = img_arr+100
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_substraction():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img).astype('int16')
    img_arr = img_arr-100
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_multiplication():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    img_arr = img_arr*1.25
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_division():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    img_arr = img_arr/1.25
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def convolution(img, kernel):
    h_img, w_img, _ = img.shape
    out = np.zeros((h_img-2, w_img-2), dtype=np.float_)
    new_img = np.zeros((h_img-2, w_img-2, 3))
    if np.array_equal((img[:, :, 1], img[:, :, 0]), img[:, :, 2]) == True:
        array = img[:, :, 0]
        for h in range(h_img-2):
            for w in range(w_img-2):
                S = np.multiply(array[h:h+3, w:w+3], kernel)
                out[h, w] = np.sum(S)
        out_ = np.clip(out, 0, 255)
        for channel in range(3):
            new_img[:, :, channel] = out_
    else:
        for channel in range(3):
            array = img[:, :, channel]
            for h in range(h_img-2):
                for w in range(w_img-2):
                    S = np.multiply(array[h:h+3, w:w+3], kernel)
                    out[h, w] = np.sum(S)
            out_ = np.clip(out, 0, 255)
            new_img[:, :, channel] = out_
    new_img = np.uint8(new_img)
    return new_img


def edge_detection():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype= np.int_)
    kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def blur():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.int_)
    kernel = np.array(
        [[0.0625, 0.125, 0.0625], [0.125, 0.25, 0.125], [0.0625, 0.125, 0.0625]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def sharpening():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.int_)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def save_histogram(data, color):
    fig, ax = plt.subplots()
    ax.bar(list(data.keys()), data.values(), color=color)
    plt.savefig(f'static/img/{color}_histogram.jpg', dpi=300)
    plt.clf()
    plt.close()

# histogram ke-2
def histogram_rgb():
    img_path = "static/img/img_now.jpg"
    img = Image.open(img_path)
    img_arr = np.asarray(img)

    if len(img_arr.shape) == 2:
        # Grayscale image
        data_g = Counter(img_arr.flatten())
        matplotlib.use('Agg')
        plt.bar(list(data_g.keys()), data_g.values(), color='black')
        plt.savefig(f'static/img/grey_histogram.jpg', dpi=300)
        plt.clf()
    elif len(img_arr.shape) == 3 and img_arr.shape[2] == 3:
        # Color image (assuming it's RGB)
        r = img_arr[:, :, 0].flatten()
        g = img_arr[:, :, 1].flatten()
        b = img_arr[:, :, 2].flatten()

        data_r = Counter(r)
        data_g = Counter(g)
        data_b = Counter(b)

        data_rgb = [data_r, data_g, data_b]
        warna = ['red', 'green', 'blue']
        data_hist = list(zip(warna, data_rgb))
        matplotlib.use('Agg')
        for data in data_hist:
            plt.bar(list(data[1].keys()), data[1].values(), color=f'{data[0]}')
            plt.savefig(f'static/img/{data[0]}_histogram.jpg', dpi=300)
            plt.clf()
    else:
#         Handle other cases or raise an error if the image format is not supported
        raise ValueError("Unsupported image format")
    

def df(img):  # to make a histogram (count distribution frequency)
    values = [0]*256
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            values[img[i, j]] += 1
    return values


def cdf(hist):  # cumulative distribution frequency
    cdf = [0] * len(hist)  # len(hist) is 256
    cdf[0] = hist[0]
    for i in range(1, len(hist)):
        cdf[i] = cdf[i-1]+hist[i]
    # Now we normalize the histogram
    # What your function h was doing before
    cdf = [ele*255/cdf[-1] for ele in cdf]
    return cdf


def histogram_equalizer():
    img = cv2.imread('static\img\img_now.jpg', 0)
    my_cdf = cdf(df(img))
    # use linear interpolation of cdf to find new pixel values. Scipy alternative exists
    image_equalized = np.interp(img, range(0, 256), my_cdf)
    cv2.imwrite('static/img/img_now.jpg', image_equalized)

def threshold(lower_thres, upper_thres):
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    condition = np.logical_and(np.greater_equal(img_arr, lower_thres),
                               np.less_equal(img_arr, upper_thres))
    print(lower_thres, upper_thres)
    
    # Membuat salinan array yang dapat diubah
    img_arr_copy = img_arr.copy()
    img_arr_copy[condition] = 255
    
    new_img = Image.fromarray(img_arr_copy)
    new_img.save("static/img/img_now.jpg")

def crop_image(img, splits):
    # Get image dimensions
    width, height = img.size
    # Calculate the width and height of each cropped image
    new_width = width // splits
    new_height = height // splits

    # Create a list to store the cropped images
    cropped_images = []

    # Loop through the rows and columns, crop the image, and save each cropped image
    for i in range(splits):
        for j in range(splits):
            left = j * new_width
            upper = i * new_height
            right = (j + 1) * new_width
            lower = (i + 1) * new_height
            cropped = img.crop((left, upper, right, lower))

            # Generate a unique filename for each cropped image
            filename = f"cropped_{i}_{j}.jpg"
            file_path = os.path.join(STATIC_IMG_FOLDER, filename)

            # Save the cropped image to the static/img folder
            cropped.save(file_path)

            # Store the URL of the saved image
            img_url = f"/static/img/{filename}"
            cropped_images.append(img_url)

    return cropped_images

    width, height = new_img.size
    print(f"Width: {width} pixels")
    print(f"Height: {height} pixels")

def random_image(img, splits):
    # Get image dimensions
    width, height = img.size
    # Calculate the width and height of each cropped image
    new_width = width // splits
    new_height = height // splits

    # Create a list to store the cropped images
    cropped_images = []

    # Loop through the rows and columns, crop the image, and save each cropped image
    for i in range(splits):
        for j in range(splits):
            left = j * new_width
            upper = i * new_height
            right = (j + 1) * new_width
            lower = (i + 1) * new_height
            cropped = img.crop((left, upper, right, lower))

            # Generate a unique filename for each cropped image
            filename = f"cropped_{i}_{j}.jpg"
            file_path = os.path.join(STATIC_IMG_FOLDER, filename)

            # Save the cropped image to the static/img folder
            cropped.save(file_path)

            # Store the URL of the saved image
            img_url = f"/static/img/{filename}"
            cropped_images.append(img_url)

    cropped_images = random.sample(cropped_images, len(cropped_images))
    return cropped_images

def get_image_dimensions(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return width, height
    except Exception as e:
        return None

def get_image_rgb(image_path):
    try:
        with Image.open(image_path) as img:
            rgb_values = list(img.getdata())
            return rgb_values
    except Exception as e:
        return None

def identity():
    img = cv2.imread("static/img/img_normal.jpg")

    kernel = np.array([[0, 0, 0],
                   [0, 1, 0],
                   [0, 0, 0]])
    
    identity = cv2.filter2D(img, -1, kernel)

    cv2.imwrite("static/img/img_now.jpg", identity)

def blur_2(kernel):
    img = cv2.imread("static/img/img_normal.jpg")

    kernel = np.ones((kernel, kernel), np.float32) / (kernel*kernel)

    blur = cv2.filter2D(src=img, ddepth=-1, kernel= kernel)

    cv2.imwrite("static/img/img_now.jpg", blur)

def cv_blur(kernel):
    img = cv2.imread("static/img/img_normal.jpg")

    cv_blur = cv2.blur(src=img, ksize=(kernel, kernel))

    cv2.imwrite("static/img/img_now.jpg", cv_blur)

def gaussian_blur(kernel):
    img = cv2.imread("static/img/img_normal.jpg")

    cv_gaussianblur = cv2.GaussianBlur(src=img,ksize=(kernel,kernel),sigmaX=0)

    cv2.imwrite("static/img/img_now.jpg", cv_gaussianblur)

def median_blur(kernel):
    img = cv2.imread("static/img/img_normal.jpg")

    median_blur = cv2.medianBlur(src=img,ksize=kernel)

    cv2.imwrite("static/img/img_now.jpg", median_blur)

def sharp():
    img = cv2.imread("static/img/img_normal.jpg")

    kernel = np.array([[0, -1, 0],
                    [-1, 5, -1],
                    [0, -1, 0]])

    sharp = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)

    cv2.imwrite("static/img/img_now.jpg", sharp)

def bilateral():
    img = cv2.imread("static/img/img_normal.jpg")   

    bf = cv2.bilateralFilter(src=img,d=9,sigmaColor=75,sigmaSpace=75)

    cv2.imwrite("static/img/img_now.jpg", bf)

def zero_padding():
    img = cv2.imread("static/img/img_normal.jpg")

    image = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)

    cv2.imwrite("static/img/img_now.jpg", image)

def lowFilterPass(kernel):
    img = cv2.imread("static/img/img_normal.jpg")
    # create the low pass filter
    lowFilter = np.ones((kernel,kernel),np.float32)/(kernel*kernel)
    # apply the low pass filter to the image
    lowFilterImage = cv2.filter2D(img,-1,lowFilter)

    cv2.imwrite("static/img/img_now.jpg", lowFilterImage)

def highFilterPass():
    img = cv2.imread("static/img/img_normal.jpg")
    # create the high pass filter
    highFilter = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
    # apply the high pass filter to the image
    highFilterImage = cv2.filter2D(img,-1,highFilter)

    cv2.imwrite("static/img/img_now.jpg", highFilterImage)

def bandFilterPass():
    img = cv2.imread("static/img/img_normal.jpg")
    # create the band pass filter
    bandFilter = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]])
    # apply the band pass filter to the image
    bandFilterImage = cv2.filter2D(img,-1,bandFilter)

    cv2.imwrite("static/img/img_now.jpg", bandFilterImage)


