from PIL import Image, ImageOps
import uuid
import os
import io
import requests

from werkzeug.datastructures import ContentSecurityPolicy
from werkzeug.wrappers import request

import boto3


class ImageService:
    def init_app(self, app):
        self.path_prefix = app.config.get('S3_BUCKET_PATH')
        self.s3_bucket = app.config.get('S3_BUCKET')

    def crop_and_save_pic(self, pic, content_type, crop):
        image = Image.open(pic.stream)
        image_format = image.format
        if crop: 
            image = ImageOps.fit(image, (500, 500))
        buf = io.BytesIO()
        print("CONTENT: " + content_type)
        image.save(buf, format=image_format)
        resized_byte_arr = buf.getvalue()

        s3_bucket_name = self.s3_bucket

        filename, full_path = self.create_filename()

        self.s3_upload(resized_byte_arr, s3_bucket_name, filename, content_type)

        return filename

    def create_filename(self):
        for i in range(10):
            filename = str(uuid.uuid4()) + '.jpg'
            full_path = self.path_prefix + filename
            if not os.path.isfile(full_path):
                return filename, full_path

        raise RecursionError("Too many attempts to create a filename")

    def s3_upload(self, inp_file_name, s3_bucket_name, inp_file_key, content_type):
        s3_client = boto3.client('s3')
        session = boto3.session.Session(region_name='eu-central-1')
        s3_client = session.client('s3', config= boto3.session.Config(signature_version='s3v4'))
        upload_file_response = s3_client.put_object(Body=inp_file_name,
                                             Bucket=s3_bucket_name,
                                             Key=inp_file_key,
                                             ContentType=content_type)

    def delete_image(self, filename):
        full_path = self.path_prefix + filename
        if os.path.isfile(full_path):
            os.remove(full_path)

    def s3_read_pic(self, s3_bucket_name, inp_file_key, expiry=3600):
        s3_client = boto3.client('s3')
        session = boto3.session.Session(region_name='eu-central-1')
        s3_client = session.client('s3', config= boto3.session.Config(signature_version='s3v4'))
        s3_response = s3_client.generate_presigned_url('get_object',
                                            Params={'Bucket': s3_bucket_name,'Key': inp_file_key},
                                            ExpiresIn=expiry)
        response = requests.get(s3_response)
        image_bytes = io.BytesIO(response.content)

        return image_bytes


image_service = ImageService()
