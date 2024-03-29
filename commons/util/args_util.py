class Argument:

    __DEFAULTS = {dict: dict(), list: list(), tuple: tuple(), str: None}

    def __init__(self,
                 *flags,
                 type=str,
                 default=None,
                 options=None,
                 required=False,
                 help=None) -> None:
        self.flags = flags
        self.type = type
        self.default = self.__DEFAULTS.get(
            type,
            default) if (default is None) and (type is not None) else default
        self.options = options
        self.required = False
        self.help = help


def load_args(description, arguments, argv=None):
    """
    Load the arguments provided to the application. This is the priority applied:
    1. Arguments informed in shell;
    2. Arguments informed in config file.
    """
    assert (arguments is not None), "Arguments must be informed."

    # Load arguments from shell:
    if argv is None:
        import sys
        argv = sys.argv[1:]

    # Load from `config` file:
    parser = __create_parser(description, arguments)
    configs = __read_config_file(argv, parser)

    # Load from shell:
    parser.set_defaults(**configs)
    return parser.parse_args(argv)


def save_args(args, path):
    from commons.util import save_yaml
    args = args if isinstance(args, dict) else vars(args)
    save_yaml(args, path)


def __create_parser(description, arguments=list()):
    from argparse import ArgumentParser
    from commons.constant import GLOBAL_ARGS

    parser = ArgumentParser(add_help=True, description=description)
    type_fn = {list: str2list, bool: str2bool, dict: str2dict}

    # Add standard arg to arguments list:
    for arg in GLOBAL_ARGS:
        arguments.insert(0, arg)

    for opt in arguments:
        assert (
            opt.flags
            is not None), "Flag property must be specified for all arguments."

        _names = [f if f.startswith("-") else f"-{f}" for f in opt.flags]
        _type = type_fn.get(opt.type, opt.type)
        _default = opt.default
        _options = opt.options
        _required = opt.required
        _help = opt.help
        parser.add_argument(*_names,
                            type=_type,
                            default=_default,
                            choices=_options,
                            required=_required,
                            help=_help)
    return parser


def __read_config_file(argv, parser):
    from commons.util import exists, read_yaml
    args = parser.parse_args(argv)

    if (args is not None) and ("config" in args) and (args.config is not None) and exists(args.config):
        # load config file
        configs = read_yaml(args.config)

        # update parser from config file
        key = vars(args).keys()
        for k in configs.keys():
            assert (k in key), f"Unknown argument: {k}"
        return configs
    return dict()


def str2list(strlist):
    """Convert key1,key2,... string into list.
    :param strlist: key1,key2
    strlist can be comma or space separated.
    """
    import re

    if strlist is not None:
        strlist = strlist.strip(', ')
    if not strlist:
        return []
    return re.split("[, ]+", strlist)


def str2bool(v):
    """
    Convert boolean string values into a `bool`.
    """
    import argparse

    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def str2dict(v):
    """
    Convert a dict string into a `dict`.
    """
    return eval(f"dict({v})")
