import numpy as np
from PIL import Image
import image_processing
import os
from flask import Flask, render_template, request, make_response
from datetime import datetime
from functools import wraps, update_wrapper
from shutil import copyfile

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)


@app.route("/index")
@app.route("/")
@nocache
def index():
    return render_template("home.html", file_path="img/image_here.jpg")


@app.route("/about")
@nocache
def about():
    return render_template('about.html')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/upload", methods=["POST"])
@nocache
def upload():
    target = os.path.join(APP_ROOT, "static/img")
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    if not os.path.isdir(target):
        if os.name == 'nt':
            os.makedirs(target)
        else:
            os.mkdir(target)
    for file in request.files.getlist("file"):
        file.save("static/img/img_now.jpg")
    copyfile("static/img/img_now.jpg", "static/img/img_normal.jpg")
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)

@app.route("/uploadquiz", methods=["POST"])
@nocache
def uploadQuiz():
    target = os.path.join(APP_ROOT, "static/img")
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    if not os.path.isdir(target):
        if os.name == 'nt':
            os.makedirs(target)
        else:
            os.mkdir(target)
    for file in request.files.getlist("file"):
        file.save("static/img/img_now.jpg")
    copyfile("static/img/img_now.jpg", "static/img/img_normal.jpg")
    img = Image.open("static/img/img_now.jpg")
    width, height = img.size
    return render_template("uploaded.html", file_path="img/img_now.jpg", width = width, height = height)

@app.route("/normal", methods=["POST"])
@nocache
def normal():
    copyfile("static/img/img_normal.jpg", "static/img/img_now.jpg")
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


@app.route("/grayscale", methods=["POST"])
@nocache
def grayscale():
    image_processing.grayscale()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


@app.route("/zoomin", methods=["POST"])
@nocache
def zoomin():
    image_processing.zoomin()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


@app.route("/zoomout", methods=["POST"])
@nocache
def zoomout():
    image_processing.zoomout()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


@app.route("/move_left", methods=["POST"])
@nocache
def move_left():
    image_processing.move_left()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


@app.route("/move_right", methods=["POST"])
@nocache
def move_right():
    image_processing.move_right()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


@app.route("/move_up", methods=["POST"])
@nocache
def move_up():
    image_processing.move_up()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


@app.route("/move_down", methods=["POST"])
@nocache
def move_down():
    image_processing.move_down()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


@app.route("/brightness_addition", methods=["POST"])
@nocache
def brightness_addition():
    image_processing.brightness_addition()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


@app.route("/brightness_substraction", methods=["POST"])
@nocache
def brightness_substraction():
    image_processing.brightness_substraction()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


@app.route("/brightness_multiplication", methods=["POST"])
@nocache
def brightness_multiplication():
    image_processing.brightness_multiplication()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


@app.route("/brightness_division", methods=["POST"])
@nocache
def brightness_division():
    image_processing.brightness_division()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


@app.route("/histogram_equalizer", methods=["POST"])
@nocache
def histogram_equalizer():
    image_processing.histogram_equalizer()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


@app.route("/edge_detection", methods=["POST"])
@nocache
def edge_detection():
    image_processing.edge_detection()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


@app.route("/blur", methods=["POST"])
@nocache
def blur():
    image_processing.blur()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


@app.route("/sharpening", methods=["POST"])
@nocache
def sharpening():
    image_processing.sharpening()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


@app.route("/histogram_rgb", methods=["POST"])
@nocache
def histogram_rgb():
    image_processing.histogram_rgb()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    if image_processing.is_grey_scale("static/img/img_now.jpg"):
        return render_template("uploaded.html", file_paths=["img/grey_histogram.jpg"], image_dim = image_dimension)
    else:
        return render_template("uploaded.html", file_paths=["img/red_histogram.jpg", "img/green_histogram.jpg", "img/blue_histogram.jpg"], image_dim = image_dimension)


