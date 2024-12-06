#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-

try:
    from sysinsight import main

except ImportError:
    from .sysinsight import main

finally:
    main()