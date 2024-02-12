def get_floor_and_seat_no(hod_desk_ref_no):
    """ Gets the floor and seat number from hot desk ref number
    Args:
        hod_desk_ref_no (str): the hot desk ref number
    Returns:
        tuple: floor and seat number
    """
    ref_no_data = hod_desk_ref_no.split()
    floor = int(''.join(filter(str.isdigit, ref_no_data[0])))
    seat_no = int(ref_no_data[1])
    return floor, seat_no
