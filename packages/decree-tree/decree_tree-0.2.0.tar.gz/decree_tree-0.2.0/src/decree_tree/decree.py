"""The basic single-level command."""

import argparse
from typing import Any, ClassVar, Sequence
from .base import SubParsersType


class Decree:
    """A class for creating a command using ``argparse``."""

    #: short help text to use (allows __doc__ to be lengthy)
    help: ClassVar[str] = ''

    #: the name of the command, if not snake-cased class name
    name: str = ''

    def __init__(self, *,
                 name: str | None = None,
                 prog_is_name: bool = False,
                 version: str | None = None) -> None:
        """
        Configure variables that change during execution.

        :param name: the command name, if overriding it for the instance
        :param prog_is_name: whether to use ``self.name`` as the program name in help
        :param version: version information to display
        """
        super().__init__()

        #: the set of argparse-processed options to be used
        self.options: argparse.Namespace = argparse.Namespace()

        #: override the name for the instance
        if name == '':
            raise ValueError("Expected non-empty name argument, if any")
        if name is not None:
            self.name: str = name

        #: whether to use the ``name`` as the ``prog``, for help
        self.prog_is_name: bool = prog_is_name

        #: version information; use ``--version`` to show
        self.version: str | None = version

        #: the parser for this object
        self._decree_parser: argparse.ArgumentParser
        # Not initializing this to None in __init__ to avoid having to check for None
        # to satisfy typing, and using a dummy ArgumentParser seems unnecessary.

    def __init_subclass__(cls, **kwargs: Any) -> None:
        r"""
        Configure/override special class variables.

        :param \**kwargs: any keyword arguments needed for subclass customization
        """
        super().__init_subclass__(**kwargs)
        snake_cased_class_name = ''.join(
            '_' + c.lower() if c.isupper() else c for c in cls.__name__
        ).lstrip('_')
        cls.name = vars(cls).get(
            'name', getattr(cls, 'name', snake_cased_class_name) or snake_cased_class_name
        )
        cls.help = vars(cls).get(
            'help', cls.__doc__ or getattr(cls, 'help', '')
        )  # intentionally defaulting to '' rather than None

    def __repr__(self) -> str:
        class_path = f'{self.__class__.__module__}.{self.__class__.__qualname__}'
        kwargs: dict[str, str | bool | None] = {}
        if self.name != self.__class__.name:
            kwargs['name'] = self.name
        if self.prog_is_name is not False:
            kwargs['prog_is_name'] = self.prog_is_name
        if self.version is not None:
            kwargs['version'] = self.version
        kwarg_list = ', '.join(f'{k}={v!r}' for k, v in kwargs.items())
        return f"{class_path}({kwarg_list})"

    def __str__(self) -> str:
        return self.name  # not showing prog for root

    def configure_parser(self, subparsers: SubParsersType | None = None) -> None:
        """
        Configure the parser for this object. Typically not called by
        nor overridden in end-user code.

        :param subparsers: the subparsers object from a parent, if any
        :raises ValueError: when the configuration of the name or prog is incorrect
        """
        if subparsers:  # self is a subcommand
            # There isn't a built-in way for Decree alone to execute this directly
            if not self.name:
                raise ValueError("Expected non-empty name")
            subparser_options: dict[str, Any] = {
                'help': self.help,
                'description': self.__doc__,
                'allow_abbrev': False,
            }
            subparser_options |= self.parser_options()
            self._decree_parser = subparsers.add_parser(self.name, **subparser_options)
        else:  # self is the root command, no ``help`` argument
            parser_options: dict[str, Any] = {
                'description': self.__doc__,
                'allow_abbrev': False,
            }
            if self.prog_is_name:
                parser_options['prog'] = self.name
            parser_options |= self.parser_options()
            self._decree_parser = argparse.ArgumentParser(**parser_options)

    def parser_options(self) -> dict[str, Any]:
        """
        Add to and override options passed to the argparse parser.

        :returns: the options to provide to the parser
        """
        return {}

    def run(self,
            argv: Sequence[str] | None = None,
            options: argparse.Namespace | None = None) -> Any:
        """
        Run the command by itself via command line or with defined arguments.

        :param argv: command-line arguments to parse
        :param options: processed arguments, circumventing parse_args if specified
        :returns: the results, to facilitate testing
        """
        if not hasattr(self, '_decree_parser'):
            self.configure_parser()
        self.add_arguments(self._decree_parser)
        self.preprocess_options(argv, options)
        self.process_options()
        return self.execute()

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add arguments to ``parser`` (not ``self._decree_parser``), if any.
        Subclass overrides typically include a call to ``super().add_arguments(parser)``.
        Handle manual argument processing in ``process_options``, not here.

        :param parser: the parser to which arguments will be added
        """
        if self.version:
            parser.add_argument('--version', action='version',
                                version=f'%(prog)s {self.version}')

    def preprocess_options(self,
                           argv: Sequence[str] | None = None,
                           options: argparse.Namespace | None = None) -> None:
        """
        Populate ``self.options`` if it isn't already. Typically not called by
        nor overridden in end-user code.

        :param argv: command-line arguments to parse
        :param options: processed arguments, circumventing parse_args if specified
        """
        if options:
            for key, value in vars(options).items():
                # Keep self.options as the same object
                setattr(self.options, key, value)
        elif self.options == argparse.Namespace():
            if isinstance(argv, str):
                # Allow processing a string with all arguments
                argv = argv.split()
            self._decree_parser.parse_args(argv, self.options)
        # Otherwise, use whatever is in ``self.options`` already

    def process_options(self) -> None:
        """
        Perform any needed processing on the options, prior to execution.
        Subclass overrides typically include a call to ``super().process_options()``.
        """

    def execute(self) -> Any:
        """
        Execute [sub]command processing.
        Subclass overrides typically include a call to ``super().execute()``.

        :returns: any required data
        """
