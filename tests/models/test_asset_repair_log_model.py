from api.models import AssetRepairLog


class TestAssetRepairLogModel:
    def test_create_asset_repair_log_succeeds(self, init_db,
                                              new_asset_repair_log, new_asset):
        """Should create a new asset repair log
        Args:
            new_asset (object): Fixture to create a new asset
            new_asset_repair_log (object): Fixture to create a new asset repair log
        """
        new_asset.update_(tag='AND/VET/JK34')
        new_asset.save()
        assert new_asset_repair_log == new_asset_repair_log.save()

    def test_update_asset_repair_log_succeeds(self, init_db, new_user, request_ctx,
                                              mock_request_two_obj_decoded_token,
                                              new_asset_repair_log, new_asset):
        """
            Should test update asset repair log
        Args:
        init_db (func): Fixture to initialize the test database
        new_user (object): Fixture to create a new user
        new_asset_repair_log (object): Fixture to create a new asset repair log
        new_asset (object): Fixture to create a new asset
        """
        new_asset.update_(tag='AND/VET/234')
        new_asset.save()
        new_asset_repair_log.update_(issue_description="Need a new Mac", )
        assert new_asset_repair_log.issue_description == "Need a new Mac"

    def test_update_repair_log_succeeds_test_policy(
        self, init_db, new_user, new_user_two, mock_request_two_obj_decoded_token, request_ctx, asset_repair_log_two, new_asset):
        """
            Should test update asset repair log
        Args:
        init_db (func): Fixture to initialize the test database
        new_user (object): Fixture to create a new user
        asset_repair_log_two (object): Fixture to create a new asset repair log
        new_asset (object): Fixture to create a new asset
        """
        new_asset.update_(tag='AND/VET/934')
        new_asset.save()
        repair = AssetRepairLog(**asset_repair_log_two)
        repair.save()
        repair.update_(created_by='-akfbkadfadfh')
        log = repair.query_().filter_by(id=repair.id).first()
        log.update_(issue_description="Need a new Mac", )
        assert log.issue_description == "Need a new Mac"

    def test_get_an_asset_repair_log_succeeds(self, init_db, new_asset,
                                              new_asset_repair_log):
        """Should retrieve an asset repair log

        Args:
            init_db (func): Fixture to initialize the test database
            new_asset (object): Fixture to create a new asset
            new_asset_repair_log (object): Fixture to create a new asset repair log
        """
        new_asset.update_(tag='AND/VET/J34')
        new_asset.save()
        new_asset_repair_log.save()
        assert AssetRepairLog.get(
            new_asset_repair_log.id) == new_asset_repair_log
        assert new_asset_repair_log.issue_description == 'Need Screen fixed'

    def test_search_asset_repair_log_succeeds(self, new_asset_repair_log):
        """Should retrieve an asset repair log that matches provided string

        Args:
            new_asset_repair_log (object): Fixture to create a new asset repair log
        """
        repair_log_query = new_asset_repair_log.query_()
        search_result = repair_log_query.search('screen').all()
        assert len(search_result) >= 1
        assert search_result[0].issue_description == 'Need Screen fixed'

    def test_get_child_relationships_(self, init_db, new_asset_repair_log):
        """Get resources relating to the AssetRepairLog model

        Args:

            init_db (func): Fixture to initialize the test database
            new_asset_repair_log (object): Fixture to create a new asset repair log
        """

        assert new_asset_repair_log.get_child_relationships() is None

    def test_asset_repair_log_representation(self, init_db,
                                             new_asset_repair_log_three):
        """Should compute the string representation

        Args:
            init_db (func): Fixture to initialize the test database
            asset_repair_log_two (object): Fixture to create a asset repair log for an asset in flow
        """

        assert repr(
            new_asset_repair_log_three
        ) == f'<AssetRepairLog {new_asset_repair_log_three.id} {new_asset_repair_log_three.issue_description}>'

    def test_delete_asset_repair_log_succeeds(
            self, new_asset_repair_log_three, request_ctx,
            mock_request_two_obj_decoded_token, new_user):
        """Should delete a asset repair log

        Args:
            new_asset_repair_log_three (object): Fixture to create a new asset repair log
            request_ctx (object): request client context
            mock_request_two_obj_decoded_token (object): Mock decoded_token from request client context
        """
        new_user.save()
        new_asset_repair_log_three.delete()
        assert AssetRepairLog.get(new_asset_repair_log_three.id) is None
