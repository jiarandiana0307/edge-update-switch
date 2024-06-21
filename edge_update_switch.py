import os
import sys
import psutil


disabled_suffix = '_disabled'


def is_update_program(file):
    path, filename = os.path.split(file)
    name, ext = os.path.splitext(filename)
    if sys.platform == 'win32':
        if ext != '.exe':
            return False
        if 'update' not in name.lower() and 'elevation_service' not in name:
            return False
        return True
    elif sys.platform == 'darwin':
        if name.startswith('EdgeUpdater'):
            return True
    return False


def get_update_program_paths():
    """
    Get a list of the paths containing the update programs
    """
    os_and_update_program_paths = {
        'win32': [
            os.path.join(os.getenv('SystemDrive', 'C:'), '\\Program Files (x86)\\Microsoft')
        ],
        'darwin': [
            '/Library/Application Support/Microsoft', 
            '/Applications/Microsoft Edge.app',
            '/Applications/Microsoft Edge Canary.app',
            '/Applications/Microsoft Edge Dev.app',
            '/Applications/Microsoft Edge Beta.app'
        ]
    }
    for platform, paths in os_and_update_program_paths.items():
        if sys.platform.startswith(platform):
            return paths

    return None


def get_update_programs(path):
    """
    Get a list of update programs in the given path
    """
    update_programs = []
    if not os.path.exists(path):
        return []
    elif is_update_program(path):
        update_programs.append(path)
    elif os.path.isdir(path):
        for subfile in os.listdir(path):
            result = get_update_programs(os.path.join(path, subfile))
            update_programs.extend(result)

    return update_programs


def get_new_file_name(file):
    path, filename = os.path.split(file)
    name, ext = os.path.splitext(filename)
    if name.endswith(disabled_suffix):
        new_name = name[:-len(disabled_suffix)]
    else:
        new_name = name + disabled_suffix
    return os.path.join(path, new_name + ext)


def terminate_update_programs():
    """
    Terminate the update programs running in the background
    and return a list of terminated update programs
    """
    terminated = set()
    for process in psutil.process_iter():
        try:
            if not process.is_running():
                continue
            if not is_update_program(process.name()):
                continue
            location = process.exe()
            process.kill()
            terminated.add(location)
        except psutil.NoSuchProcess:
            pass
    return terminated


def disable_update():
    """
    Disable Edge update and return a list of pairs of 
    original name and new name of disabled update programs
    """
    update_program_paths = get_update_program_paths()
    if update_program_paths is None:
        return []

    update_programs = []
    for path in update_program_paths:
        update_programs.extend(get_update_programs(path))

    disabled_files = []
    for file in update_programs:
        if not os.path.exists(file):
            continue
        path, filename = os.path.split(file)
        name, ext = os.path.splitext(filename)
        if not name.endswith(disabled_suffix):
            new_file = get_new_file_name(file)
            os.rename(file, new_file)
            disabled_files.append([file, new_file])

    return disabled_files


def enable_update():
    """
    Enable Edge update and return a list of pairs of
    new name and original name of enabled update programs
    """
    update_program_paths = get_update_program_paths()
    if update_program_paths is None:
        return []

    update_programs = []
    for path in update_program_paths:
        if not os.path.exists(path):
            continue
        update_programs.extend(get_update_programs(path))

    enabled_files = []
    for file in update_programs:
        if not os.path.exists(file):
            continue
        path, filename = os.path.split(file)
        name, ext = os.path.splitext(filename)
        if name.endswith(disabled_suffix):
            new_file = get_new_file_name(file)
            os.rename(file, new_file)
            enabled_files.append([file, new_file])

    return enabled_files


def main():
    if sys.platform == 'win32':
        # request administrator in Windows
        from ctypes import windll
        if not windll.Shell32.IsUserAnAdmin():
            windll.Shell32.ShellExecuteW(None, 'runas', os.sys.executable, __file__, None, 1)
            return

    update_program_paths = get_update_program_paths()
    if update_program_paths is None:
        print('Unsupported operation system')
        return

    terminated = terminate_update_programs()
    if len(terminated) > 0:
        print('Shutdown update program')
        for program in terminated:
            print('Killed', program)

    try:
        result = disable_update()
        if len(result) > 0:
            print('Rename:')
            for old, new in result:
                print(old, '->', os.path.split(new)[1])
            print('Edge update disabled')

        else:
            result = enable_update()
            if len(result) > 0:
                print('Rename:')
                for old, new in result:
                    print(old, '->', os.path.split(new)[1])
                print('Edge update enabled')

        if len(result) == 0:
            print('No update program disabled or enabled')

    except (PermissionError, psutil.AccessDenied) as e:
        print('Must run as admin')

    input('Enter to continue...')


if __name__ == '__main__':
    main()
