#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-

try:
    from mkgtree import main

except ImportError:
    from .mkgtree import main

finally:
    main()