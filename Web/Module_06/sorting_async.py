import argparse
import asyncio
from itertools import chain
import os
import re
from typing import List

from aiopath import AsyncPath
from aioshutil import move, unpack_archive


parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument("--source", "-s", help="Source folder", required=True)

args = vars(parser.parse_args())

source = args.get("source")
source_folder = AsyncPath(source)


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

files_extension_to_folders = {
        'images': ['.jpeg', '.png', '.jpg', '.svg', '.bmp', '.tiff'],
        'video': ['.avi', '.mp4', '.mov', '.mkv', '.flv'],
        'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx', '.djvu', '.djv', '.csv', '.fb2'],
        'audio': ['.mp3', '.ogg', '.wav', '.amr'],
        'archives': ['.zip', '.gz', '.tar']
    }

files_and_folders = []


async def read_folder(folder: AsyncPath) -> List[AsyncPath]:

    async for path in folder.iterdir():

        if await path.is_file():
            files_and_folders.append(path)

        elif await path.is_dir():
            if len(os.listdir(path)) == 0:
                await path.rmdir()
                continue

            files_and_folders.append(path)
            await read_folder(path)

    return files_and_folders


async def normalize(path_list: List[AsyncPath]) -> List[AsyncPath]:

    normalized_names = []

    for path in path_list:

        new_name = path.stem.translate(transliteration)
        new_name = re.sub(r'\W', '_', new_name)
        new_path = path.with_stem(f'{new_name}')

        try:
            new_path = await path.rename(new_path)
        except FileExistsError:
            new_path = path.with_stem(f'{new_name}_1')
            new_path = await path.rename(new_path)

        normalized_names.append(new_path)

    return normalized_names


def add_unknown_ext(path_list: List[AsyncPath]) -> None:
    unknown_ext = []

    for path in path_list:

        if path.suffix not in chain(*extensions.values()):
            unknown_ext.append(path.suffix)

    extensions.update(dict(unknown=unknown_ext))


async def move_files_to_categorical_folders(files):

    for path in files:

        for folder, ext in extensions.items():

            if path.suffix in ext:
                categorical_dir = path.parent / folder
                await categorical_dir.mkdir(parents=True, exist_ok=True)

                if path.suffix in extensions.get('archives'):
                    new_path = categorical_dir / path.stem
                    await unpack_archive(path, new_path)
                    await path.unlink()
                else:
                    await move(path, categorical_dir)

                break


async def perform(sorting_folder: AsyncPath) -> None:
    files_and_folders_list = await read_folder(sorting_folder)
    files = [file for file in files_and_folders_list if await file.is_file()]
    folders = [folder for folder in files_and_folders_list if await folder.is_dir()][::-1]

    normalized_files = await normalize(files)
    add_unknown_ext(normalized_files)
    await move_files_to_categorical_folders(normalized_files)

    await normalize(folders)


async def main(sorting_folder: AsyncPath) -> None:

    if not await source_folder.exists():
        raise ValueError("Folder for sorting isn't exist")

    await perform(sorting_folder)


if __name__ == '__main__':

    asyncio.run(main(source_folder))
