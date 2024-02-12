"""Tests for schedule model"""

from api.models import Schedule

from api.utilities.enums import ScheduleStatusEnum


class TestScheduleModel:
    """Test Schedule Model"""

    def test_create_new_schedule_succeeds(self, init_db, new_schedule):
        """Should create a new schedule

        Args:
            init_db (object): Fixture to initialize the test database operations.
            new_schedule (object): Fixture to create a new schedule
        """
        new_schedule.save()
        retrieved_value = Schedule.get(new_schedule.id)
        assert retrieved_value
        assert retrieved_value.id == new_schedule.id

    def test_create_new_schedule_with_attachments_succeeds(
            self, init_db, new_schedule):
        """Should create a new schedule
         Args:
            init_db (object): Fixture to initialize the test database operations.
            new_schedule (object): Fixture to create a new schedule
        """
        schedule_attchements = ['our attachemnts']
        new_schedule.attachments = schedule_attchements
        new_schedule.save()
        retrieved_value = Schedule.get(new_schedule.id)
        assert retrieved_value
        assert retrieved_value.id == new_schedule.id
        assert retrieved_value.attachments == schedule_attchements

    def test_update_schedule_succeeds(self, new_schedule, new_user_two):
        """Test that the update method updates the schedule

        Args:
            new_schedule (object): Fixture to create a new schedule
        """
        new_user_two.save()
        new_assignee_id = new_user_two.token_id
        new_schedule.update_(assignee_id=new_assignee_id)

        assert new_schedule.assignee_id == new_assignee_id

    def test_get_succeeds(self, new_schedule):
        """Test that the get method returns the schedule

        Args:
            new_schedule (object): Fixture to create a new schedule
        """
        new_schedule.save()
        assert Schedule.get(new_schedule.id) == new_schedule

    def test_query_succeeds(self, new_schedule):
        """Test that the query_ method returns a list of schedules

        Args:
            new_schedule (object): Fixture to create a new schedule
        """
        schedule_query = new_schedule.query_()
        assert isinstance(schedule_query.all(), list)

    def test_schedule_model_string_representation(self, new_schedule):
        """Should compute the string representation of a schedule

        Args:
            new_schedule (object): Fixture to create a new schedule
        """
        assert repr(
            new_schedule
        ) == f'<Schedule: schedule: {new_schedule.id} status: {new_schedule.status}>'

    def test_get_child_relationships(self, new_schedule):
        """Get resources relating to the model

        Args:
            new_schedule (object): Fixture to create a new schedule
        """

        assert new_schedule.get_child_relationships() is None

    def test_schedule_enum_class(self):
        """
        Check that the enum fields returned are valid
        """
        schedule_enums = ScheduleStatusEnum.get_all()
        assert 'pending' in schedule_enums
        assert 'done' in schedule_enums
