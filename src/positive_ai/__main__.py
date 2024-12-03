#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Package entry point."""
import os
import sys


sys.path.append(os.getcwd())


if __name__ == "__main__":  # pragma: no cover
    from positive_ai.cli import main

    main()
