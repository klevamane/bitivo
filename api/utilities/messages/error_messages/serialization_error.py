error_dict = {  # pylint: disable=C0103
    'invalid_file_type': 'Sorry, this {} file type is currently not supported',
    'invalid_column': 'Invalid filter column: {}',
    'invalid_query_key':
    'Query keys must be one or all of {}. Please check if they have required parameters',
    'invalid_request_param': '{0} must be one of {1}',
    'not_empty': "This cannot be empty",
    'url_syntax': '{0} is not a valid url',
    'email_syntax': 'This is not a valid andela email address',
    'email_exists': '{0} is already registered',
    'email_length': 'Email must be at least 6 characters',
    'field_required': 'This field is required',
    'field_length': 'Field must be at least {0} characters',
    'json_invalid': 'Invalid JSON input provided',
    'string_characters':
    'Field must start with an alphabet, only contain alphanumeric characters, non-consecutive fullstops, hyphens, spaces and apostrophes',
    # pylint: disable=C0301
    'string_length': 'Field must be {0} characters or less',
    'input_control':
    'Incorrect input control type provided, please provide one of {input_controls}',  # pylint: disable=C0301
    'choices_required':
    'choices seperated by comma must be provided if multi choice inputs controls are selected',
    # pylint: disable=C0301
    'provide_attributes': 'Please provide at least one attribute',
    'attribute_required':
    'The following required attribute(s) must be included: {}',
    'unrelated_attribute':
    'The attribute {} is not related to this asset category',
    'invalid_category_id': 'This asset category id is invalid',
    'invalid_center_id': 'This center id is invalid',
    'category_not_found': 'This category does not exist in the database',
    'center_not_found': 'This center does not exist in the database',
    'request_type_not_found':
    'This request type does not exist in the database',
    'invalid_request_status_type':
    "Invalid request status type '{}'. Allowed status types are: {}",
    'attribute_not_related':
    'attribute with the id of {attribute_id} is not related to the asset category of id {asset_category_id}',
    # pylint: disable=C0301
    'invalid_id': 'Invalid id in parameter',
    'invalid_resource_access_levels': 'Invalid type. Please provide an object',
    'invalid_resource_access_levels_list':
    'Invalid type. Please provide an array',
    'key_error': '{} key not found',
    'choices_type': 'Choices must be an Array',
    'invalid_field': 'invalid field supplied',
    'invalid_query': "Only takes 'include=children' as query",
    'invalid_query_strings': '{0} contains invalid parameter {1}',
    'json_type_required': 'Content-Type should be application/json',
    'duplicate_asset': 'Asset with the tag {} already exists',
    'asset_category_assets': 'Assets for category {} fetched successfully',
    'exists': '{} already exists',
    'last_page_returned':
    'The requested page exceeds the total pages count, however the last page was returned',
    'not_found': '{} not found',
    'invalid_choice':
    'The value of attribute {} must be one of these options: {}',
    'must_have_parent_space': 'This space needs to have a parent space',
    'cannot_have_parent_space': 'This space cannot have a parent space',
    'cannot_have_parent_type': 'This space cannot have a {} as a parent space',
    'centers_not_match':
    "Space cannot be assigned under a parent space from another center",
    'not_provided': 'No valid field(s) in request body',
    'invalid_id_field': 'This is not a valid id string',
    'invalid_status': "status must be 'enabled' or 'disabled'",
    'invalid_hot_desk_status':
    "status must be 'pending', 'approved' or 'rejected",
    'archived': '{} has been Archived',
    'can_not_edit_parent':
    'can not change a building/floor to a room if it has children',
    'provide_space_and_spacetype_id':
    'You need to provide both parentId and spaceTypeId to update a space or spaceId',
    'space_not_found': 'This space does not exist in the database',
    'invalid_space_id': 'This space id is invalid',
    'not_in_center': "This space is not part of the asset's center",
    'duplicate_found': 'Duplicate {}(s) found in the submitted request',
    'single_permission': '{} supplied, no need of the extra permission(s)',
    'assignee_not_found': 'The assignee was not found',
    'invalid_assignee_type':
    "Invalid assignee type '{}'. Only 'space' and 'user' are allowed",
    'invalid_assignee_id': 'The assignee id is invalid',
    'non_matching_assignee_type':
    'The assignee type does not match the assignee id provided',
    'assignee_id_and_type_required':
    'Both assigneeId and assigneeType are required',
    'invalid_period': 'An invalid {} number was provided',
    'asset_status':
    'Incorrect asset status provided, please provide one of {asset_status}',
    'invalid_doc_name':
    'Incorrect doc_name provided, please provide one of {}',
    'missing_entry': 'Please include the {} value.',
    'comparison_error': '{} value must be greater than {} value',
    'invalid_priority':
    "Invalid priority. Only 'Key' and 'Not Key' are allowed",
    'invalid_input_value': 'invalid {} value',
    'missing_input_field': '{} field missing from request',
    'stock_count_exists': 'Stock count for this given period already exists',
    'different_week': 'Week values must be the same',
    'invalid_value': '{} is an invalid value for {}',
    'invalid_query_wrong_value':
    'Invalid URL query: `{}` is assigned an invalid value: `{}`',
    'invalid_date':
    'Invalid date format {}. Please use a valid date using the following format: YYYY-MM-DD',
    # pylint: disable=C0301
    'invalid_provided_date': 'Invalid date range please, {}.',
    'invalid_date_time':
    'Invalid date time format {}. Please use a valid date time using the following format: YYYY-MM-DD HH:MM:SS',
    'invalid_date_range': 'start date cannot be greater than end date',
    'invalid_start_date': 'start date cannot be greater than today',
    'invalid_end_date': 'end date must be today if no start date is provided',
    'missing_fields': 'The `{}` field cannot be empty',
    'invalid_date_input':
    'Input error: Valid `{}` must be a number from 0 to {}',
    'invalid_day_in_date_input':
    '{} Input error: Valid `{}` must be greater than or equal to {}',
    'user_not_found': '{} not found in the specified center',
    'resource_not_found': '{} not found',
    'requester_not_found': 'The requester was not found',
    'requester_not_found_in_center':
    'The requester was not found in the center',
    'request_type_not_found_in_center':
    'The request type was not found in the center',
    'invalid_requester_id': 'The requester id is invalid',
    'requester_cannot_be_responder': 'The requester cannot be a responder',
    'not_owner': 'You cannot update a comment not authored by you',
    'delete_error': 'You cannot delete {} you did not create',
    'invalid_include_key': 'The query param "include" must be {}',
    'generic_not_found': 'The {} was not found',
    'invalid_data_type': "only data of type list is allowed for attachments",
    'processed status': 'sorry, {} is no longer open to be deleted.',
    'invalid_enum_value': 'Please provide one of this {values}',
    'assignee_not_found': 'The assignee was not found in the center',
    'work_order_exists':
    "The work order '{}' for that maintenance category exists in the center",
    'maintenance_category_exists':
    "The maintenance category '{}' for that asset category exists in the center",
    'invalid_request_type_time':
    "`{}` input error: must be an object that contains either `{}`",
    'invalid_date_sum':
    '{} Input error: The sum of the values of `{}` must be greater than `{}`',
    'cannot_delete': "You are not authorised to delete this {} please",
    "invalid_param_key": 'The query param  must be {}',
    'incomplete_transaction': 'Request incomplete, {} not created',
    "cannot_update":
    "something went wrong, try again.check the work order id if you are updating",
    "invalid_date_time":
    "Invalid date time format {}. Please use a valid date time using the following format: YYYY-MM-DD HH:MM:SS",
    "request_status_update":
    "You are not permitted to update the {} of this request",
    "request_assignee_update":
    "You are not permitted to assign this request to an {}.",
    "request_center_update":
    "You are not permitted to update the {} of this request",
    "requester_two_fields":
    "You are not permitted to updated the {} and {} of this request",
    "requester_three_fields":
    "You are not permitted to update the {}, {} and {} of this request",
    "data_type": "{} should be a {}",
    "required_field": "{} is a required field",
    "not_created": "{} not created",
    "not_choice": "{} is not a valid choice. Choice are {}",
    'delete_not_allowed': "You are not authorised to delete this {} please",
    'cannot_be_empty': "Provide one or more {} please",
    "required_param_key": "{} is a required query param for this request",
    'cant_view': "You are not allowed to view this HotDesk Request",
    'cant_cancel': "You are not allowed to cancel this {}",
    'invalid_hotdesk_status': "You can only cancel a pending or approved {}",
    'select_reason': "Please select a {}",
    'complainant_not_found': 'The complainant was not found',
    'invalid_asset_id': 'This asset id is invalid',
    'asset_not_found': 'The asset was not found',
    'invalid_complainant_id': 'The complainant id is invalid',
    'invalid_return_date': 'Expected return date cannot be before today',
    'invalid_document_type': "The document type is invalid. Valid choices are: {choices}",
    'form_data_type_required': 'Content-Type should be multipart/form-data',
    'invalid_search_param': 'Invalid search param key',
    'empty_query_param_value': 'Query parameter value cannot be empty',
    'image_url_and_public_id_missing': 'You must provide an image url and a public_id'
}
