from api.models import AssetCategory
"""
Module of tests for user endpoints
"""
# System libraries
from unittest.mock import Mock
from io import BytesIO
# Third-party libraries
from flask import json
import pyexcel as pe
# Constants
from api.utilities.constants import CHARSET
from api.tasks.transformer.accessories_transformer import AccessoriesTransformer
from tests.mocks.asset_migration import RAW_TEST_DEVICES_DATA, CLEAN_TEST_DEVICES_DATA

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1

# Model


class TestTransformation:
    def test_test_devices_transformation(self, init_db):

        sheet = pe.Sheet(RAW_TEST_DEVICES_DATA)
        new_book = AccessoriesTransformer.transform_test_devices(sheet, {})
        assert new_book == CLEAN_TEST_DEVICES_DATA
