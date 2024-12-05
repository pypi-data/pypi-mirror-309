# Yuck!

`Yuck!` is a library that is helpful when you need to create a singleton instance of a function.

Just decorate the function you want to singletonize, call it once with setup arguments and subsequent calls
will use the already setup function call.


## Example

```py
from yuck import yuck


@yuck
def db(connection_string: str):
    connection = connect(connection_string)

    query = yield
    while True:
        query = yield connection.execute(query)


# Initial setup
db_instance = db("sqlite:///:memory:")

# Use the singleton instance
result = db_instance.send("SELECT * FROM users")
print(result)

```

> NOTE: I'm not entirely sure this really works but I'm too lazy to even check :D.