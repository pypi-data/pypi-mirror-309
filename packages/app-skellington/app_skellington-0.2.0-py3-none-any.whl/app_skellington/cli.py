import argparse
import inspect
import re
import sys

from . import app_container
from ._bootstrap import _bootstrap_logger

# If explicit fail is enabled, any command with at least one unknown
# argument will be rejected entirely. If not enabled, unknown arguments
# will be ignored.
EXPLICIT_FAIL_ON_UNKNOWN_ARGS = True


class CommandTree:
    """
    Command-line interface to hold a menu of commands. You can register
    commands (functions or methods) in a CommandTree which will generate
    a corresponding argparse.ArgumentParser (and nested SubParsers) that
    map function/method arguments into argparse Parameters. Then, you
    can translate command-line arguments into invoking the function.

    Commands must be registered before being invoked. You create nested
    SubMenu(s). If function parameters have defaults, those will be
    available for override else they use the function defaults.

    Print helpful information:

        ./scriptname -h                       # View tier-0 help and usage doc
        ./scriptname [submenu] -h             # View submenu help and usage doc
        ./scriptname [submenu] [command] -h   # View command documentation and parameters

    argparse is finicky about argument placement:

        ./scriptname
            [application arguments]
            [submenu] [submenu arguments]
            [command] [command arguments]

    For example,

        ./scriptname --option="value" [submenu] [command]

        is different than

        ./scriptname [submenu] [command] --option="value"

    in that option is being applied to the application in the first example and
    applied to the refresh_datasets command (under the nhsn command group) in
    the second. In the same way the -h, --help options print different docs
    depending on where the help option was passed.
    """

    def __init__(self):
        self.root_parser = argparse.ArgumentParser()
        self.submenu_param = None  # submenu_param is the variable name
        # of the root submenu argument, i.e. the arg
        # in root_parser which selects the submenu.
        self.entries = {}
        # NOTE(MG) Implementation note:
        # CommandTree uses only one of these internal structures (i.e. mutually exclusive),
        # 'entries' is used when there is a submenu linked to multiple commands.
        # '_cmd_tree_is_single_command' and '_single_command' instead are used
        # when the CommandTree is linked to one and only one command.
        self._cmd_tree_is_single_command = False
        self._single_command = None

    def print_tree(self):
        raise NotImplementedError

    def add_argument(self, *args, **kwargs):
        """
        Adds an argument to the root parser.
        """
        _bootstrap_logger.info(
            "adding argument to root parser: %s and %s", args, kwargs
        )
        self.root_parser.add_argument(*args, **kwargs)

    def init_submenu(self, param_name, is_required=False):
        """
        Creates a root-level submenu with no entries. SubMenu node is
        returned which can have submenus and commands attached to it.
        """
        # NOTE(MG) Fix for Python>=3.7,
        # argparse.ArgumentParser added 'required' argument.
        # Must also be written into SubMenu.create_submenu.
        func_args = {"dest": param_name, "metavar": param_name, "required": is_required}
        if sys.version_info.major == 3 and sys.version_info.minor < 7:
            if is_required:
                _bootstrap_logger.warn(
                    "Unable to enforce required submenu: Requires >= Python 3.7"
                )
            del func_args["required"]
        # END fix for Python<3.7

        # Creates an argument as a slot in the underlying argparse.
        subparsers = self.root_parser.add_subparsers(**func_args)

        submenu = SubMenu(self, subparsers, param_name)
        submenu.submenu_path = ""
        submenu.var_name = param_name

        _bootstrap_logger.info(
            "Initialized root-level submenu: Parameter = '%s'", param_name
        )
        self.entries[param_name] = submenu
        self.submenu_param = param_name

        return submenu

    def register_command(
        self, func, cmd_name=None, func_signature=None, docstring=None
    ):
        """
        When no submenu functionality is desired, this links a single
        command into underlying argparse options.
        """
        # begin copy-paste from SubMenu.register_command
        if inspect.isfunction(func):
            # print('func is function')
            pass
        elif inspect.ismethod(func):
            pass
            # print('func is method')
        else:
            raise Exception("bad value passed in for function")

        if not cmd_name:
            # safe try/except
            cmd_name = func.__name__

        if func_signature is None:
            func_signature = inspect.signature(func)

        if docstring is None:
            docstring = func.__doc__

        sig = func_signature
        params = sig.parameters

        # help is displayed next to the command in the submenu enumeration or
        # list of commands:
        HelpGenerator.generate_help_from_sig(docstring)
        # description is displayed when querying help for the specific command:
        HelpGenerator.generate_description_from_sig(docstring)
        # end copy-paste from SubMenu.register_command

        # begin copy-paste then edited from SubMenu.register_command
        # For each parameter in the function create an argparse argument in
        # the child ArgumentParser created for this menu entry:
        for key in params:
            if key == "self":
                continue
            param = params[key]

            if "=" in str(param):
                if param.default is None:
                    helptext = "default provided"
                else:
                    helptext = "default = '{}'".format(param.default)
                self.root_parser.add_argument(
                    key, help=helptext, nargs="?", default=param.default
                )
            else:
                helptext = "required"
                self.root_parser.add_argument(key, help=helptext)

        # Build the CommandEntry structure
        cmd = CommandEntry()
        cmd.argparse_node = self.root_parser
        cmd.cmd_name = cmd_name
        cmd.func_signature = sig
        # cmd.func_ref = None
        cmd.callback = func

        registered_name = cmd_name
        _bootstrap_logger.info("registered command: %s", registered_name)
        # end copy-paste then editted from SubMenu.register_command

        self._cmd_tree_is_single_command = True
        self._single_command = cmd
        self._entries = None

    def parse(self, args=None):
        if args is None:
            args = sys.argv[1:]

        try:
            # on error, prints some argparse error messages:
            pargs, unk = self.root_parser.parse_known_args(args)

            # if len(unk) > 0:
            #     _bootstrap_logger.error(
            #         'failed to interpret argument(s) or command-line switch from shell: %s',
            #         unk)

            #     if EXPLICIT_FAIL_ON_UNKNOWN_ARGS:
            #         _bootstrap_logger.warn(
            #             'failed to parse arguments: explicitly failing to be safe')
            #         return False, False

            if hasattr(pargs, "usage"):
                pass
                # print('found usage in app_skellington')

            return pargs, unk, True

        # Note: SystemExit is raised when '-h' argument is supplied.
        except SystemExit:
            return None, None, False

    def run_command(self, args=None):
        args, unk, success = self.parse(args)
        if not success:
            _bootstrap_logger.info("cli - SystemExit: Perhaps user invoked --help")
            return

        if args is False and unk is False:
            _bootstrap_logger.error("cli - Failed parsing args.")
            return False
        _bootstrap_logger.info("cli - Received args from shell: %s", args)

        args = vars(args)

        cmd = self._lookup_command(args)
        if cmd is None:
            _bootstrap_logger.critical("cli - Failed to find command.")
            return False

        return self._invoke_command(cmd, args)

    def _lookup_command(self, args):
        keys = list(args.keys())

        # In the case there is at-most one command registered in
        # the CommandTree with no SubMenu (submenu will be disabled
        # in this case):
        if self._cmd_tree_is_single_command:
            assert (
                self._cmd_tree_is_single_command is True
            ), "corrupt data structure in CommandMenu"
            assert self._entries is None, "corrupt data structure in CommandMenu"
            assert isinstance(
                self._single_command, CommandEntry
            ), "corrupt data structure in CommandMenu"
            return self._single_command

        # There is at least one submenu we need to go down:
        else:

            assert self._single_command is None, "corrupt data structure in CommandMenu"
            assert (
                self._cmd_tree_is_single_command is False
            ), "corrupt data structure in CommandMenu"

            # Key or variable name used by argparse to store the submenu options
            argparse_param = self.submenu_param  # e.g.: submenu_root
            submenu = self.entries[argparse_param]

            while True:
                if argparse_param not in keys:
                    print("root menu parameter not found in args:", argparse_param)
                    input("<broken>")

                val = args.get(argparse_param)
                _bootstrap_logger.debug(
                    "cli - argparse command is '{}' = {}".format(argparse_param, val)
                )

                lookup = submenu.entries.get(val)
                _bootstrap_logger.debug(
                    "cli - lookup, entries[{}] = {}".format(val, lookup)
                )

                # pop value
                del args[argparse_param]

                if isinstance(lookup, SubMenu):
                    submenu = lookup
                    argparse_param = submenu.var_name
                elif isinstance(lookup, CommandEntry):
                    return lookup
                    # return self._invoke_command(lookup, args)

                else:
                    raise app_container.NoCommandSpecified("No command specified.")

    def _invoke_command(self, cmd, args):
        command_to_be_invoked = cmd.callback
        func = command_to_be_invoked
        sig = cmd.func_signature
        params = sig.parameters
        params = [params[paramname] for paramname in params]
        func_args = []
        for param in params:
            if param.name in args:
                func_args.append(args[param.name])

        _bootstrap_logger.info("cli - function: %s", func)
        _bootstrap_logger.info("cli - function args: %s", func_args)
        return command_to_be_invoked(*func_args)

    def _get_subparser(self):
        return self.root_parser._subparsers._actions[1]


