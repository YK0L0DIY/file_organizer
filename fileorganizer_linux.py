import argparse
import os
from datetime import datetime

import extensiondict


def concat_folder_with_file(folder: str, file_name: str):
    if folder.endswith('/'):
        return folder + file_name
    else:
        return folder + '/' + file_name


def execute(source: str, output: str, delete_sub_folder: bool = False):
    for filename in os.listdir(source):

        path = concat_folder_with_file(source, filename)

        if filename.startswith('.') or filename.startswith('".'):
            print(f"Ignoring file: {path}")
            continue

        if os.path.isdir(path):
            folder_path = path + '/'
            execute(folder_path, output)
            if delete_sub_folder:
                delete_folder(folder_path)

        else:
            split = os.path.splitext(path)
            extension = split[1]

            try:
                dest = output + extensiondict.extension_dict[extension.lower()]

                file_date = os.path.getmtime(path)
                year = datetime.fromtimestamp(int(file_date)).strftime("%Y")
                month = datetime.fromtimestamp(int(file_date)).strftime("%m")
                day = datetime.fromtimestamp(int(file_date)).strftime("%d")

                dest = f'{dest}/{year}/{month}/{day}'

                final_path_exists = os.path.exists(dest)

                if not final_path_exists:
                    os.makedirs(dest)

                if " " in filename:
                    filename = f'"{filename}"'
                else:
                    filename = filename

                file_exists_in_dest = os.path.isfile(concat_folder_with_file(dest, filename))

                filepath = concat_folder_with_file(source, filename)

                file_exists_in_src = os.path.isfile(filepath)

                if file_exists_in_dest:
                    move_with_new_name_if_exist(filename, source, dest)

                else:
                    if file_exists_in_src and not file_exists_in_dest:
                        movefile(filepath, dest)

            except:
                print(f"Unknown extension: {extension.lower()}")


def move_with_new_name_if_exist(filename, source, dest):
    original_file_name = filename
    file_exists_in_dest = os.path.isfile(concat_folder_with_file(dest, filename))

    count = 1
    while file_exists_in_dest:
        if filename.startswith('"'):
            filename.replace('"', '')
            filename = str(count) + f'_{filename}'
            filename = f'"{filename}"'
        else:
            filename = f"{count}_{filename}"

        file_exists_in_dest = os.path.isfile(concat_folder_with_file(dest, filename))

    movefile(concat_folder_with_file(source, original_file_name), concat_folder_with_file(dest, filename))


# movefile is the function that handles moving of files from source to destination folder
def movefile(src, dst):
    os.system('mv ' + src + ' ' + dst)


# movefile is the function that handles moving of files from source to destination folder
def delete_folder(src):
    if not os.listdir(src):
        os.system('rm -r ' + src)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='File Organizer',
        description='Looks through any folder and subfolder you tell it to and moves the files to respective '
                    'sub folders based on the file type and dates.')

    parser.add_argument('-s', '--source', type=str,
                        help='Source folder where to look for files')

    parser.add_argument('-o', '--output', type=str,
                        help='Output folder where to save organized files')

    parser.add_argument('-d', '--delete', action='store_true',
                        help='Delete processed sub folders')

    args = parser.parse_args()

    src_base = args.source
    dst_base = args.output

    if not src_base.endswith('/'):
        src_base = src_base + '/'

    if not dst_base.endswith('/'):
        dst_base = dst_base + '/'

    execute(src_base, dst_base, args.delete)
