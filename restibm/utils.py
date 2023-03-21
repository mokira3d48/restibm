import inspect


# Tags constants:
EXCEPT = '[ \033[91mPROGRAMMING ERROR\033[0m ]  '
ERRO = '[ \033[91mERRO\033[0m ]  '
WARN = '[ \033[93mWARN\033[0m ]  '
INFO = '[ \033[94mINFO\033[0m ]  '
SUCC = '[ \033[32mOK\033[0m ]    '


def get_app_name(cls):
    """Function to get a application name from a class.
    
    Attributs:
        cls (type): The type that we want retreive his application name.
    
    Returns:
        str: The application that contains this cls.
    """
    if not inspect.isclass(cls):
        raise TypeError(EXCEPT + "`cls` must be a 'python type'.")
    return cls.__module__.split('.')[0]

