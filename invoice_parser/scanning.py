from PIL import Image, ImageEnhance


def scan(filename):
    factor = 2
    angle = -90
    im = Image.open("invoice_parser/static/uploads/{}".format(filename))
    enhancer = ImageEnhance.Brightness(im)
    im_output = enhancer.enhance(factor)
    im_output = im_output.rotate(angle, expand=True)
    im_output.save('invoice_parser/static/uploads/brightened-image.png')
