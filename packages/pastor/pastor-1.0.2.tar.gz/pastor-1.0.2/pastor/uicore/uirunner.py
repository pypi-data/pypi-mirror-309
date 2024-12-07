#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time   :2024/10/31 16:50
# @Author : liangchunhua
# @Desc   :
import validators

def open(url):
    r = validators.url(url)
    if not r:
        raise r
    else:
        print(2)
    print(3)

if __name__ == '__main__':
    open('1')