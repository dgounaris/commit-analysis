import argparse
import logging
import os
import sys

logger = logging.getLogger('commit-analysis')

# borrowed as a resolution from https://github.com/pre-commit/pre-commit/issues/217
os.environ.pop('__PYVENV_LAUNCHER__', None)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
