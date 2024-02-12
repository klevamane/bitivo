# Schemas
from api.schemas.schedule import ScheduleSchema


class TestScheduleSchema:
    """Test schedule schema"""

    def test_schedule_schema_with_valid_data_succeeds(self, init_db,
                                                      new_schedule):
        """Tests schedule schema works when valid data is supplied to the schema

         Args:
            init_db(SQLAlchemy): Fixture to initialize the test database actions
            new_schedule (object): Fixture to create a new schedule
        """
        schedule = new_schedule.save()
        schedule_data = ScheduleSchema().dump(schedule).data

        assert schedule.status.value == schedule_data['status']
        assert schedule.id == schedule_data['id']
