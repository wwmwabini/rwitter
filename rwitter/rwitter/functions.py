import secrets, os

def random_photo_name(self):
    _, photo_extension = os.path.splitext(self.photo.path)
    photo_filename = secrets.token_hex(12) + photo_extension
    print("Random photo name", photo_filename)

    return photo_filename


def random_image_name(self):
    _, photo_extension = os.path.splitext(self.image.path)
    photo_filename = secrets.token_hex(12) + photo_extension
    print("Random image name", photo_filename)

    return photo_filename


def handle_uploaded_file(file, location, prefix):
    _, file_extension = os.path.splitext(file.name)
    random_media_name = prefix + '-' + secrets.token_hex(12) + file_extension
    print("Actual file name: ", file.name)
    if not location.endswith('/'):
        location += '/'
    with open('media/'+location + random_media_name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return random_media_name