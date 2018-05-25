#!/usr/bin/env python
# *-* coding:UTF-8 *-*

"""
# Author: yuyet 
# Date:   2018/1/31
# Description:
"""

# -------------------
import os

# -------------------


def main():
    file_name = r"E:\cf.txt"
    new_name = r"E:\cf1.txt"
    tmp = ""
    lines = ""
    i = 0
    with open(file_name, "r") as fd, open(new_name, "w") as nfd:
        for line in fd:
            info = line.strip()
            if not info.endswith("="):
                tmp = tmp + info
            else:
                tmp = tmp + info
                lines = lines + tmp + "\t\t\t"
                i = i + 1
                if (i % 5) == 0:
                    nfd.write(lines+"\n\n\n")
                    lines = ""
                tmp = ''


if __name__ == '__main__':
    main()
