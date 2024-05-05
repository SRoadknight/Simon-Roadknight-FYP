from typing_extensions import Annotated, TypeAliasType
from annotated_types import Len

ConstrainedId = TypeAliasType(
    'ConstrainedId', 
    Annotated[str, Len(min_length=8, max_length=8)]
    )


# Acts as a title/name for a field in a model
Name = TypeAliasType(
    'Name', 
    Annotated[str, Len(min_length=3, max_length=50)]
    )

Description = TypeAliasType(
    'Description', 
    Annotated[str, Len(min_length=3, max_length=250)]
    )

LongDescription = TypeAliasType(
    'LongDescription', 
    Annotated[str, Len(min_length=3, max_length=1000)]
    )



