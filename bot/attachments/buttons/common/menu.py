cancel_button = {
    "name": "cancel",
    "type": "button",
    "value": "cancel",
    "text": "Cancel",
    "style": "danger"
}

cancel_request_button = [{
    "fallback":"",
    "callback_id":"some_id",
    "color":"#3AA3ES",
    "actions":[
        {
    "name": "cancel request",
    "type": "button",
    "value": "cancel",
    "text": "Cancel this hot desk",
    "style": "danger"
}
    ]
}]

approval_buttons = [{
    "text":
    "Kindly respond to this request.",
    "fallback":
    "",
    "callback_id":
    "decision_buttons",
    "color":
    "#3AA3E3",
    "actions": [{
        "name": "approve",
        "type": "button",
        "text": "Approve",
        "style": "primary",
        "value": "approved"
    },
                {
                    "name": "reject",
                    "type": "button",
                    "text": "Reject",
                    "style": "danger",
                    "value": "rejected"
                }]
}]

back_button = {
    "name": "back",
    "type": "button",
    "value": "back",
    "text": "< Back",
    "style": "grey"
}
back_button_action = {
    "fallback":
        "",
    "color":
        "#3AA3E3",
    "callback_id":
        "back_button",
     "actions": [back_button]
}


def get_floors_list(list_of_hot_desks):
    """method which prepares data to be displayed as available floors.
        Args:
           list_of_hot_desks: list of dict with the key as floor
           Returns: list of slack available floors attachments
    """
    floors = []
    list_of_hot_desks_copy = []
    for floors_desk in list_of_hot_desks:
        for floor, room in floors_desk.items():
            floor = f'{floor[0]}{floor[1:].lower()}'
            floors.append(floor)
            list_of_hot_desks_copy.append({floor: room})
    return [create_hot_desk_buttons('Choose a floor...', floors,
                                    None),  back_button_action], list_of_hot_desks_copy, floors


def get_hot_desk_list(dict_key, list_of_hot_desks, single_floor=False):
    """method which prepares data dynamically to be used to make attachments.
        Args:
           list_of_hot_desks: list of dict with the key as floor
           dictkey: key of the dictionary which is actually the floor clicked
        Returns: list of slack  attachments
    """

    hot_desk = []
    for floors_desk in list_of_hot_desks:
        desks = prepair_list_attachments(hot_desk, floors_desk, dict_key,
                                         single_floor)
    desks.append(back_button_action)
    return desks


def prepair_list_attachments(desk_container,
                             desk_list,
                             dictkey,
                             single_floor=False):
    """helper method which prepares data dynamically to be used to make attachments.
        Args:
           desk_container: list to hold the attachments created
           desk_list: dict which has key as floor and value as list of hot desk
           dictkey: key of the dictionary which is actually the floor clicked
        Returns: list of slack  attachments
    """
    if desk_list.get(dictkey):
        import re, math
        re.sub(' +', ' ', dictkey)

        limit = 5
        count = math.ceil(len(desk_list[dictkey]) / limit)

        create_attachments(desk_container, limit, desk_list, count, dictkey, single_floor)

    return desk_container


def create_hot_desk_buttons(floor, rooms, name):
    """method which  handles dynamic attachment creation.
        Args:
            floor: Name of the floor
            rooms: list of available hot desk
        Returns: dict of slack  attachments
    """
    actions = [{
            "type": "button",
            "text": value,
            "name": value if not name else name,
            "style": "primary",
            "value": value
        } for value in rooms]
    return {
        "text":
        floor,
        "fallback":
        "",
        'message_type':
        "main message",
        "callback_id":
        "floor_list",
        "color":
        "#3AA3E3",
        "actions": actions
    }


def create_attachments(*args):
    """helper method which creates attachments.
        Args:
           desk_container: list to hold the attachments created
           desk_list: (dict) which has key as floor and value as list of hot desk
           dictkey: key of the dictionary which is actually the floor clicked
           count: (int) total rows to be displayed on the view
           limit: (int) total number of hot desk to be displayed per row
           single_floor(bool)
        Returns: None
    """
    desk_container, limit, desk_list, count, dictkey, single_floor = args 
    for i in range(1, count + 1):

        current_slot, dictkey_ = set_current_slot_and_floor_description(i, limit, desk_list, dictkey, single_floor)

        desk_container.append(
            create_hot_desk_buttons(dictkey_, current_slot, 'hot desk'))


def set_current_slot_and_floor_description(*args):
    """helper method which creates attachments.
        Args:
           floor: (dict) to hold the attachments created
           desk_list: dict which has key as floor and value as list of hot desk
           single_floor (bool):
           index: (int) list index
           limit: (int) total number of hot desk to be displayed per row
        Returns: None
    """
    index, limit, desk_list, floor, single_floor = args
    if index == 1:
        current_slot = desk_list[floor][0:limit]
        dictkey_ = f'Choose a seat from the {floor}' if not single_floor else 'Choose from the available seats'

    else:
        current_slot = desk_list[floor][(limit * (index - 1)):(
            limit * index)]
        dictkey_ = ''
    return current_slot, dictkey_
