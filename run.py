#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from web.server import Server


def main():
    with open("lib/config.json", 'r') as f:
        data = json.load(f)
    s = Server(data)
    s.run()


if __name__ == '__main__':
    main()
