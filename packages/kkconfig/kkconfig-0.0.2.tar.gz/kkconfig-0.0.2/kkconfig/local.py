"""
Functions for managing local configurations for a project.
"""

import yaml
import os

def load_settings(cfgpath, env):
    """
    Loads the contents of the `cfgpath` YAML file and updates the contents of
    `env` with the values.

    If `cfgpath` does not exists, then the function silently returns. This is
    when no override of the settings is desired.

    If `cfgpath` is a list, then the items are checked sequentially and loaded
    if each exists.
    """
    # Normalize the input types
    if type(cfgpath)!=list:
        cfgpath=[cfgpath]

    # Existing paths only
    cfgpath = filter(lambda mycfgpath: os.path.exists(mycfgpath), cfgpath)

    # Loop and load!
    for mycfgpath in cfgpath:
        cfg = yaml.safe_load(open(mycfgpath))
        env.update(cfg)
