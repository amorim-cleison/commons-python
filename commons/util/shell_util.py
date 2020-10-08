
def download_file(url, target_file):
    print(f"Downloading '{url}''...")
    command = 'wget {}'.format(url)
    args = {'-O': target_file, '-q': '', '--show-progress': ''}
    execute_command(command, args)


def execute_command(self, command, args):
    from subprocess import (check_call, STDOUT, CalledProcessError)
    str_args = "".join([f"{k} {v}" for k, v in args.items()])
    command_line = f"{command} {str_args}"

    try:
        check_call(command_line, shell=True, stderr=STDOUT)
        success = True
    except CalledProcessError as e:
        success = False
        print(
            f"Failed to execute command '{command_line}':\n{e.returncode} {e.output}"
        )
    return success