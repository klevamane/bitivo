SLACK_BOT_TOKEN = 'SLACK_BOT_TOKEN'
SLACK_CHANNEL = 'SLACK_CHANNEL'
WELCOME_MSG = 'Make a HotDesk Request:'
CANCEL_MSG = 'Thank you for using Activo Bot! We hope you\'ll come back soon :wave:'
CONNECTION_MSG = 'Connection timed out'
ACTIVO_BOT_ICON = 'https://res.cloudinary.com/andeladevs/image/upload/v1531392321/Logo.png'
DEFAULT = {
    'text':
    'Unfortunately, this feature is only available in Lagos and Nairobi :disappointed:'
}
HOST_DESK_SOURCE = 'HOST_DESK_SOURCE'
HOT_DESK = "HOT DESK"
SHEET_HOT_DESK = 'Hot Desk'
GOOGLE_SHEET_NOT_FOUND = 'Sorry, your request could not be completed, kindly contact the Activo admin through #ask-activo'
TIMEOUT = 'Whoops, there seems to be an error in connection, try again please.'
CENTERS = ['lagos']
CENTER_CHILDREN = ['et']
SOMETHING_WENT_WRONG = 'Whoops!, we did not get that, please try `/activo` again'
USER_NOT_FOUND = 'Sorry, your request could not be completed because your details could not be retreived, kindly contact the Activo admin through #ask-activo'
HOT_DESK_MSG = {
    'no_hot_desk':
    'Hi *@{}* \n You do not have any *pending* or *approved* hotdesk',
    'confirm_delete_hot_desk':
    'Hey *@{}*, Are you sure you want to *cancel* your hotdesk',
    'successfully_cancelled':
    'Hey *@{}* \n Your hot desk has been successfully cancelled',
    'not_work_hours':
    'Sorry *@{}*, you can only book a hot desk from *8:00 AM* to *6:00 PM*',
}
CANCEL_HOTDESK_TITLE = 'Reason for Cancelling'
CANCEL_HOTDESK = 'cancel hot desk'
REJECT = 'reject'
OPS_CANCEL_UPDATE = 'Hi *@{}*, the user *@{}* has cancelled his/her request for hot desk *@{}*'
HELP_MESSAGE = 'view available commands below: \n'
INVALID_COMMAND = '`{}` is not a valid command on activo \n View available commands below: \n'
PERMANENT_SEAT_MSG = 'you are not eligible to request for a hot desk because you have been assigned a permanent seat at *{}*. If you have a complaint, contact the Activo admin through `#ask-activo` channel'
ASSIGNED_HOTDESK_MSG = 'You already have *hot desk - {}* allocated to you for the day :slightly_smiling_face:'
PENDING_HOTDESK_MSG = 'You have a pending request for *hot desk - {}* :slightly_smiling_face:'
NO_CANCEL_REASON = 'Kindly start over and make sure to select a cancellation reason'
PREDEFINED_CANCEL_REASONS = ['changed my mind',
                             'leaving early', 'delayed approval', 'seat changed']
NOT_IMPLEMENTED_MSG = {
    'text': 'Sorry this feature has not been implemented yet. :disappointed:'}