class SubMenu:
    def __init__(self, parent, subparsers_obj, name):
        self.parent = parent  # Reference to root CommandTree
        self.subparsers_obj = subparsers_obj
        self.name = name
        self.submenu_path = None

        self.entries = {}

    def register_command(
        self, func, cmd_name=None, func_signature=None, docstring=None
    ):
        """
        Registers a command as an entry in this submenu. Provided function is
        converted into argparse arguments and made available to the user.

        Arguments
        ---------
        func:
            Callback function which will be mapped
            to the submenu entry.

        cmd_name (optional):
            User-facing entry name. By default will be the function name.
            The user will be able to use [cmd_name] [arg, ...] to
            invoke the callback function.

        func_signature: optionally, you can pass in the
        inspect.signature(). If None, will inspect the
        incoming func. Note on internals: This is used
        to pass the function signature of the command
        function while having the callback point to a
        function partial which executes some other code.
        This hook is used to inject dependencies and then
        execute the command function.
        """
        if inspect.isfunction(func):
            pass
        elif inspect.ismethod(func):
            pass
        else:
            raise Exception("bad value passed in for function")

        if not cmd_name:
            # TODO(MG) Safer sanitation
            cmd_name = func.__name__

        if func_signature is None:
            func_signature = inspect.signature(func)

        if docstring is None:
            docstring = func.__doc__

        sig = func_signature
        params = sig.parameters

        # help is displayed next to the command in the submenu enumeration or
        # list of commands:
        help_text = HelpGenerator.generate_help_from_sig(docstring)
        # description is displayed when querying help for the specific command:
        description_text = HelpGenerator.generate_description_from_sig(docstring)

        # Entry in local argparse._SubParsersAction
        # type = ArgumentParser
        child_node = self.subparsers_obj.add_parser(
            cmd_name,  # Note: cmd_name here will be the VALUE
            # passed into the argparse arg VARIABLE NAME
            # created when the SubMenu/argparse.add_subparsers()
            # was created.
            help=help_text,
            description=description_text,
        )

        # For each paramter in the function create an argparse argument in
        # the child ArgumentParser created for this menu entry:
        for key in params:
            if key == "self":
                continue
            param = params[key]

            if "=" in str(param):
                if param.default is None:
                    helptext = "default provided"
                else:
                    helptext = "default = '{}'".format(param.default)
                child_node.add_argument(
                    key, help=helptext, nargs="?", default=param.default
                )
            else:
                helptext = "required"
                child_node.add_argument(key, help=helptext)

        # Build the CommandEntry structure
        cmd = CommandEntry()
        cmd.argparse_node = child_node
        cmd.cmd_name = cmd_name
        cmd.func_signature = sig
        # cmd.func_ref = None
        cmd.callback = func

        registered_name = "{}.{}".format(self.submenu_path, cmd_name)
        _bootstrap_logger.info("cli - registered command: %s", registered_name)
        self.entries[cmd_name] = cmd

    def create_submenu(self, var_name, cmd_entry_name=None, is_required=False):
        """
        Creates a child-submenu.

        Arguments
        ---------
        var_name:
            A code-facing argparse parameter used to store the
            value/entry chosen by the user.

        cmd_entry_name:
            A user-facing name used to select created submenu.
            If not provided, the user-facing command name defaults
            to the same name as the code-facing argparse parameter

        is_required:
            Switches if a value must be selected in the created submenu.
            If not, it's an optional positional argument.
        """
        if cmd_entry_name is None:
            cmd_entry_name = var_name

        # Create an entry in self's submenu:
        # type = ArgumentParser
        entry_node = self.subparsers_obj.add_parser(
            cmd_entry_name, help="sub-submenu help", description="sub-sub description"
        )

        # NOTE(MG) Fix for Python>=3.7,
        # argparse.ArgumentParser added 'required' argument.
        # Must also be written into CommandTree.init_submenu
        func_args = {"dest": var_name, "metavar": var_name, "required": is_required}
        if sys.version_info.major == 3 and sys.version_info.minor < 7:
            if is_required:
                _bootstrap_logger.warn(
                    "Unable to enforce required submenu: Requires >= Python 3.7"
                )
            del func_args["required"]
        # END fix for Python<3.7

        # Turn entry into a submenu of it's own:
        # type = _SubParsersAction
        subp_node = entry_node.add_subparsers(**func_args)

        submenu = SubMenu(self.parent, subp_node, cmd_entry_name)

        submenu.var_name = var_name

        submenu.submenu_path = "{}.{}".format(self.submenu_path, cmd_entry_name)
        submenu_name = submenu.submenu_path

        _bootstrap_logger.info("cli - registered submenu: %s", submenu_name)
        self.entries[cmd_entry_name] = submenu
        return submenu

    def __repr__(self):
        return "SubMenu({})<{}>".format(self.name, ",".join(["cmds"]))


