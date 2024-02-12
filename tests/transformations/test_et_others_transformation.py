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
from api.tasks.transformer.asset_transformer import AssetRegisterTransformer
from tests.mocks.asset_migration import RAW_ET_OTHERS_DATA, CLEAN_ET_OTHERS_DATA

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1

# Model


class TestTransformation:
    def test_et_others_transformation(self, init_db):

        sheet = pe.Sheet(RAW_ET_OTHERS_DATA)
        new_book = AssetRegisterTransformer.transform_et_others(sheet, {})
        assert new_book == CLEAN_ET_OTHERS_DATA
