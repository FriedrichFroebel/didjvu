# encoding=UTF-8

# Copyright © 2009-2021 Jakub Wilk <jwilk@jwilk.net>
#
# This file is part of didjvu.
#
# didjvu is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# didjvu is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.

"""
didjvu's command-line interface
"""

import argparse
import functools
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union

from didjvu import djvu_support
from didjvu import gamera_support
from didjvu import version
from didjvu import xmp


def range_int(x: int, y: int, typename: str) -> Type:
    class RangeInt(int):
        def __new__(cls, value: Union[int, str]):
            n = int(value)
            if not (x <= n <= y):
                raise ValueError
            return n

    return type(typename, (RangeInt,), {})


DPI_TYPE = range_int(djvu_support.DPI_MIN, djvu_support.DPI_MAX, 'dpi')
LOSS_LEVEL_TYPE = range_int(djvu_support.LOSS_LEVEL_MIN, djvu_support.LOSS_LEVEL_MAX, 'loss level')
SUBSAMPLE_TYPE = range_int(djvu_support.SUBSAMPLE_MIN, djvu_support.SUBSAMPLE_MAX, 'subsample')


def slice_type(max_slices: int = djvu_support.IW44_N_SLICES_MAX) -> Callable[[str], int]:
    def slices(value: str):
        result = []
        if ',' in value:
            previous_slice = 0
            for slice_value_string in value.split(','):
                slice_value = int(slice_value_string)
                if slice_value <= previous_slice:
                    raise ValueError('non-increasing slice value')
                result += [slice_value]
                previous_slice = slice_value
        elif '+' in value:
            slice_value = 0
            for slice_increase_string in value.split('+'):
                slice_increase = int(slice_increase_string)
                if slice_increase <= 0:
                    raise ValueError('non-increasing slice value')
                slice_value += slice_increase
                result += [slice_value]
        else:
            slice_value = int(value)
            if slice_value < 0:
                raise ValueError('invalid slice value')
            result = [slice_value]
        assert len(result) > 0
        if len(result) > max_slices:
            raise ValueError('too many slices')
        return result

    return slices


def get_slice_repr(lst: List[int]) -> str:
    def fold(inner_list: List[int], obj: int):
        return inner_list + [obj - sum(inner_list)]

    plus_list = functools.reduce(fold, lst[1:], lst[:1])
    return '+'.join(map(str, plus_list))


class Intact:
    def __init__(self, x: Any):
        self.x = x

    def __call__(self) -> Any:
        return self.x


def replace_underscores(s: str) -> str:
    return s.replace('_', '-')


def _get_method_parameters_help(methods: Dict[str, gamera_support.PluginFunction]) -> str:
    result = ['binarization methods and their parameters:']
    for name, method in sorted(methods.items()):
        result += ['  ' + name]
        for arg in method.args.values():
            arg_help = arg.name
            if arg.type in {int, float}:
                arg_help += '=' + 'NX'[arg.type is float]
                arg_help_paren = []
                if (arg.min is None) != (arg.max is None):
                    message = f'inconsistent limits for {name}.{arg.name}: min={arg.min}, max={arg.max}'
                    raise NotImplementedError(message)
                if arg.min is not None:
                    arg_help_paren += [f'{arg.min} .. {arg.max}']
                if arg.default is not None:
                    arg_help_paren += [f'default: {arg.default}']
                if arg_help_paren:
                    arg_help += f' ({", ".join(arg_help_paren)})'
            elif arg.type is bool:
                if arg.default is not False:
                    message = f'unexpected default value for {name}.{arg.name}: {arg.default}'
                    raise NotImplementedError(message)
            else:
                message = f'unexpected type for {name}.{arg.name}: {arg.type.__name__}'
                raise NotImplementedError(message)
            result += ['  - ' + arg_help]
    return '\n'.join(result)


