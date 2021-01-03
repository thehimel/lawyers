import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
from users.appvars import MAX_FILE_SIZE_IN_MB, APP_NAME


# Adding APP_NAME in the beginning, to distinguish projects in cloudinary
user_default_pro_pic = APP_NAME + '/defaults/img/user_pro_pic.jpg'


# file will be uploaded to MEDIA_ROOT/APP_NAME/user_<username>/<filename>
# When we use id here, during the creation of a user model, id becomes None.
def user_dir(instance, filename):
    return APP_NAME + f'/user_data/user_{instance.username}/{filename}'


# For lawyer profile, we get the user_id from instance.user.id
# file will be uploaded to MEDIA_ROOT/APP_NAME/user_<username>/<filename>
def user_dir_lawyer(instance, filename):
    return APP_NAME + f'/user_data/user_{instance.user.username}/{filename}'


def resize_image(form_data, field_name, height_limit=300, square=True):
    """
    Resize image to the given limit and crop from center if square is needed
    """

    # We get source = form_data.pro_pic. Here pro_pic is the field_name.
    # For different models, field_name will be different.
    # To make the function dynamic, we are getting the attribute in this way.
    # field_name is a string here.
    source = getattr(form_data, field_name)

    # Opening the uploaded image
    img = Image.open(source)
    output = BytesIO()

    height = source.height
    width = source.width

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

    # For the default file selection at the beginning,
    # it doesn't have content type. Easiest solution is
    # to check for the extension at the end.
    # Make sure the user_default_pro_pic is a JPG file.
    # content_type = 'image/jpeg', content_type = 'image/png'.
    if source.name.endswith(".jpg") or source.name.endswith(".jpeg"):
        content_type = 'image/jpeg'
    else:
        content_type = source.file.content_type

    # Fetching the part after the last slash.
    file_format = content_type.split("/")[-1]

    # after modifications, save it to the output
    # Here format can be, format='JPEG', format='PNG'
    img.save(output, format=file_format, quality=90)
    output.seek(0)

    # change the imagefield value to be the newley modifed image value
    compressed_source = InMemoryUploadedFile(
        output, 'ImageField', source.name,
        content_type, sys.getsizeof(output), None)

    # We can not update the attribute with equal sign.
    # We should set new value to the attribute with setattr().
    setattr(form_data, field_name, compressed_source)


def file_size(value):
    limit = MAX_FILE_SIZE_IN_MB * 1024 * 1024
    if value.size > limit:
        raise ValidationError(
            f'File too large. Size should not exceed {MAX_FILE_SIZE_IN_MB} MB. \
                Current size is {value.size/(1024*1024):.2f} MB.')


def content_type_test(value, content_types, msg):

    # Few other file type options
    # content_types = ['video/x-msvideo', 'application/pdf',
    #                  'video/mp4', 'audio/mpeg', ]

    # When we create the model, that time file field will be there.
    # When we update the model and don't upload any file, no file
    # file will exist. That time it will through error that content_type
    # not available. Thus, we need to check if the object has the attribute.
    # try-except doesn't work here.
    if hasattr(value.file, 'content_type'):
        if value.file.content_type not in content_types:
            raise ValidationError(msg)


def content_type_pdf(value):
    content_types = ['application/pdf']
    msg = 'Only PDF file is accepted.'
    content_type_test(value, content_types, msg)


def content_type_jpeg(value):
    content_types = ['image/jpeg']
    msg = 'Only JPG or JPEG file is accepted.'
    content_type_test(value, content_types, msg)
