from PIL import Image, ImageOps
import uuid
import io
import requests

import boto3


def create_filename():
    return str(uuid.uuid4()) + '.jpg'


class ImageService:
    def init_app(self, app):
        self.s3_bucket = app.config.get('S3_BUCKET')

    def crop_and_save_pic(self, pic):
        image = Image.open(pic.stream)
        image = ImageOps.fit(image, (500, 500))
        return self._save_pic_to_s3(image)

    def save_pic(self, pic):
        image = Image.open(pic.stream)
        return self._save_pic_to_s3(image)


    def _save_pic_to_s3(self, pillow_image):
        io_buffer = io.BytesIO()
        pillow_image.save(io_buffer, format='jpeg')
        resized_byte_arr = io_buffer.getvalue()
        filename = create_filename()
        self.s3_upload(resized_byte_arr, filename, 'image/jpeg')
        return filename

    def s3_upload(self, file_content, file_key, content_type):
        session = boto3.session.Session(region_name='eu-central-1')
        s3_client = session.client('s3', config=boto3.session.Config(signature_version='s3v4'))
        s3_client.put_object(Body=file_content,
                             Bucket=self.s3_bucket,
                             Key=file_key,
                             ContentType=content_type,
                             CacheControl="private, max-age=604800",
                             )

    def delete_file(self, file_key):
        session = boto3.session.Session(region_name='eu-central-1')
        s3_client = session.client('s3', config=boto3.session.Config(signature_version='s3v4'))
        s3_client.delete_object(Bucket=self.s3_bucket,
                                Key=file_key)

    def get_file(self, file_key):
        session = boto3.session.Session(region_name='eu-central-1')
        s3_client = session.client('s3', config=boto3.session.Config(signature_version='s3v4'))
        s3_response = s3_client.generate_presigned_url('get_object',
                                                       Params={'Bucket': self.s3_bucket, 'Key': file_key},
                                                       ExpiresIn=3600)
        print(s3_response)
        response = requests.get(s3_response)
        image_bytes = io.BytesIO(response.content)

        return image_bytes


image_service = ImageService()
