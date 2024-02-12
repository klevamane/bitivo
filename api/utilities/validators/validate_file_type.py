from werkzeug.utils import secure_filename

from api.utilities.constants import ALLOWED_FILE_EXTENSIONS


def allowed_file(filename):
    """
    Method to validate file type input.
        Args:
        filename (string): name of file to be validated
        Returns:
        reponse (boolean): returns True or False
    """
    filtered_filename = secure_filename(filename)

    return '.' in filtered_filename and filtered_filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS
