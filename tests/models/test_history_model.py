""" module to test history model """
# models
from api.models import History

# validators
from api.middlewares.base_validator import ValidationError

# mocks
from tests.mocks.history import histories


class TestHistoryModel:
    """Test history model
    """

    def test_new_history(self, init_db, new_user):
        """Test creating new history

        Args:
            init_db (SQLAlchemy): fixture to initialize the test database
        """
        new_user.save()

        new_history = History(**histories[0])
        assert new_history == new_history.save()

    def test_count(self):
        """Test history was saved in the db
        """

        assert History.count() == 1

    def test_query(self):
        """Test quering histories
        """

        history_query = History.query_()

        assert history_query.count() == 1
        assert isinstance(history_query.all(), list)

    def test_history_representation(self):
        """Should compute the official string representation of history
        """
        history = History(**histories[-1])
        assert repr(history) == f'<History on {history.resource_type}>'

    def test_history_child_relationships(self):
        """Test child relationships of history
        """

        history = History.query_().first()
        assert history.get_child_relationships() is None