class ArgumentParser(argparse.ArgumentParser):
    class Defaults:
        page_id_template = '{base-ext}.djvu'
        pages_per_dict = 1
        dpi = None
        foreground_slices = [100]
        foreground_crcb = djvu_support.CRCB.full
        foreground_subsample = 6
        background_slices = [74, 84, 90, 97]
        background_crcb = djvu_support.CRCB.normal
        background_subsample = 3

    def __init__(self, methods: Dict[str, Callable], default_method: str, prog: Optional[str] = None):
        super(ArgumentParser, self).__init__(formatter_class=argparse.RawDescriptionHelpFormatter, prog=prog)
        self.add_argument('--version', action=version.VersionAction)
        parser_separate = self.add_subparser('separate', help='generate masks for images')
        parser_encode = self.add_subparser('encode', help='convert images to single-page DjVu documents')
        parser_bundle = self.add_subparser('bundle', help='convert images to bundled multi-page DjVu document')
        epilog = []
        default = self.Defaults
        for parser in (parser_separate, parser_encode, parser_bundle):
            epilog += [f'{parser.prog} --help']
            parser.add_argument('-o', '--output', metavar='FILE', help='output filename')

            if parser is parser_bundle:
                parser.add_argument(
                    '--page-id-template', metavar='TEMPLATE', default=default.page_id_template,
                    help=f'naming scheme for page identifiers (default: "{default.page_id_template}")'
                )
            else:
                parser.add_argument(
                    '--output-template', metavar='TEMPLATE',
                    help=f'naming scheme for output file (e.g. "{default.page_id_template}")'
                )

            parser.add_argument('--losslevel', dest='loss_level', type=LOSS_LEVEL_TYPE, help=argparse.SUPPRESS)
            parser.add_argument(
                '--loss-level', dest='loss_level', type=LOSS_LEVEL_TYPE, metavar='N',
                help='aggressiveness of lossy compression'
            )
            parser.add_argument(
                '--lossless', dest='loss_level', action='store_const', const=djvu_support.LOSS_LEVEL_MIN,
                help='lossless compression (default)'
            )
            parser.add_argument(
                '--clean', dest='loss_level', action='store_const', const=djvu_support.LOSS_LEVEL_CLEAN,
                help='lossy compression: remove flyspecks'
            )
            parser.add_argument(
                '--lossy', dest='loss_level', action='store_const', const=djvu_support.LOSS_LEVEL_LOSSY,
                help='lossy compression: substitute patterns with small variations'
            )

            if parser is not parser_separate:
                parser.add_argument('--masks', nargs='+', metavar='MASK', help='use pre-generated masks')
                parser.add_argument('--mask', action='append', dest='masks', metavar='MASK', help='use a pre-generated mask')
                for layer_name, layer_id in (('foreground', 'fg'), ('background', 'bg')):
                    if layer_name == 'foreground':
                        def_slices = get_slice_repr(default.foreground_slices)
                        parser.add_argument(
                            '--fg-slices', dest='foreground_slices', type=slice_type(1), metavar='N',
                            help=f'number of slices for foreground (default: {def_slices})'
                        )
                    else:
                        def_slices = get_slice_repr(default.background_slices)
                        parser.add_argument(
                            '--bg-slices', dest='background_slices', type=slice_type(), metavar='N+...+N',
                            help=f'number of slices in each background chunk (default: {def_slices})'
                        )
                    default_crcb = getattr(default, f'{layer_name}_crcb')
                    parser.add_argument(
                        f'--{layer_id}-crcb', dest=f'{layer_name}_crcb', choices=list(map(str, djvu_support.CRCB.values)),
                        help=f'chrominance encoding for {layer_name} (default: {default_crcb})'
                    )
                    default_subsample = getattr(default, f'{layer_name}_subsample')
                    parser.add_argument(
                        f'--{layer_id}-subsample', dest=f'{layer_name}_subsample', type=SUBSAMPLE_TYPE, metavar='N',
                        help=f'subsample ratio for {layer_name} (default: {default_subsample})'
                    )
                parser.add_argument('--fg-bg-defaults', help=argparse.SUPPRESS, action='store_const', const=1)

            if parser is not parser_separate:
                parser.add_argument(
                    '-d', '--dpi', type=DPI_TYPE, metavar='N',
                    help=f'image resolution (default: {djvu_support.DPI_DEFAULT})'
                )
            if parser is parser_bundle:
                parser.add_argument(
                    '-p', '--pages-per-dict', type=int, metavar='N',
                    help=f'how many pages to compress in one pass (default: {default.pages_per_dict})'
                )
            parser.add_argument(
                '-m', '--method', choices=methods, metavar='METHOD', type=replace_underscores, default=default_method,
                help=f'binarization method (default: {default_method})'
            )
            parser.add_argument(
                '-x', '--param', action='append', dest='params', metavar='NAME[=VALUE]',
                help='binarization method parameter (can be given more than once)'
            )
            if parser is parser_encode or parser is parser_bundle:
                parser.add_argument('--xmp', action='store_true', help='create sidecar XMP metadata (experimental!)')
            parser.add_argument(
                '-v', '--verbose', dest='verbosity', action='append_const', const=None,
                help='more informational messages'
            )
            parser.add_argument(
                '-q', '--quiet', dest='verbosity', action='store_const', const=[],
                help='no informational messages'
            )
            parser.add_argument('input', metavar='IMAGE', nargs='+')
            parser.set_defaults(
                masks=[],
                fg_bg_defaults=None,
                loss_level=djvu_support.LOSS_LEVEL_MIN,
                pages_per_dict=default.pages_per_dict,
                dpi=default.dpi,
                foreground_slices=Intact(default.foreground_slices),
                background_slices=Intact(default.background_slices),
                foreground_crcb=Intact(default.foreground_crcb),
                background_crcb=Intact(default.background_crcb),
                foreground_subsample=Intact(default.foreground_subsample),
                background_subsample=Intact(default.background_subsample),
                verbosity=[None],
                xmp=False,
            )
            parser.epilog = _get_method_parameters_help(methods)
        self.epilog = 'more help:\n  ' + '\n  '.join(epilog)
        self.__methods = methods

    def add_subparser(self, name: str, **kwargs) -> argparse.ArgumentParser:
        try:
            # noinspection PyUnresolvedReferences
            self.__subparsers  # type: ignore[has-type]
        except AttributeError:
            # noinspection PyAttributeOutsideInit
            self.__subparsers = self.add_subparsers(parser_class=argparse.ArgumentParser)

        kwargs.setdefault('formatter_class', argparse.RawDescriptionHelpFormatter)
        parser = self.__subparsers.add_parser(name, **kwargs)
        parser.set_defaults(_action_=name)
        return parser

    def _parse_parameters(self, options: argparse.Namespace) -> Dict[str, Any]:
        result = dict()
        for parameter in options.params or ():
            if '=' not in parameter:
                if parameter.isdigit() and len(options.method.args) == 1:
                    [parameter_name] = options.method.args
                    parameter_value = parameter
                else:
                    parameter_name = parameter
                    parameter_value = True
            else:
                [parameter_name, parameter_value] = parameter.split('=', 1)
            parameter_name = replace_underscores(parameter_name)
            try:
                argument = options.method.args[parameter_name]
            except KeyError:
                self.error(f'invalid parameter name {parameter_name!r}')
            try:
                # noinspection PyUnboundLocalVariable
                if (parameter_value is True) and (argument.type is not bool):
                    raise ValueError
                parameter_value = argument.type(parameter_value)
            except ValueError:
                self.error(f'invalid parameter {parameter_name} value: {parameter_value!r}')
            if (argument.min is not None) and parameter_value < argument.min:
                self.error(f'parameter {parameter_name} must be >= {argument.min}')
            if (argument.max is not None) and parameter_value > argument.max:
                self.error(f'parameter {parameter_name} must be <= {argument.max}')
            result[argument.name] = parameter_value
        for argument in options.method.args.values():
            if (not argument.has_default) and (argument.name not in result):
                self.error(f'parameter {argument.name} is not set')
        return result

    # noinspection PyMethodOverriding
    def parse_arguments(self, actions: List[argparse.Action]) -> Any:
        options = argparse.ArgumentParser.parse_args(self)
        if not hasattr(options, 'fg_bg_defaults'):
            import sys
            self.print_usage()
            print('didjvu: error: too few arguments')
            sys.exit(2)
        if options.fg_bg_defaults is None:
            for layer in 'foreground', 'background':
                namespace = argparse.Namespace()
                setattr(options, f'{layer}_options', namespace)
                for facet in 'slices', 'crcb', 'subsample':
                    attribute_name = f'{layer}_{facet}'
                    value = getattr(options, attribute_name)
                    if isinstance(value, Intact):
                        value = value()
                    else:
                        options.fg_bg_defaults = False
                    setattr(namespace, facet, value)
                    delattr(options, attribute_name)
                if isinstance(namespace.crcb, str):
                    namespace.crcb = getattr(djvu_support.CRCB, namespace.crcb)
        if options.fg_bg_defaults is not False:
            options.fg_bg_defaults = True
        # noinspection PyTypeChecker
        options.verbosity = len(options.verbosity)
        if options.pages_per_dict <= 1:
            options.pages_per_dict = 1
        action = getattr(actions, vars(options).pop('_action_'))
        options.method = self.__methods[options.method]
        options.parameters = self._parse_parameters(options)
        try:
            if options.xmp and not xmp.backend:
                raise xmp.import_error  # pylint: disable=raising-bad-type
        except AttributeError:
            pass
        return action(options)


def dump_options(
        options: argparse.Namespace, multi_page: bool = False
) -> Generator[Tuple[str, Any], None, None]:
    method_name = options.method.name
    if options.params:
        method_name += ' '
        method_name += ' '.join(
            f'{parameter_name}={parameter_value}'
            for parameter_name, parameter_value
            in sorted(options.params.items())
        )
    yield 'method', method_name
    if multi_page:
        yield 'pages-per-dict', options.pages_per_dict
    yield 'loss-level', options.loss_level
    if options.fg_bg_defaults:
        yield 'fg-bg-defaults', True
    else:
        for layer_name in 'fg', 'bg':
            layer = getattr(options, f'{layer_name}_options')
            yield f'{layer_name}-crcb', str(layer.crcb)
            yield f'{layer_name}-slices', get_slice_repr(layer.slices)
            yield f'{layer_name}-subsample', layer.subsample


__all__ = ['ArgumentParser', 'dump_options']

# vim:ts=4 sts=4 sw=4 et
