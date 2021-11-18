import os


def max_workers():
    return 2 * os.cpu_count() + 1


def with_class(class_name):
    return {"class": class_name}


def with_id(id_to_find):
    return {"id": id_to_find}
