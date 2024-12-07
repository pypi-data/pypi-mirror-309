
Some small Python utilities for everyday convenience.

See code for more details about the utilities themselves.


A note on packaging/installation:
---------------------------------

Note that the package name and import name is
anton_util
not
anton-util
as in the pip install command shown on PyPI. If I remember, there is a bug somewhere in the Python distribution chain that replaces _ with - in package names. It seems to be around PyPI since the package import name and pip name is according to the pyproject.toml, ie anton_util. This is important, since
import anton-util
is invalid Python syntax while
import anton_util
works just fine.

pip install anton_util
seems to work too, so it might be more or less a display bug only.





//AB
