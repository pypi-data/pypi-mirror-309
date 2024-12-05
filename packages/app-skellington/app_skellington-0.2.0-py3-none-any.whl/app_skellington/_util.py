from __future__ import print_function

import inspect
import os
import sys


def eprint(*args, **kwargs):
    """
    Print to STDERR stream.
    """
    print(*args, file=sys.stderr, **kwargs)


def filename_to_abspath(filename):
    """
    Converts a filename to it's absolute path. If it's already an
    absolute path, do nothing.
    """
    return os.path.abspath(filename)


def does_file_exist(filepath):
    """
    Because the file can be deleted or created immediately after execution of
    this function, there cannot be guarantees made around the existence of
    said file (race condition). This merely says if the file existed at this
    instant in execution.
    """
    try:
        open(filepath, "r")
        return True
    except FileNotFoundError:
        return False


def ensure_dir_exists(dirpath):
    if dirpath is None:
        return
    if dirpath == "":
        return
    os.makedirs(dirpath, exist_ok=True)


def get_root_asset(filepath):
    """
    Attempts to locate a resource or asset shipped with the application.
    Searches starting at the root module (__main__) which should be the
    python file initially invoked.
    """
    module_root = os.path.abspath(os.path.dirname(sys.modules["__main__"].__file__))
    path = os.path.join(module_root, filepath)
    return path


def get_asset(module, filepath):
    """
    Attempts to locate a resource or asset shipped with the application.
    Input filename is relative to the caller code, i.e. this starts
    searching relative to the file that called this function.

    Returns the full absolute path of the located file if found or None

    Args:
        module: Pass in the module (or __name__) to search relative to module
        filepath: the relative filepath of the file to look for in the
            package directory.
    """
    # NOTE(MG) setuptools suggests using pkg_resources ResourceManager API
    # to perform this.
    # import pkg_resources
    # my_data = pkg_resources.resource_string(__name__, "foo.dat")
    # https://setuptools.readthedocs.io/en/latest/pkg_resources.html#resourcemanager-api

    if isinstance(module, str):
        module_file = sys.modules[module].__file__
    elif isinstance(module, module):
        module_file = module.__file__
    else:
        raise Exception("Invalid Usage")

    try:
        root = module_file

        if os.path.islink(root):
            root = os.path.realpath(root)

        root = os.path.dirname(os.path.abspath(root))
    except Exception:
        raise

    path = os.path.join(root, filepath)
    return path


def register_class_as_commands(app, submenu, cls_object):
    """
    Registers commands for each class method. e.g.: pass in the CLI
    object, the target submenu, and the class to be registered, and
    this will create a command-line menu item for each method in
    the class.

    IMPORTANT: Currently, you need to pass in only a class and not
    an object/instance of a class.
    """
    cls_constructor = cls_object
    members = inspect.getmembers(cls_object)
    for m in members:
        name = m[0]
        ref = m[1]
        if inspect.isfunction(ref) and not name.startswith("_"):
            cls_method = ref
            constructor = app._inject_service_dependencies(cls_constructor)
            sig = inspect.signature(cls_method)
            func = create_func(constructor, cls_method)
            # docstring = cls_method.__doc__
            docstring = inspect.getdoc(cls_method)
            submenu.register_command(func, name, sig, docstring)


def create_func(constructor, cls_method):
    def func(*args, **kwargs):
        cmd_class_instance = constructor()
        return cls_method(cmd_class_instance, *args, **kwargs)

    return func
