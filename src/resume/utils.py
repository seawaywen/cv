# -*- coding: utf-8 -*-

import random

import os
import uuid
from tempfile import NamedTemporaryFile
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
import io

from PIL import ImageOps, ImageChops
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile


def get_file_data(file_obj):
    # reset file obj to read the whole contents
    file_obj.seek(0)
    data = file_obj.read()
    # reset file obj so it can be read again
    file_obj.seek(0)
    return data


def convert_to_png_uploaded_file(uploaded_img, size=None):
    """Convert to PNG format from other fie format"""
    if uploaded_img.name is not None and uploaded_img.name.strip() != '':
        file_name, file_ext = os.path.splitext(uploaded_img.name)
        with NamedTemporaryFile(mode='rb', suffix='.png') as tmp_png_file:
            with NamedTemporaryFile(mode='wb+', suffix=file_ext) as tmp_file:
                for chunk in uploaded_img.chunks():
                    tmp_file.write(chunk)
                tmp_file.flush()
                _image = Image.open(tmp_file.name)
                _image.save(tmp_png_file.name, 'png')
            return SimpleUploadedFile(file_name + '.png', tmp_png_file.read())
    return None
        

def create_thumbnail(uploaded_img):
    if not uploaded_img:
        return

    THUMBNAIL_SIZE = (160, 120)
    BOX_SIZE = (150, 110)
    PIL_TYPE = 'png'
    
    image = Image.open(io.BytesIO(uploaded_img.read()))
    #image = Image.open(uploaded_img.name)

    image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
    image_size = image.size

    #thumb = image.crop((0, 0, THUMBNAIL_SIZE[0], THUMBNAIL_SIZE[1]))
    #offset_x = max((THUMBNAIL_SIZE[0] - image_size[0]) / 2, 0)
    #offset_y = max((THUMBNAIL_SIZE[1] - image_size[1]) / 2, 0)

    #thumb = ImageChops.offset(thumb, offset_x, offset_y)
    thumb = ImageOps.fit(image=image, size=image.size, method=Image.ANTIALIAS, 
        bleed=0.01, centering=(0.5, 0.5))

    background = Image.new("RGB", THUMBNAIL_SIZE, (230, 230, 230, 0))

    box = Image.new("RGB", BOX_SIZE, (255, 255, 255, 0))
    
    box.paste(thumb, ((BOX_SIZE[0] - image.size[0]) // 2, 
        (BOX_SIZE[1] - image.size[1]) // 2))
    background.paste(box, ((THUMBNAIL_SIZE[0] - box.size[0]) // 2,
        (THUMBNAIL_SIZE[1] - box.size[1]) // 2))
    
    tmp_handle = io.BytesIO()
    background.save(tmp_handle, PIL_TYPE, quality=95)
    #thumb.save(tmp_handle, PIL_TYPE, quality=95)
    tmp_handle.seek(0)

    suf = SimpleUploadedFile(os.path.split(uploaded_img.name)[-1],
                             tmp_handle.read())

    return suf


def generate_uuid():
    uid_hostId_with_time = uuid.uuid1()
    uid_with_random_seed = uuid.uuid1(random.randint(0, 10000))
    random_uid = uuid.uuid4()
    uuid_list = [str(uid_hostId_with_time), str(uid_with_random_seed), str(random_uid)]
    tmp = ''.join(uuid_list)

    # Make UUI using SHA-1 Hash of namespace UUID and created UUID
    _uuid = uuid.uuid5(uuid.NAMESPACE_DNS, tmp)
    return str(_uuid)
