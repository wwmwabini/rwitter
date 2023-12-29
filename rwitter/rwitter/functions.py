import secrets, os

def random_photo_name(self):
    _, photo_extension = os.path.splitext(self.photo.path)
    photo_filename = secrets.token_hex(12) + photo_extension
    print("Random photo name", photo_filename)

    return photo_filename


def random_image_name(self):
    _, photo_extension = os.path.splitext(self.image.path)
    photo_filename = secrets.token_hex(12) + photo_extension
    print("Random photo name", photo_filename)

    return photo_filename