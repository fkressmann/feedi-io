from PIL import Image, ImageOps
import uuid
import os


class ImageService:
    def init_app(self, app):
        self.path_prefix = app.config.get('PICTURE_PATH')

    def crop_and_save_pic(self, pic):
        image = Image.open(pic.stream)
        resized = ImageOps.fit(image, (500, 500))

        filename, full_path = self.create_filename()
        resized.save(full_path)

        return filename

    def create_filename(self):
        for i in range(10):
            filename = str(uuid.uuid4()) + '.jpg'
            full_path = self.path_prefix + filename
            if not os.path.isfile(full_path):
                return filename, full_path

        raise RecursionError("Too many attempts to create a filename")

    def delete_image(self, filename):
        full_path = self.path_prefix + filename
        if os.path.isfile(full_path):
            os.remove(full_path)


image_service = ImageService()
