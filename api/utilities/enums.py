"""Input control enums Module"""

from enum import Enum


class Priority(Enum):
    """Asset Category priority enum"""
    key = 'key'
    not_key = 'not key'


class InputControlChoiceEnum(Enum):
    """
    Input controls enums
    """

    TEXTAREA = "textarea"
    TEXT = "text"
    DROPDOWN = "dropdown"
    CHECKBOX = "checkbox"
    RADIOBUTTON = "radio button"
    DATE = "date"

    @classmethod
    def get_multichoice_fields(cls):
        return [cls.DROPDOWN.value, cls.CHECKBOX.value, cls.RADIOBUTTON.value]

    @classmethod
    def get_singlechoice_fields(cls):
        return [cls.TEXTAREA.value, cls.TEXT.value, cls.DATE.value]

    @classmethod
    def get_all_choices(cls):
        return cls.get_multichoice_fields() + cls.get_singlechoice_fields()


class AssigneeType(Enum):
    """
    Assignee type enums
    """
    user = 'user'
    space = 'space'
    store = 'store'


class ParentType(Enum):
    """
    Parent type enums
    """
    Request = 'Request'
    Schedule = 'Schedule'

    @classmethod
    def get_all(cls):
        """Gets all parent types
        Args:
            cls (ParentType): An instance of the ParentType object
        Returns:
            set: Collection of parent_types.
        """
        return {parent_type.value for parent_type in cls}


class AssetStatus(Enum):
    """
    Asset status enums
    """
    INVENTORY = 'inventory'
    ASSIGNED = 'assigned'
    AVAILABLE = 'available'
    FAIRLY_USED = 'fairly used'
    OK = 'ok'
    OK_IN_USE = 'ok-in use'
    FAULTY = 'faulty'
    FAULTY_IN_STORE = 'faulty-in store'
    OK_IN_STORE = 'ok-in store'
    WITH_IT = 'with it'
    STOLEN = 'stolen'
    IN_REPAIRS = 'in repairs'
    IN_USE = 'in - use'
    LOST = 'lost'
    DISPOSED_WITH_APPROVAL = 'disposed with approval'

    @classmethod
    def get_all(cls):
        """Gets all asset status
        Args:
            cls (AssetStatus): An instance of the AssetStatus object
        Returns:
            set: Collection of valid asset status
        """
        return {status.value for status in cls}

    @classmethod
    def get_ok_status(cls):
        return (cls.ASSIGNED.value, cls.AVAILABLE.value, cls.OK.value,
                cls.OK_IN_STORE.value, cls.OK_IN_USE.value)

    @classmethod
    def get_reconciliation_status(cls):
        return (cls.AVAILABLE.value, cls.OK_IN_STORE.value,
                cls.INVENTORY.value)


class RequestStatusEnum(str, Enum):
    open = 'open'
    in_progress = 'in progress'
    completed = 'completed'
    closed = 'closed'

    @classmethod
    def get_all(cls):
        """Gets all request statuses

        Args:
            cls (RequestStatus): An instance of the RequestStatus object

        Returns:
            set: Collection of valid request status
        """
        return {status.value for status in cls}


class FrequencyEnum(Enum):
    """
    Request status enums
    """
    no_repeat = 'no_repeat'
    daily = 'daily'
    weekly = 'weekly'
    weekday = 'weekday'
    custom = 'custom'

    @classmethod
    def get_all(cls):
        """Gets all frequency types

        Args:
            cls (FrequencyTypes): An instance of the FrequencyTypes object

        Returns:
            list: Collection of valid frequency types
        """
        return [frequency.value for frequency in cls]


class CustomFrequencyEnum(Enum):
    """
    Frequency status enum
    """
    daily = "daily"
    weekly = 'weekly'
    monthly = 'monthly'
    yearly = 'yearly'

    @classmethod
    def get_all(cls):
        """Gets all custom occurence statuses

        Args:
            cls (CustomFrequencyEnum): An instance of the ScheduleStatus object

        Returns:
            list: Collection of valid custom occurence status
        """
        return [customoccurence.value for customoccurence in cls]


def get_enum_fields(cls):
    """Gets all Status

    Args:
        cls (Status): An instance of the Status object

    Returns:
        list: Collection of valid status
    """
    return [data.value for data in cls]


class StatusEnum(Enum):
    """
    Status enum
    """
    enabled = 'enabled'
    disabled = 'disabled'

    @classmethod
    def get_all(cls):
        """Gets all Status

        Args:
            cls (Status): An instance of the Status object

        Returns:
            list: Collection of valid status
        """
        return [status.value for status in cls]


class ScheduleStatusEnum(Enum):
    """Schedule status Enum."""

    pending = 'pending'
    done = 'done'

    @classmethod
    def get_all(cls):
        """Gets all schedule statuses

        Args:
            cls (ScheduleStatus): An instance of the ScheduleStatus object

        Returns:
            list: Collection of valid schedule status
        """
        return [status.value for status in cls]


class HotDeskRequestStatusEnum(Enum):
    """ Hot desk status enum """

    pending = 'pending'
    approved = 'approved'
    rejected = 'rejected'
    cancelled = 'cancelled'


class HotDeskResponseStatusEnum(Enum):
    """ Hot desk response status enum """
    pending = 'pending'
    approved = 'approved'
    rejected = 'rejected'
    cancelled = 'cancelled'


class RepairLogStatusEnum(Enum):
    """ RepairLog status enum """
    open = 'open'
    closed = 'closed'


class AssetWarrantyStatusEnum(Enum):
    """ AssetWarranty status enum """
    active = 'active'
    expired = 'expired'


class HotDeskCancellationReasonEnum(Enum):
    """ Hot desk cancellation reason enum """
    changed_my_mind = 'changed my mind'
    delayed_approval = 'delayed approval'
    leaving_early = 'leaving early'
    seat_changed = 'seat changed'


class AssetSupportingDocumentTypeEnum(Enum):
    """ Asset Supporting document type enum """
    purchase_receipts = 'purchase receipts'
    repair_receipts = 'repair receipts'
