# FunctionalMaybe
A simple Maybe wrapper class that works. Creates a wrapper around variable and allows transformation of said variable to different values and supplying it to functions.

# Usage:

```Python
import sys
from FunctionalMaybe import FunctionalMaybe as Maybe

joined = Maybe(["one", "two", "three"])\
        .transform(lambda list_: ", ".join(list_))\  # Transform the values to something with lambda
        .run(lambda result: print(result))\          # Run functions with the contained value
        .unwrap()                                    # Return the wrapped value

# We can easily e.g. print, if the wrapped value was an empty
if isinstance(joined, Maybe.Empty):
    print(str(joined), file=sys.stderr)

```

Also supports calling the constructure inside the Maybe-class, which enables error handling via Maybe.Empty:
```Python
from FunctionalMaybe import FunctionalMaybe as Maybe

class Foo:
    def __init__(self, x, y, z=None, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}, {self.w}"

def log(val):
    print(val)

Maybe().construct(Foo, 1, "one", w=4).transform(lambda foo: str(foo)).run(log)
# or could utilize the Maybe.Unwrapper in the following way:
Maybe("one").construct(Foo, 1, Maybe.Unwrapper, w=4).transform(lambda foo: str(foo)).run(log)
# When ever Maybe.Unwrapper is supplied as an argument, the Maybe.Unwrapper object
# is mapped to the wrapped value contained by the Maybe
```
