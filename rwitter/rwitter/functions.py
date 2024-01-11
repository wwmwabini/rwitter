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


def handle_uploaded_file(f):
    _, file_extension = os.path.splitext(f.name)
    random_media_name = 'feedback-' + secrets.token_hex(12) + file_extension
    print("Actual file name: ", f.name)
    with open('media/feedback_media/'+random_media_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return random_media_name