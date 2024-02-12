""" create reasons """


reject_reason = [{
        "label": "Reason",
        "type": "textarea",
        "name": "reason",
        "placeholder": "Your reason",
    }]


def cancel_reason_options(value='Choose a Reason....'):
    return {
        "text": "*Cancel Hot Desk*",
        "response_type": "in_channel",
        "attachments": [
            {
                "text": "Choose a reason for cancelling your hot desk",
                "fallback": "Choose a reason",
                "color": "danger",
                "attachment_type": "default",
                "value": "This is the way forward",
                "callback_id": "cancel hot desk reason",
                "actions": [
                    {
                        "name": "cancel reason options",
                        "text": value,
                        "type": "select",
                        "options": [
                            {
                                "text": "changed my mind",
                                "value": "changed my mind"
                            },
                            {
                                "text": "leaving early",
                                "value": "leaving early"
                            },
                            {
                                "text": "delayed approval",
                                "value": "delayed approval"
                            },
                            {
                                "text": "seat changed",
                                "value": "seat changed"
                            },
                            {
                                "text": "others",
                                "value": "others"
                            }

                        ]
                    },
                    {
                        "type": "button",
                        "text": "submit",
                        "name": 'submit cancel hot desk reason',
                        "style": "primary",
                        "value": 'submit_cancel'
                    },

                ],

            }
        ]
    }


other_reason_text = [{
        'label': 'Reason',
        'type': 'textarea',
        'name': "cancelled_reason",
        "placeholder": 'Your reason',
        'hint': 'e.g i am feeling sick',
    }]
