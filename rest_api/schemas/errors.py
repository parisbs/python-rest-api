from flask_restplus import fields

common_error_schema = {
    'message': fields.String(
        title='Message',
        description='Error message',
        example='Invalid request',
        readOnly=True
    ),
    'extra_data': fields.String(
        title='Extra data',
        description='Extra data fields',
        example='extra1: some, extra2: 10',
        readOnly=True
    ),
}
