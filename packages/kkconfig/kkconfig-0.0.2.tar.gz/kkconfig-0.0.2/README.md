# Karol Krizka's Project Configuration
Module to help with configuration of local workspaces.

## Local Configuration
The goal of the local configuration is to provide a mechanism for providing ]
setting specific to the local workspaces (ie: paths to local data).

The project should provide a module `config` that contains the following
snipplet:

```python
from kkconfig import local

mydatapath = '/default/path/to/data'

local.load_settings('.myproject.yaml', globals())
```

The `load_settings` function will load the settings from the specified file (if
it exists) and update the global namespace (aka `config` module globals) with
the contents. The variables should also be provided this module to provide
default values and show available settings.