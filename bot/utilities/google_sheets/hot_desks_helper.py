def add_hot_desk_to_list(hot_desk, list_of_hot_desk):
    """  helper method that checks if hot_desk exists and appends in to the list of available hot desks 
    args:
        hot_desk(str): hot desk
        list_of_hot_desk(list): a list of hot desks.
    """
    if hot_desk:
        list_of_hot_desk.append(hot_desk)
