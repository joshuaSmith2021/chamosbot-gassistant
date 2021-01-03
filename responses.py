class GoogleAssistantResponse(dict):
    def __init__(self, message, expect_response=True):
        self['payload'] = {
            'google': {
                'expectUserResponse': expect_response,
                'richResponse': {
                    'items': [
                        {
                            'simpleResponse': {
                                'textToSpeech': message
                            }
                        }
                    ]
                }
            }
        }


class TextResponse(dict):
    def __init__(self, message):
        self['fulfillmentMessages'] = [
            {
                'text': {
                    'text': [
                        message
                    ]
                }
            }
        ]

