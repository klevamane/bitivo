# Models
from api.models import Schedule

# Utilities
from api.utilities.helpers.seeders import clean_seed_data

# Seed data
from .seed_data import get_env_based_data

def seed_schedule(clean_data=False):
   """Populate the schedules table with seed data.

   Args:
       clean_data (bool): If False doesn't allow duplicate seed data
   """
   schedule = get_env_based_data('schedule')

   schedule = clean_seed_data('schedule', schedule) if not clean_data else schedule

   Schedule.bulk_create(schedule)
