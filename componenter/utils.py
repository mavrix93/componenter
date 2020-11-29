def unwrap_type(inst):

    return inst.__origin__ if inst.__class__.__name__ == "_GenericAlias" else inst
