"""Module for remove_whitespace function test"""

from api.utilities.helpers.remove_whitespace import remove_whitespace


class TestRemoveWhitespace:
    """Class to hold test methods for remove_whitespace function"""

    def test_that_white_space_removal_succeeds(self):
        """Test method for that it does expected behaviour"""

        data = {
            "title": "   the     game is over   ",
        }

        remove_whitespace(data, 'title', data.get('title'))

        assert data["title"] == "the game is over"
