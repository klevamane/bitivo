from bot.utilities.ref_no_info import get_floor_and_seat_no

class TestRefNo:
    """Tests for the ref number helper"""
    
    def test_get_floor_and_seat_no(self):
        """ tests that the method returns floor and seat no
        self (Instance): instance of this class
        """
        
        ref_no = '1M 121'
        floor, seat_no = get_floor_and_seat_no(ref_no)
        assert floor == 1
        assert seat_no == 121
