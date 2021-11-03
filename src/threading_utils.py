import os


def max_workers():
    return 2 * os.cpu_count() + 1
