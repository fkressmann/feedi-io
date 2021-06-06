from PIL import Image, ImageOps
import uuid


class ImageService:
    def init_app(self, app):
        self.app = app

    def crop_and_save_pic(self, pic):
        image = Image.open(pic.stream)
        resized = ImageOps.fit(image, (500, 500))

        path = self.app.config.get('PICTURE_PATH')
        filename = str(uuid.uuid4()) + '.jpg'

        resized.save(path + filename)

        return filename


image_service = ImageService()