@app.route("/thresholding", methods=["POST"])
@nocache
def thresholding():
    lower_thres = int(request.form['lower_thres'])
    upper_thres = int(request.form['upper_thres'])
    image_processing.threshold(lower_thres, upper_thres)
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)

@app.route("/crop-image", methods=["POST"])
@nocache
def show_crop_image():
    if request.method == "POST":
        # Get the uploaded image
        image = "static/img/img_now.jpg"

        # Get the number of splits from the form
        splits = int(request.form["crop_piece"])

        # Open the image using Pillow
        img = Image.open(image)

        image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')

        # Save the cropped images
        cropped_images = image_processing.crop_image(img, splits)

        return render_template(
            "uploaded.html",
            file_path="img/img_now.jpg",
            cropped_images=cropped_images,
            image_dim = image_dimension,
            splits=splits,
        )

    return render_template("uploaded.html")


@app.route("/random-image", methods=["POST"])
@nocache
def show_random_image():
    if request.method == "POST":
        # Get the uploaded image
        image = "static/img/img_now.jpg"

        # Get the number of splits from the form
        splits = int(request.form["crop_piece"])

        # Open the image using Pillow
        img = Image.open(image)

        image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')

        # Save the cropped images
        cropped_images = image_processing.random_image(img, splits)

        return render_template(
            "uploaded.html",
            file_path="img/img_now.jpg",
            cropped_images=cropped_images,
            splits=splits,
            image_dim = image_dimension,
        )

    return render_template("uploaded.html")

@app.route("/rgb_value", methods=["POST"])
@nocache
def rgb_value():
    target = os.path.join(APP_ROOT, "static/img")
    image_dimension = image_processing.get_image_dimensions("static/img/img_now.jpg")
    rgb_values = image_processing.get_image_rgb("static/img/img_now.jpg")
    if not os.path.isdir(target):
        if os.name == 'nt':
            os.makedirs(target)
        else:
            os.mkdir(target)
    for file in request.files.getlist("file"):
        file.save("static/img/img_now.jpg")
    copyfile("static/img/img_now.jpg", "static/img/img_normal.jpg")
    return render_template("rgb_value.html", file_path="img/img_now.jpg", image_dim = image_dimension, img_rgb_val=rgb_values)


@app.route("/identity", methods=["POST"])
@nocache
def identity():
    image_processing.identity()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)

@app.route("/blur_2", methods=["POST"])
@nocache
def blur_2():
    kernel = int(request.form['kernel'])
    image_processing.blur_2(kernel)
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)

@app.route("/cv_blur", methods=["POST"])
@nocache
def cv_blur():
    kernel = int(request.form['kernel'])
    image_processing.cv_blur(kernel)
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)

@app.route("/gaussian_blur", methods=["POST"])
@nocache
def gaussian_blur():
    kernel = int(request.form['kernel'])
    image_processing.gaussian_blur(kernel)
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)

@app.route("/median_blur", methods=["POST"])
@nocache
def median_blur():
    kernel = int(request.form['kernel'])
    image_processing.median_blur(kernel)
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)

@app.route("/sharp", methods=["POST"])
@nocache
def sharp():
    image_processing.sharp()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)

@app.route("/bilateral", methods=["POST"])
@nocache
def bilateral():
    image_processing.bilateral()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)

@app.route("/zero_padding", methods=["POST"])
@nocache
def zero_padding():
    image_processing.zero_padding()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)

@app.route("/lowFilterPass", methods=["POST"])
@nocache
def lowFilterPass():
    kernel = int(request.form['kernel'])
    image_processing.lowFilterPass(kernel)
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)

@app.route("/highFilterPass", methods=["POST"])
@nocache
def highFilterPass():
    image_processing.highFilterPass()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)

@app.route("/bandFilterPass", methods=["POST"])
@nocache
def bandFilterPass():
    image_processing.bandFilterPass()
    image_dimension = image_processing.get_image_dimensions('static/img/img_now.jpg')
    return render_template("uploaded.html", file_path="img/img_now.jpg", image_dim = image_dimension)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

