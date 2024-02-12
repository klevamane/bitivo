"""Test database schema migrations with Alembic"""
# System imports
import os
from subprocess import call

# Third party imports
import alembic.command
import alembic.config

alembic_cfg = alembic.config.Config("./migrations/alembic.ini")


class TestMigrations:
    def test_running_all_migrations_succeeds(self, set_up_db):
        """Should pass with valid migration files for upgrade and downgrade
        
        Args:
            set_up_db (func): sets up the test db
        """
        script_dir = alembic.script.ScriptDirectory.from_config(alembic_cfg)
        revisions = [
            sc.revision for sc in script_dir.walk_revisions('base', 'heads')
        ]
        revisions.reverse()
        for revision in revisions:
            alembic.command.upgrade(alembic_cfg, revision)
        revisions.reverse()
        for revision in revisions:
            alembic.command.downgrade(alembic_cfg, revision)

    def test_latest_migration_upgrade_downgrade_succeeds(self, set_up_db):
        """Should pass with valid last downgrade migration file
        
        Args:
            set_up_db (func): sets up the test db
        """
        alembic.command.upgrade(alembic_cfg, 'head')
        alembic.command.downgrade(alembic_cfg, 'base')

    def test_latest_migration_downgrade_and_upgrade_with_data_succeeds(
            self, set_up_db):
        """Should pass with valid migration files and valid seed data
        
        Args:
            set_up_db (func): sets up the test db
        """
        alembic.command.upgrade(alembic_cfg, 'head')
        call(["flask", "seed"])
        alembic.command.downgrade(alembic_cfg, 'base')

    def test_all_changes_to_model_have_migrations_files(self, set_up_db):
        """Should pass with no new migration files created
        
        Args:
            set_up_db (func): sets up the test db
        """
        current_head = self.get_current_head()
        alembic.command.upgrade(alembic_cfg, 'head')
        call(['flask', 'db', 'migrate'])
        alembic.command.upgrade(alembic_cfg, 'head')
        new_head = self.get_current_head()
        assert current_head == new_head

    def get_current_head(self):
        """Gets the current head of migrations 
        
        Returns:
            (str): string of the current head 
        """
        script_dir = alembic.script.ScriptDirectory.from_config(alembic_cfg)
        current_head = script_dir.get_heads()
        return current_head[0]
