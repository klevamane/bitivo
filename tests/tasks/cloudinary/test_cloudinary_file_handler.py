""" Test creation and deletion of file from cloudinary """

import os

# Standard Mock library
from unittest.mock import Mock
from faker import Faker

# import cloudinary library
import cloudinary
import cloudinary.uploader

# Cloudinary task
from api.tasks.cloudinary.cloudinary_file_handler import FileHandler

FAKE = Faker()


class TestFileHandler():
    """Test the task for uploading and deleting file from cloudinary """

    def test_upload_file_to_cloudinary_succeeds(self):
        """ Test the method for uploading file to cloudinary """

    file = os.path.join(os.path.dirname(__file__), '/mock-image.png')

    cloudinary.uploader.upload = Mock(
        return_value={'url': 'http://someimage.com'})

    value = FileHandler.upload_file(file)

    assert cloudinary.uploader.upload.called
    assert value == {'url': 'http://someimage.com'}

    def test_delete_file_to_cloudinary_succeeds(self):
        """ Test the method for deleting file from cloudinary """

        # mocking cloudinary
        cloudinary.api.delete_resources = Mock()

        public_id = FAKE.random
        FileHandler.delete_file(public_id)

        # assertion
        assert cloudinary.api.delete_resources.called
