# fastapi-uuidbase62

`fastapi-uuidbase62` is intended to provide Pydantic and FastAPI functionality that exposes UUID values as
nicely-formatted Stripe-like string values, with validated prefixing. For example, a User UUID identifier of
`"f8711c37-c1d1-4961-ba3c-98cdc5b4fda8"` with a `"user"` prefix becomes `"user_7yNMTpVy8ddRxYKGJqtk7e"`.

## Benefits

Why take this approach?

- users: easy text selection of Stripe-like formatted values (fast double-click or keyboard-based) compared to UUIDs (
  try double clicking the samples above!)
- database: using UUIDs in your database is likely much more efficient storage-wise as well as more performant
- prefixing:
    - allows for programmatic routing within a microservice architecture
    - easier to reason about debug output, logging messages (lower cognitive load/overhead)

## Installation

`fastapi-uuidbase62` installation is much the same as any other Python package.

```commandline
pip install fastapi-uuidbase62
```

### Python Support
Python 3.7, 3.8, 3.9, 3.10, 3.11 are supported and covered by the `tox` test configuration described below. 

## Usage

This package provides the ability to define a field on a Pydantic model that auto-serializes a UUID value to 
base62 and auto-prefixes a defined label. This serializes a UUID to a prefixed string when rendering a FastAPI 
response, and does the reverse when processing an incoming FastAPI request.

In the following example, take note of the following:
- `UUIDBase62ModelMixin` adds a `to_uuidbase62` method to Model to easily convert a UUID or valid base62 prefixed value to a `UUIDBase62` value 
- the `con_uuidbase62` function, which defines the autoprefixing and serializing UUID <-> str field
- the `get_validated_uuidbase62_by_model` dependency injection function providing validation/serialization on incoming base62-encoded parameters (path, header, query)
  - there is a similar `get_validated_uuidbase62` function that does not rely on a Model class/field
- `UUIDBase62` instance properties
  - `uuidbase62_value.uuid`: UUID matching the base62 encoded str
  - `uuidbase62_value.base62_str`: non-prefixed base62 string value
  - `uuidbase62_value.value`: prefixed base62 string value, same as `str(uuidbase62_value)`
  - `uuidbase62_value.prefix`: the prefix used for this `UUIDBase62` instance

```Python
import uuid

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from uuidbase62 import con_uuidbase62, UUIDBase62, UUIDBase62ModelMixin, get_validated_uuidbase62_by_model

app = FastAPI()


class Book(UUIDBase62ModelMixin, BaseModel):
    id: con_uuidbase62(prefix="book")
    title: str


@app.get("/", response_model=list[Book])
async def get_item_list():
    # fake fetching a list of books from the DB, yielding book IDs and titles
    return [{
        "id": uuid.uuid4(),
        "title": "Red Mars",
    }]


@app.get("/{item_id}", response_model=Book)
async def get_item(item_id: UUIDBase62 = Depends(get_validated_uuidbase62_by_model(Book, 'id', 'item_id'))):
    # fake fetching from the DB based on `item_id`, yielding a book ID and title
    return {
        "id": uuid.uuid4(),
        "title": "Green Mars",
    }


@app.post("/", response_model=Book)
async def create_item(item: Book):
    book_id = item.id  # UUIDBase62 value
    book_id.uuid  # uuid value
    book_id.base62_str  # non-prefixed base62 string value
    book_id.value  # prefixed base62 string value, same as str(book_id)
    book_id.prefix  # 'book'

    return item.dict()
```

## Development
To set up a development environment, it is recommended to create a Python virtual environment, and then install 
development requirements. You should probably be using 
[`pyenv` to manage your local Python versions](https://github.com/pyenv/pyenv):

```commandline
# do this for each supported Python version, all are needed to run complete tests via tox
pyenv install 3.x.x 

# in the project directory, make supported Python versions available; first one listed is the default Python
pyenv local 3.10.x 3.7.x 3.8.x 3.9.x 3.11.x 

# create Python virtual environment
python -m venv venv

# install development dependencies
./venv/bin/pip install -r requirements.txt
```

### Testing
`fastapi-uuidbase62` is easily tested via the [configuration set up with `tox`](./tox.ini), which configures the `tox` 
command line tool:

```commandline
# run tox, parallel mode
./venv/bin/tox -p
```

## Contributing
Leverage [Github issues](https://github.com/jaddison/fastapi-uuidbase62/issues), and do consider submitting fixes/improvements via pull requests on Github.


