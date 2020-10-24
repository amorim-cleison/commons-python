from commons.log import log

def execute_command(command, args):
    from subprocess import (check_call, STDOUT, CalledProcessError)
    str_args = "".join([f"{k} {v}" for k, v in args.items()])
    command_line = f"{command} {str_args}"

    try:
        log(f"Executing '{command_line}'...'", 3)
        check_call(command_line, shell=True, stderr=STDOUT)
        success = True
    except CalledProcessError as e:
        success = False
        log(
            f"Failed to execute command '{command_line}':\n{e.returncode} {e.output}"
        , 3)
    return success
