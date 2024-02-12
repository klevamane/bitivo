"""Test deleting cloudinary center image background task"""

import cloudinary

# Standard Mock library
from unittest.mock import Mock
from faker import Faker

# Cloudinary background task
from api.tasks.cloudinary.delete_cloudinary_image import DeleteCloudinaryImage

fake = Faker()

class TestDeleteCloudinaryImage:
    """Test the background task for deleting cloudinary image"""

    def test_delete_cloudinary_image_handler(self):
        """handles the deleting and calls the cloudinary image delete method
        """

        DeleteCloudinaryImage.delete_cloudinary_image.delay = Mock(
            side_effect=DeleteCloudinaryImage.delete_cloudinary_image)
        cloudinary.api.delete_resources = Mock()
        
        public_id = fake.random
        DeleteCloudinaryImage.delete_cloudinary_image_handler(public_id)

        assert  DeleteCloudinaryImage.delete_cloudinary_image.delay.called
        assert  cloudinary.api.delete_resources.called


    def test_delete_cloudinary_image_from_cloudinary(self):
        """Make a request to cloudinary to delete an image
        """
        cloudinary.api.delete_resources = Mock()

        public_id = fake.random
        DeleteCloudinaryImage.delete_cloudinary_image(public_id)

        assert  cloudinary.api.delete_resources.called