class CommandEntry:
    """
    Structure for a command-entry in the CLI.

    Stores the command-subcommand names, the function signature which contains
    the original parameters of the function-to-be-invoked, a reference to the
    original function, and a callback function wrapper which, by convention,
    instantiates the necessary objects (injecting dependencies, etc.) and
    executes the original function.

    The CLI module has functionality to translate the original function
    arguments into argparse options (creating the documentation also). Similary,
    it can convert from argparse options into a function call.
    """

    def __init__(self):
        self.argparse_node = None

        self.cmd_name = None  # Don't think we need. And needs to be changed
        # from SubMenu
        self.menu_path = None
        self.func_signature = None
        self.func_ref = None
        self.callback = None

    def __repr__(self):
        return "CommandEntry<{}>".format(self.cmd_name)


class HelpGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_help_from_sig(doctext):
        """
        The 'help' text is displayed next to the command when enumerating
        the submenu commands.
        """
        if doctext is None:
            return doctext
        regex = "(.*?)[.?!]"
        match = re.match(regex, doctext, re.MULTILINE | re.DOTALL)
        if match:
            return match.group(1) + "."
        return doctext

    @staticmethod
    def generate_description_from_sig(doctext):
        """
        The 'description' paragraph is provided when the user requests help
        on a specific command.
        """
        if doctext is None:
            return doctext
        regex = "(.*?)[.?!]"
        match = re.match(regex, doctext, re.MULTILINE | re.DOTALL)
        if match:
            return match.group(1) + "."
        return doctext
