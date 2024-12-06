#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
import os

__version__ = "0.1.2"

def __tree__(root, max_depth=None, exclude=None, indent='', legacy: bool=False):
    if legacy == True:
        branch = "|---"
        final  = "|___"

    else:
        branch = "├──"
        final  = "└──"


    if not os.path.isdir(root):
        print("Invalid directory path.")
        return
    
    if exclude is not None and any(ex in root for ex in exclude):
        return
    
    try:
        items = os.listdir(root)

        for i, item in enumerate(sorted(items)):
            item_path = os.path.join(root, item)
            is_last = i == len(items) - 1
            
            if os.path.isdir(item_path):
                print(f"{indent}{final if is_last else branch} {item}/")
                sub_indent = indent + '    ' if is_last else indent + '│   '
                
                if max_depth is None or len(sub_indent) // 4 < max_depth:
                    __tree__(item_path, indent=sub_indent, max_depth=max_depth, exclude=exclude, legacy=legacy)
            else:
                print(f"{indent}{final if is_last else branch} {item}")
    
    except PermissionError as e:
        print(f"{indent}Permission Denied ({e.filename})")
        return

def maketree(root, max_depth=None, exclude=None, indent='', legacy=False):
        __tree__(root, max_depth, exclude, indent, legacy)

def main():
    maketree(os.getcwd(), None, None, '', False)

if __name__ == "__main__":
    main()