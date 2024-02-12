"""
This module contains asset collectiion definitions for use by swagger UI
"""

from ..collections import api

asset_namespace = api.namespace(
    'assets',
    description='A collection of Asset related endpoints'
)

asset_categories_namespace = api.namespace(
    'asset categories',
    description=' A collection of asset category related endpoints',
    path='/asset-categories'
)

asset_subcategories_namespace = api.namespace(
    'asset subcategories',
    description=' A collection of asset subcategory related endpoints',
    path='/subcategories'
)

asset_insurance_namespace = api.namespace(
    'asset insurance',
    description='A collection of asset insurance related endpoints',
    path='/insurance')

asset_note_namespace = api.namespace(
    'asset notes',
    description='A collection of asset notes related endpoints',
    path='/notes')

asset_warranty_namespace = api.namespace(
    'asset warranty',
    description='A collection of asset warranty related endpoints',
    path='/warranty'
)

repair_logs_namespace = api.namespace(
    ' asset repair logs',
    description='A collection of repair logs related endpoints',
    path='/repair-logs'
)

supporting_document_namespace = api.namespace(
    'asset supporting document',
    description='A collection of asset supporting document related endpoints',
    path='/documents'
)
