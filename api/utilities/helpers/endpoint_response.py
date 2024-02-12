from ..messages.success_messages import SUCCESS_MESSAGES


def get_success_responses_for_post_and_patch(model_instance, schema,
                                             *message_args, **kwargs):
    return ({
        "status":
        "success",
        "message":
        SUCCESS_MESSAGES[kwargs.get('message_key')].format(*message_args),
        "data":
        schema.dump(model_instance).data,
    }, kwargs.get('status_code'))
