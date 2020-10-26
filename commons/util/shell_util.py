import os
from subprocess import PIPE


def execute_command(command, args, stdout=PIPE, stderr=PIPE):
    from subprocess import (check_call, CalledProcessError)
    str_args = " ".join([f"{k} {v}" for k, v in args.items()])
    command_line = f"{command} {str_args}"

    with open(os.devnull, 'w') as FNULL:
        try:
            stdout = (FNULL if stdout is None else stdout)
            stderr = (FNULL if stderr is None else stderr)
            code = check_call(command_line,
                              shell=True,
                              stdout=stdout,
                              stderr=stderr)
            return (code == 0), None
        except CalledProcessError as e:
            return False, str(e)
