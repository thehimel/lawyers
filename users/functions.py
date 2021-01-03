import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def resize_image(form_data, height_limit=300, square=True):
    """
    Resize image to the given limit and crop from center if square is needed
    """

    # Opening the uploaded image
    img = Image.open(form_data.pro_pic)
    output = BytesIO()

    height = form_data.pro_pic.height
    width = form_data.pro_pic.width

    # If square output is needed, crop the image.
    if square:
        width_limit = height_limit

        # check which one is larger
        if width > height:
            # make square by cutting off equal amounts from left and right
            left = (width - height) / 2
            right = (width + height) / 2

            top = 0
            bottom = height

            img = img.crop((left, top, right, bottom))

        elif height > width:
            # make square by cutting off equal amounts from top and bottom
            left = 0
            right = width

            top = (height - width) / 2
            bottom = (height + width) / 2

            img = img.crop((left, top, right, bottom))

    # If square output is not needed, calculate the height keeping the ratio.
    else:
        width_limit = round((width / height) * height_limit)

    # Resize/modify the image
    if width > width_limit and height > height_limit:
        img = img.resize((width_limit, height_limit))

    # after modifications, save it to the output
    img.save(output, format='JPEG', quality=90)
    output.seek(0)

    # change the imagefield value to be the newley modifed image value
    form_data.pro_pic = InMemoryUploadedFile(
        output, 'ImageField', f"{form_data.pro_pic.name.split('.')[0]}.jpg",
        'image/jpeg', sys.getsizeof(output), None)
