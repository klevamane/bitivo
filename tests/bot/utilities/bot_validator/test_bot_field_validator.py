from bot.utilities.dialog_bot_validation.bot_fields_validators import cancel_hot_desk_dialog_validator
from bot.utilities.dialog_serialization_errors import BOT_DIALOG_ERROR


class TestHotDeskDialogValidator:
    """Test the hot desk dialog validations"""
    
    def test_cancel_hot_desk_dialog_validator_with_no_reason_fails(self):
        """
        Test the cancel hot desk dialog validator method with reason as false
        """
        reason = False
        errors = cancel_hot_desk_dialog_validator(reason)

        assert 'errors' in errors
        assert errors['errors'][0]['name'] == 'cancelled_reason'
        assert errors['errors'][0]['error'] == BOT_DIALOG_ERROR['not_empty']

    def test_cancel_hot_desk_dialog_validator_with_reason_of_only_space_fails(self):
        """
        Test the cancel hot desk dialog validator method
        """
        reason = '   '
        errors = cancel_hot_desk_dialog_validator(reason)

        assert 'errors' in errors
        assert errors['errors'][0]['name'] == 'cancelled_reason'
        assert errors['errors'][0]['error'] == BOT_DIALOG_ERROR['not_empty']
