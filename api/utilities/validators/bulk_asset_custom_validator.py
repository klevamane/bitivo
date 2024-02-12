import datetime

from api.models import Attribute
from api.models.database import db
from api.utilities.enums import InputControlChoiceEnum
from api.utilities.messages.error_messages.serialization_error import error_dict as serial_dict


class ValidateAssetsCustomField:
    """Used to vaidate custom attributes"""

    def __init__(self, asset_category):
        """Use to get custom attributes when object is created
        Args:
            asset_category(string): asset category id
        """
        self.asset_category = asset_category
        self.custom_attributes = self.fetch_custom_attributes()

    def validate_text(self, text, choices):
        """Validate type text or text area of custom attributes
        Args:
            text(string): Text to be validated
            choices(string): Will be null since text have no choices
        Return:
            text(string): Validated text
        """
        return text

    def validate_check_box(self, text, choices):
        """Validate type checkbox of custom attributes
        Args:
            text(string): Text to be validated
            choices(string): Choices to be taken from
        Return:
            text(string): Validated text
        Raises:
            valueError: if text does not pass validation
        """
        user_choices = set(text.split(","))
        choices = set(choices.split(","))
        if user_choices.isdisjoint(choices):
            raise ValueError(serial_dict["not_choice"].format(text, choices))
        common_fields = user_choices.intersection(choices)
        return ",".join(list(common_fields))

    def validate_radio_button(self, text, choices):
        """Validate type radio button of custom attributes
        Args:
            text(string): Text to be validated
            choices(string): Choices to be taken from
        Return:
            text(string): Validated text
        Raises:
            valueError: if text does not pass validation
        """
        if text.strip() not in choices.split(","):
            raise ValueError(serial_dict["not_choice"].format(text, choices))
        return text

    def validate_date(self, date_value, choices):
        """Validate type date of custom attributes
        Args:
            date_value(string): Text to be validated
            choices(string): Choices to be taken from
        Return:
            text(string): Validated text
        Raises:
            valueError: if text does not pass validation
        """
        try:
            datetime.datetime.strptime(date_value, '%Y-%m-%d')
            return date_value
        except ValueError:
            raise ValueError(serial_dict["invalid_date"].format(date_value))

    def fetch_custom_attributes(self):
        """Used to query attributes related to current asset category
        Returns:
            A list of tuples containing attributes details
        """
        return db.session.query(
            Attribute.label, Attribute.is_required, Attribute._key,
            Attribute.input_control, Attribute.choices).filter_by(
                deleted=False, asset_category_id=self.asset_category).all()

    def validate_attributes(self, asset, schema_validated_assets):
        """Will be used to determine whether user passed custom attributes
         and pass them to validator
        Args:
            asset(dict): Current assets that is being validated
            schema_validated_assets(dict): Asset details validated by schema
        """
        validated_custom_fields = {}
        for attribute in self.custom_attributes:
            custom_field = asset.get(attribute[2])
            if custom_field:
                self.validate_custom_type(validated_custom_fields, attribute,
                                          schema_validated_assets,
                                          custom_field)

            elif attribute[1] is True:
                schema_validated_assets[1][attribute[2]] = \
                    [serial_dict["required_field"].format(attribute[0])]
        schema_validated_assets[0][
            "custom_attributes"] = validated_custom_fields

    def validate_custom_type(self, *args):
        """Will be used to map custom attributes to their validation according to type
        Args:
            args:
                validated_custom_fields(dict): A group of validated custom attributes
                attribute(tuple): Current attribute type details to be used in validation
                schema_validated_assets: Asset details validated by schema
                custom_field: "Custom attribute to be validated"
        """
        validated_custom_fields, attribute,schema_validated_assets, \
        custom_field = args
        validation_mapper = {
            InputControlChoiceEnum.TEXTAREA.value: self.validate_text,
            InputControlChoiceEnum.TEXT.value: self.validate_text,
            InputControlChoiceEnum.DROPDOWN.value: self.validate_radio_button,
            InputControlChoiceEnum.CHECKBOX.value: self.validate_check_box,
            InputControlChoiceEnum.RADIOBUTTON.value:
            self.validate_radio_button,
            InputControlChoiceEnum.DATE.value: self.validate_date,
        }
        try:
            validated_custom_fields[attribute[2]] = \
                validation_mapper.get(attribute[3].lower())(str(custom_field).strip(), attribute[4])
        except ValueError as e:
            schema_validated_assets[1][attribute[2]] = [e.args[0]]
