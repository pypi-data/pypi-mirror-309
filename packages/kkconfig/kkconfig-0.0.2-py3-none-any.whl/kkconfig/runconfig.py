"""
Configure script execution
"""

import yaml

def load(runcfgpaths):
    """
    Load run configurations from paths stored in the `runcfgpaths` list and
    return the merged result as a dictionary.
    """
    runcfg = {}
    for runcfgpath in runcfgpaths:
        myruncfg=yaml.safe_load(open(runcfgpath))
        runcfg.update(myruncfg)
    return runcfg