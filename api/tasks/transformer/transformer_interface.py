import abc
from io import BytesIO

import pyexcel as pe

class AssetTransformerInterface(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def transform(book, email):
        """Initiates transformation by calling transform_all

            Args:
                book (dict): a dictionary of 2 dimensional arrays as sheets
                email (str): email of the user that initiated the transformation
            Returns:
                None
        """

        pass

    @classmethod
    def transform_all(cls, book, scripts_mapper, email, book_name):
        """Transforms all the mapped sheets in the document

            Args:
                book (dict): a dictionary of 2 dimensional arrays as sheets
                scripts_mapper (dict): a dictionary of mapped sheets in a document
                email (str): email of the user that initiated the transformation
                book_name (String): A name of the document being transformed
            Returns:
                new_book_content (dict): a dictionary of 2 dimensional arrays
        """

        new_book_content = {}

        cls.run_scripts(scripts_mapper, book, new_book_content)  # updates new_book_content

        cls.send_email(new_book_content, book_name, email)

        return new_book_content


    @classmethod
    def generate_new_book(cls, data):
        """Creates a pyexcel book
        
            Args:
                data (dict): a dict of sheet names as keys
                and scripts as values

            Returns:
                pyexcel book
        """
        return pe.Book(data)
    
    @classmethod
    def run_scripts(cls, scripts_mapper, book, new_book_content):
        """Runs the script mapped to the sheet names in the scripts mapper
        
            Args:
                scripts_mapper (dict): a dict of sheet names as keys
                and scripts as values
                book (dict): a dictionary of 2 dimensional arrays as sheets
                new_book_content (dict): an empty dict that will be populated with 
                2 dimensional arrays of the transformed document

            Returns:
                None
        """

        for sheet_name in book.keys():
            script, sheet_data = scripts_mapper.get(sheet_name.lower()), book[sheet_name]
            sheet = pe.Sheet(sheet_data)
            sheet.name = sheet_name
            script(sheet, new_book_content) if script else '' # Abstract this logic
    
    @classmethod
    def clean_sheet_headers(cls, column_replacers):
        """Returns a function that cleans column headers
         Args:
          column_replacers (dict): Dict for column headers with old name
          as key and new name as value
         Returns:
          clean_header (func): Function that will work on each header
        """

        def clean_header(header):
            if header.strip() in column_replacers:
                return column_replacers.get(header.strip())
            return header

        return clean_header
    
    @classmethod
    def send_email(cls, book_content, doc_name, recipients):
        """Sends the tranformed document (xlsx) to the email address provided
        
            Args:
                scripts_mapper (dict): a dict of sheet names as keys
                and scripts as values
                book_content (dict): a dictionary of 2 dimensional arrays as sheets
                recipents (list): an list of email recipents

            Returns:
                None
        """

        from api.tasks.email_sender import Email
        from api.utilities.constants import XLSX
        book = cls.generate_new_book(book_content)
        stream = BytesIO()
        file_object = book.save_to_memory(XLSX, stream)
        body = f'Hi, please find the transformed verson of {doc_name} in the attachment'
        title = 'Transformed Sheets'
        Email.send_mail(title, [recipients], body, {'name': f'{doc_name}.{XLSX}', 'file': file_object})
