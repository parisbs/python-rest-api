from flask_restplus import fields

user_schema = {
    'id': fields.Integer(
        title='ID',
        description='Example ID',
        example='1',
        readOnly=True,
    ),
    'email': fields.String(
        title='Email',
        description='ID email',
        example='john.smith@example.com',
        readOnly=True,
    ),
    'name': fields.String(
        title='Name',
        description='ID name',
        example='John Smith',
        readOnly=True,
    ),
}
