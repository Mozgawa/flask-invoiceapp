from PIL import Image, ImageEnhance


def scan(filename):
    path = "invoice_parser/static/uploads/"
    factor = 2
    angle = -90
    im = Image.open(f"{path}{filename}")
    enhancer = ImageEnhance.Brightness(im)
    im_output = enhancer.enhance(factor)
    im_output = im_output.rotate(angle, expand=True)
    im_output.save(f"{path}brightened-image.png")
