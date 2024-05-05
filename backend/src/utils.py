from pydantic import ValidationError, TypeAdapter, HttpUrl



def validate_website_url(cls, v):
    if v is None  or v == "":
        return None
    try:
        parsed_url = TypeAdapter(HttpUrl).validate_python(v)
        return str(parsed_url)
    except ValidationError:
        raise ValueError("Invalid HTTP URL Format")
    

def validate_short_description(cls, value):
    if value is not None and value != '':
        if len(value) < 3:
            raise ValueError('Must be at least 3 characters long')
    return value

    

