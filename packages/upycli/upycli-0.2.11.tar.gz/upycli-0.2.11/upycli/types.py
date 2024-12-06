def resolve(dtype, default = (None, None, None)):
    
    kwdict = { "required": True }
    
    # For lists, we want to use nargs in argparse
    if dtype == list:
        kwdict = { **kwdict, "action": "store", "nargs": "*" }
    # For bools, we want to have action
    elif dtype == bool:
        kwdict = { **kwdict, "action": "store_true" }
    # For everything else just simple type
    else:
        kwdict = { **kwdict, "type": dtype }
        
    if default != (None, None, None):
        del kwdict["required"]
        kwdict = { **kwdict, 
            "default": default,
            "help": f"(default {default})",
        }
        
    return kwdict
