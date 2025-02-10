#!/usr/bin/env python3
# Copyright (c) 2025 Zet Software All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
# Create role structure directoris

import os
import sys
from pathlib import Path
from itertools import islice

space =  '    '
branch = '│   '
tee =    '├── '
last =   '└── '

path_roles = "roles"
role_directoris = ["defaults","docs","files","meta","tasks","vars","templates","handlers"]
file_yaml = "main.yml"

def tree(dir_path: Path, level: int=-1, limit_to_directories: bool=False,length_limit: int=1000):
    """Given a directory Path object print a visual tree structure"""
    dir_path = Path(dir_path) # accept string coerceable to Path
    files = 0
    directories = 0
    def inner(dir_path: Path, prefix: str='', level=-1):
        nonlocal files, directories
        if not level: 
            return # 0, stop iterating
        if limit_to_directories:
            contents = [d for d in dir_path.iterdir() if d.is_dir()]
        else: 
            contents = list(dir_path.iterdir())
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield prefix + pointer + path.name
                directories += 1
                extension = branch if pointer == tee else space 
                yield from inner(path, prefix=prefix+extension, level=level-1)
            elif not limit_to_directories:
                yield prefix + pointer + path.name
                files += 1
    print(dir_path.name)
    iterator = inner(dir_path, level=level)
    for line in islice(iterator, length_limit):
        print(line)
    if next(iterator, None):
        print(f'... length_limit, {length_limit}, reached, counted:')
    print(f'\n{directories} directories' + (f', {files} files' if files else ''))


def main():
    os.chdir("..")
    role = input("Enter role name: ")
    with open(role + ".yml","w") as role_file:
        role_file.write("---" + role_file.name)
        role_file.write("# File: " + role_file.name)
        role_file.write("# Role: " + role)
        role_file.close()
    if not os.path.exists(path_roles): os.makedirs(path_roles)
    os.chdir(path_roles)
    os.makedirs(role)
    os.chdir(role)
    for dir_ansible in role_directoris:
        os.makedirs(dir_ansible)
        os.chdir(dir_ansible)
        with open(file_yaml,"w") as f:
            f.write("---")
            f.write("#file in " + path_roles + "/" + dir_ansible + "/" + f.name )
            f.close()
        os.chdir("..")
    os.chdir("../../")
    tree(path_roles)


if __name__ == "__main__":
    main()


