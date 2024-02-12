""" Manage creation and deletion of files from cloudinary """

# import cloudinary library
import cloudinary
import cloudinary.uploader


# App config
from config import AppConfig

# update Appconfig with cloudinary credentials
cloudinary.config.update = ({
    'cloud_name': AppConfig.CLOUDINARY_CLOUD_NAME,
    'api_key': AppConfig.CLOUDINARY_API_KEY,
    'api_secret': AppConfig.CLOUDINARY_API_SECRET
})


class FileHandler():
    """Manage creation and deletion of file from cloudinary"""

    @staticmethod
    def upload_file(file):
        """Handles the upload of file to cloudinary

        Args:
            file (file type): The image to be uploaded to cloudinary
        """
        return cloudinary.uploader.upload(file)

    @staticmethod
    def delete_file(public_id):
        """Handles the deletion of file from cloudinary

        Args:
            public_id (str): The public_id of the image to be deleted
        """

        return cloudinary.api.delete_resources([public_id])
