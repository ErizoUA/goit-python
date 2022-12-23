import argparse
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from itertools import chain
import os
from pathlib import Path
import re
from shutil import move, unpack_archive
from typing import List


parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument("--source", "-s", help="Source folder", required=True)

args = vars(parser.parse_args())

source = args.get("source")
source_folder = Path(source)


extensions = {
        'images': ['.jpeg', '.png', '.jpg', '.svg', '.bmp', '.tiff'],
        'video': ['.avi', '.mp4', '.mov', '.mkv', '.flv'],
        'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx', '.djvu', '.djv', '.csv', '.fb2'],
        'audio': ['.mp3', '.ogg', '.wav', '.amr'],
        'archives': ['.zip', '.tar'],
        'unknown': []
    }

cyrillic_symbols = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюяёъыэ'
cyrillic_to_latin = ('a', 'b', 'v', 'h', 'g', 'd', 'e', 'ye',
                     'zh', 'z', 'y', 'i', 'yi', 'y', 'k', 'l',
                     'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
                     'f', 'kh', 'ts', 'ch', 'sh', 'shch', '', 'yu',
                     'ya', 'yo', '', 'y', 'e')
transliteration = {}

for cyrillic, latin in zip(cyrillic_symbols, cyrillic_to_latin):
    transliteration[ord(cyrillic)] = latin
    transliteration[ord(cyrillic.upper())] = latin.upper()

files_and_folders = []


def read_folder(folder: Path) -> List[Path]:

    for path in folder.iterdir():

        if path.is_file():
            files_and_folders.append(path)

        elif path.is_dir():
            if len(os.listdir(path)) == 0:
                path.rmdir()
                continue

            if path.stem in extensions:
                continue

            files_and_folders.append(path)
            read_folder(path)

    return files_and_folders


def normalize(path: Path) -> None:

    new_name = path.stem.translate(transliteration)
    new_name = re.sub(r'\W', '_', new_name)
    new_path = path.with_stem(f'{new_name}')

    if path.is_dir():
        if path == new_path:
            return

    try:
        new_path = path.rename(new_path)
    except FileExistsError:
        new_path = path.with_stem(f'{new_name}_1')
        new_path = path.rename(new_path)

    return new_path


def add_unknown_ext(path_list: List[Path]) -> None:
    unknown_ext = []

    for path in path_list:

        if path.suffix not in chain(*extensions.values()):
            unknown_ext.append(path.suffix)

    extensions.update(dict(unknown=unknown_ext))


def move_files_to_categorical_folders(path: Path) -> None:

    for folder, ext in extensions.items():

        if path.suffix in ext:
            categorical_dir = path.parent / folder
            categorical_dir.mkdir(parents=True, exist_ok=True)

            if path.suffix in extensions.get('archives'):
                new_path = categorical_dir / path.stem
                unpack_archive(path, new_path)
                path.unlink()
            else:
                move(path, categorical_dir)

            break


if __name__ == '__main__':

    if not source_folder.exists():
        raise ValueError("Folder isn't exist")

    files_and_folders_list = read_folder(source_folder)
    files = [file for file in files_and_folders_list if file.is_file()]
    folders = [folder for folder in files_and_folders_list if folder.is_dir()][::-1]

    with ThreadPoolExecutor(max_workers=10) as executor:

        normalize_files = [executor.submit(normalize, file) for file in files]
        wait(normalize_files)

        results_normalize_files = [result.result() for result in normalize_files]
        add_unknown_ext(results_normalize_files)

        executor.map(move_files_to_categorical_folders, results_normalize_files)

    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.map(normalize, folders)
