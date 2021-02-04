import os
from subprocess import PIPE


def execute_command(command, args, stdout=PIPE, stderr=PIPE):
    from subprocess import (check_call, CalledProcessError)
      
    if isinstance(args, dict):
        str_args = " ".join([f"{k} {v}" for k, v in args.items()])
    elif isinstance(args, list):
        str_args = " ".join(str(x) for x in args)
    elif isinstance(args, str):
        str_args = args
    command_line = f"{command} {str_args}"

    with open(os.devnull, 'w') as FNULL:
        try:
            stdout = (FNULL if stdout is None else stdout)
            stderr = (FNULL if stderr is None else stderr)
            code = check_call(command_line,
                              shell=True,
                              stdout=stdout,
                              stderr=stderr)
            return (code == 0), None, None
        except CalledProcessError as e:
            return False, str(e), e
