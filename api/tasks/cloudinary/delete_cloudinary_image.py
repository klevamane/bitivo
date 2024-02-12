"""Delete image from cloudinary"""

from .cloudinary_file_handler import FileHandler


# Main
from main import celery_app

# Utilities
from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env

# App config
from config import AppConfig


class DeleteCloudinaryImage:
    """Executes deleting of image on cloudinary"""

    @staticmethod
    def delete_cloudinary_image_handler(public_id):
        """Handles the Removal of image from cloudinary
        When the resource is deleted, the deleted column will be True
        after the operation and then the request to delete on
        cloudinary will be performed

        Args:
            public_id (str): The public_id of the image to be deleted
        """

        delete_image = adapt_resource_to_env(
            DeleteCloudinaryImage.delete_cloudinary_image.delay)
        delete_image(public_id)

    @staticmethod
    @celery_app.task(name="delete_cloudinary_image")
    def delete_cloudinary_image(public_id):
        """ 
        This method request for deletion of a image in cloudinary

        Args:
            public_id (str): The public_id of the image to be deleted
        """
        FileHandler.delete_file(public_id)
