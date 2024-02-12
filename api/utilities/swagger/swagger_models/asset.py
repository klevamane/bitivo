"""
Model Definition for asset collection
"""

from flask_restplus import fields

from ..collections.asset import (asset_namespace, asset_insurance_namespace,
                                 asset_note_namespace, asset_warranty_namespace,
                                 repair_logs_namespace, asset_categories_namespace)


# swagger model defining assets fields
asset_model = asset_namespace.model("asset_model", {
    'assetCategoryId': fields.String(
        required=True, description='Asset category ID'),
    'tag': fields.String(
        required=True, description='Asset tag'),
    'assigneeId': fields.String(
        required=True, description='space_id or token_id'),
    'assigneeType': fields.String(
        required=True, description='space or user'),
    'customAttributes': fields.Nested(asset_namespace.model(
        'custom_attributes_assets', {
            'deviceType': fields.String(
                description='The type of device',
                required=False,
            ),
            'color': fields.String(
                description='color of the device',
                required=False,
            ),
        })),
})


# swagger model that defines bulk asset fields
bulk_asset_model = asset_namespace.model("bulk_asset_model", {
    'assetCategoryId': fields.String(
        required=True, description='Asset category ID'),
    'assetCategoryName': fields.String(
        required=True, description='Asset category name'),
    'assets': fields.List(
        fields.Nested(asset_model)),
})


# swagger model that defines asset insurance fields
asset_insurance_model = asset_insurance_namespace.model("asset_insurance_model", {
    'company': fields.String(
        required=True, description='insurance company name'),
    'startDate': fields.String(
        required=True, description='start date of the insurance policy'),
    'endDate': fields.String(
        required=True, description='end date of the insurance policy'),
})


# swagger model that defines asset  note fields
asset_note_model = asset_note_namespace.model("asset_note_model", {
    'title': fields.String(
        required=True, description='title of the note'),
    'body': fields.String(
        required=True, description='body of the note'),
})


# swagger model that defines asset fields
asset_warranty_model = asset_warranty_namespace.model("asset_warranty_model", {
    'startDate': fields.String(
        required=True, description='start date of the  warranty'),
    'endDate': fields.String(
        required=True, description='expiry date of the warranty'),
    'status': fields.String(
        required=True,
        description='status o the warranty. Either expired or active'),
})

# swagger model that defines asset repair log fields
asset_repair_log_model = repair_logs_namespace.model("asset_repair_log_model", {
    'complainantId': fields.String(
        required=True, description='id of user who made the complaint'),
    'assetId': fields.String(
        required=True, description='asset id'),
    'assigneeId': fields.String(
        required=True, description='id of user assigned to repair asset'),
    'issueDescription': fields.String(
        required=True, description='description of the issue'),
    'expectedReturnDate': fields.String(
        required=True, description='date when asset should be returned'),
    'dateReported': fields.String(
        required=True, description='date when asset defect was reported'),
    'defectType': fields.String(
        required=True, description='type of asset defect'),
    'repairer': fields.String(
        required=True, description='person/entity to carry out repairs'),
})

# swagger model that defines asset category fields
asset_categories_model = asset_categories_namespace.model(
    "asset_categories_model", {
        'name': fields.String(
            required=True, description='name of the asset category'),
        'runningLow': fields.String(
            required=True, description=''),
        'lowInStock': fields.String(
            required=True, description=''),
        'priority': fields.String(
            required=True, description=''),
        'customAttributes': fields.List(fields.Nested(asset_namespace.model(
            'custom_attributes_asset_categories', {
                'label': fields.String(
                    description='a label of the asset category',
                    required=False,
                ),
                'inputControl': fields.String(
                    description='can be text or drop down',
                    required=False,
                ),
                'isRequired': fields.Boolean(
                    description='can be true or false',
                    default=False,
                    required=False,
                ),
            }))
        )
    })

# swagger model that defines asset supporting document fields
supporting_documents_model = asset_namespace.model(
    "supporting_documents_model", {
        'documentName': fields.String(
            required=True, description='document name'),
        'documentType': fields.String(
            required=True, description='document type'),
        'document': fields.String(
            required=True, description='file to be uploaded')
    })
