from PIL import Image, ImageEnhance

# read the image


def scan(filename):
    im = Image.open("static/uploads/{}".format(filename))

    # image brightness enhancer
    enhancer = ImageEnhance.Brightness(im)

    factor = 2  # brightens the image
    im_output = enhancer.enhance(factor)
    im_output = im_output.rotate(270)
    im_output.save('static/uploads/brightened-image.png')
