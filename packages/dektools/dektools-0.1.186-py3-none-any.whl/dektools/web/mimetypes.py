from mimetypes import MimeTypes

mimetypes = MimeTypes()

custom_types = {
    'text/javascript': '.js',
    'application/x-javascript': '.js'
}

for k, v in custom_types.items():
    mimetypes.add_type(k, v)
