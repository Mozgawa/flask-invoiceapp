from PIL import Image, ImageEnhance


def scan(filename):
    im = Image.open("static/uploads/{}".format(filename))

    # image brightness enhancer
    enhancer = ImageEnhance.Brightness(im)
    factor = 2
    im_output = enhancer.enhance(factor)
    im_output = im_output.rotate(-90, expand=True)
    im_output.save('static/uploads/brightened-image.png')
