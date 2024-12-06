from pathlib import Path


import ast
import json
import logging
import re

from collections import defaultdict
from copy import deepcopy
from deepdiff import DeepDiff

from ruamel.yaml import YAML
from ruamel.yaml.representer import RoundTripRepresenter
from ruamel.yaml.compat import StringIO

class NonAliasingRTRepresenter(RoundTripRepresenter):
    def ignore_aliases(self, data):
        return True


class StrYaml(YAML):
    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        self.Representer = NonAliasingRTRepresenter
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()



logger = logging.getLogger()


def dict_path(d: dict, path: list = None):
    if path is None:
        path = []

    if not isinstance(d, dict) or d == dict():
        return [path]

    result = []

    for k, v in d.items():
        dp_k = dict_path(v, path + [k])
        result.extend(dp_k)

    return result


def pathlist2dict(l: list[str], value: dict | None = None) -> dict:
    current = value
    for p in l[::-1]:
        current = {p: current}
    return current


def paths_by_path_ptrns(d: dict, path: list[str] = None) -> list:
    path = path if path else list()
    result = dict_path(d)
    # apply path pattern filter
    for i, ptrn in enumerate(path):
        result = [r for r in result if len(r) > i and re.match(ptrn, r[i])]
    # trim by path pattern length
    result = [r[:len(path)] for r in result]
    
    return [list(t) for t in set([tuple(r) for r in result])]


def get_subdict_by_path(d: dict, path: list = None):
    result = d
    for p in path:
        if p in result:
            result = result[p]
        else:
            result[p] = dict()
            result = result[p]
    return result


def apply_whens(path_patterns: list[str], whens: list[When] = None, d1: dict = None, d2: dict = None) -> list[str]:
    d1 = d1 if d1 else dict()
    d2 = d2 if d2 else dict()
    path_patterns = path_patterns if path_patterns else []

    paths1 = paths_by_path_ptrns(d1, path_patterns)
    result = paths1
    banned_in_result = deepcopy(result)

    if whens:
        # d1 whens
        flag_use_banned = False
        for path in paths1:
            whens_results = list()
            subdict1 = get_subdict_by_path(d1, path)
            for when in whens:
                if when.has_children:
                    flag_use_banned = True
                    paths_with_children = paths_by_path_ptrns(subdict1, when.has_children)
                    if paths_with_children and path in banned_in_result:
                        whens_results.append(True)
                    else:
                        whens_results.append(False)
                if when.doesnt_have_chidren:
                    flag_use_banned = True
                    paths_with_children = paths_by_path_ptrns(subdict1, when.doesnt_have_chidren)
                    if not paths_with_children and path in banned_in_result:
                        whens_results.append(True)
                    else:
                        whens_results.append(False)

            if all(whens_results):
                banned_in_result.remove(path)

        if flag_use_banned:
            result = [r for r in result if r not in banned_in_result]
        banned_in_result = deepcopy(result)

        # d2 whens
        flag_use_banned = False
        for when in whens:
            if when.absent_in_destination:
                flag_use_banned = True
                paths2 = paths_by_path_ptrns(d2, path_patterns)
                paths_absent_in_d2 = [p for p in result if p not in paths2]
                for p in paths_absent_in_d2:
                    banned_in_result.remove(p)

        if flag_use_banned:
            result = [r for r in result if r not in banned_in_result]

        return result
    else:
        return result


def dump_action(action_dict: dict, path: list[str], symbol: str, color: bool = False) -> list[str]:
    if not action_dict:
        return []

    if path:
        path_dict = pathlist2dict(path)
        subpath_dict = get_subdict_by_path(path_dict, path[:-1])
        subpath_dict[path[-1]] = action_dict
    else:
        path_dict = action_dict

    yaml = StrYaml(typ=['rt'])
    e = yaml.emitter
    e.MAX_SIMPLE_KEY_LENGTH = 1024
    s = yaml.dump(path_dict).split('\n')

    s_formatted = list(map(lambda x: re.sub('^[- ] ', f"  ", x), s))
    color_end = '\033\u001b[0m' if color else ''
    s_no_nones = list(map(lambda x: re.sub(r'\:( None| \{\})?$', color_end, x), s_formatted))

    result = list()

    for i, line in enumerate([snn for snn in s_no_nones if snn]):
        if i >= len(path):
            result.append(re.sub(r'(^\s*)', r"\1" + f"{symbol} ", line))
        else:
            result.append(line)

    return result


def paths_to_dict(paths: list[tuple]) -> dict:
    result = dict()
    for path in paths:
        current = result
        for p in path:
            if p in current:
                current = current[p]
            else:
                current[p] = dict()
    return result


def indented_to_dict_clean(config: str, indent_char: str = " ", indent: int = 3, comments: list[str] = None):
    comments = comments if comments else list()
    indented_lines = []
    paths = ['!FOOBAR']
    for i, line in enumerate(config.splitlines()):
        if any(re.match(comment, line) for comment in comments):
            continue
        name = line.lstrip(indent_char).rstrip()
        level = (len(line) - len(name)) // indent
        indented_lines.append((i, level, name))
        paths.append([p for p in paths[-1][:level]] + [name])
    paths = paths[1:]

    return paths_to_dict(paths)


def indented_to_dict(
        config: str,
        indent_char: str = " ",
        indent: int = 3,
        comments: list[str] = None,
        enter_exits: list | None = None
):
    enter_exits = enter_exits if enter_exits else list()
    comments = comments if comments else list()
    indented_lines = []
    paths = ['!FOOBAR']

    enter_exit_level = 0

    for i, line in enumerate(config.splitlines()):
        if any(re.match(comment, line) for comment in comments):
            continue

        name = line.lstrip(indent_char).rstrip()
        level = (len(line) - len(name)) // indent + enter_exit_level
        indented_lines.append((i, level, name))
        paths.append([p for p in paths[-1][:level]] + [name])

        for enter_exit in enter_exits:
            if re.match(enter_exit['enter'], line):
                enter_exit_level += 1
            if re.match(enter_exit['exit'], line):
                enter_exit_level -= 1

    paths = paths[1:]

    return paths_to_dict(paths)


def remove_key_nokey(d: dict, no: str = "no "):
    keys = list(d)
    for k in keys:
        nokey = f"{no}{k}"
        if k in d and nokey in d:
            d.pop(k)
            d.pop(nokey)
    for k in list(d):
        remove_key_nokey(d[k])



class ConfigCompare:
    """
    Config Compare class reads two input files and transforms them into nested dicts.
    The dicts can be changed with the help of input filters. And then dicts are compared.
    Filters are objects of class CfgCmprFilter (filter actions examples are cp21, cp12, del1, del2, upd1,upd2).
    """
    def __init__(self, f1: str, f2: str, settings: CfgCmprSettings, filters: list[dict] = None):
        """
        1. Create cc object: read files, create d1 and d2. 
        2. Apply filters to dicts
        3. Run comparison
        """
        settings: CfgCmprSettings
        filters: list[CfgCmprFilter]

        # initial sets
        self.filters = [CfgCmprFilter(**filter) for filter in filters]
        self.settings = CfgCmprSettings(**settings)

        self.f1 = str(Path(f1).absolute())
        self.f2 = str(Path(f2).absolute())

        # files read
        with open(self.f1, 'r') as f:
            c1 = f.read()
        with open(self.f2, 'r') as f:
            c2 = f.read()
        
        # set dicts from files
        self.d1 = indented_to_dict(c1, **self.settings.model_dump(include=['indent', 'indent_char', 'comments', 'enter_exits']))
        self.d2 = indented_to_dict(c2, **self.settings.model_dump(include=['indent', 'indent_char', 'comments', 'enter_exits']))

        # set method list to help find filters
        self.method_list = [
            attribute
            for attribute in dir(self.__class__)
            if callable(getattr(self.__class__, attribute)) and attribute.startswith('__') is False
        ]

        # apply filters
        self.apply_filters()

        # apply cmd no cmd
        if self.settings.ignore_cmd_nocmd:
            remove_key_nokey(self.d1)
            remove_key_nokey(self.d2)

        # run comparison
        self.compare()

    def dump(self, quiet: bool = True, color: bool = False):
        """
        Dump diff in text form.
        """
        result = list()
        char_add = '\u001b[32m' if color else ''
        char_add += '+'
        char_del = '\u001b[31m' if color else ''
        char_del += '-'
        for k, v in self.diff_dict.items():
            lines_add = dump_action(v['add'], k, char_add, color)
            lines_del = dump_action(v['del'], k, char_del, color)
            if lines_add:
                lines_del = lines_del[len(k):]
            result.extend(lines_add + lines_del)
        if not quiet:
            print('\n'.join(result))
        return result

    def compare(self):
        """
        Compare prepared dicts using deepdiff and set diff_dict - subdicts to be added and to be removed from d2
        """
        dif = DeepDiff(self.d1, self.d2)

        dif_add = [
            tuple(ast.literal_eval(p.replace("root", "").replace('"', '').replace('][', ', ')))
            for p in dif.get('dictionary_item_added', [])
        ]
        dif_del = [
            tuple(ast.literal_eval(p.replace("root", "").replace('"', '').replace('][', ', ')))
            for p in dif.get('dictionary_item_removed', [])
        ]

        diff_dict = defaultdict(dict)

        for path in set(dif_add + dif_del):
            result_path = path[:-1]
            key = tuple(result_path)
            if not key in diff_dict:
                diff_dict[key]['add'] = dict()
                diff_dict[key]['del'] = dict()
            if path in dif_add:
                diff_dict[key]['add'][path[-1]] = get_subdict_by_path(self.d2, path)
            if path in dif_del:
                diff_dict[key]['del'][path[-1]] = get_subdict_by_path(self.d1, path)

        pass

        self.diff_dict = dict(diff_dict)


    @staticmethod
    def cp_single_path(d1: dict, d2: dict, path: list[str]) -> None:
        """
        Filter heper. Copy a path from d1 to d2.
        """
        subd1 = get_subdict_by_path(d1, path)
        subd2 = get_subdict_by_path(d2, path[:-1])
        subd2[path[-1]] = subd1
        pass

    def cp(self, d1: dict, d2: dict, path: list[str], whens: list[When]) -> None:
        """
        Filter helper. Copy from d1 to d2. d1 can be self.d1 or self.d2 and vice versa for d2.
        """
        paths_whens = apply_whens(path, whens, d1, d2)

        pass
        for p in paths_whens:
            self.cp_single_path(d1, d2, p)

    def cp21(self, filter: CfgCmprFilter):
        """
        Filter. Copy from self.d2 to self.d1.
        """
        self.cp(self.d2, self.d1, filter.path, filter.when)

    def cp12(self, filter: CfgCmprFilter):
        """
        Filter. Copy from self.d2 to self.d2.
        """
        self.cp(self.d1, self.d2, filter.path, filter.when)

    @staticmethod
    def del_path(d: dict, path: list[str], whens: list[When]):
        """
        Filter. Del path in dict.
        """
        paths_whens = apply_whens(path, whens, d)

        for p in paths_whens:
            subdict = get_subdict_by_path(d, p[:-1])
            subdict.pop(p[-1])

    def del1(self, filter: CfgCmprFilter):
        """
        Filter. Del in self.d1.
        """
        self.del_path(self.d1, filter.path, filter.when)

    def del2(self, filter: CfgCmprFilter):
        """
        Filter. Del in self.d2.
        """
        self.del_path(self.d2, filter.path, filter.when)

    @staticmethod
    def upd_path(d: dict, path: list[str], whens: list[When], data: dict):
        """
        Filter helper. Update dict at path with another dict.
        """
        paths_whens = apply_whens(path, whens, d)
        for p in paths_whens:
            subdict = get_subdict_by_path(d, p)
            subdict.update(data)

    def upd1(self, filter: CfgCmprFilter):
        """
        Filter. Update self.d1 at path with data dict.
        """
        self.upd_path(self.d1, filter.path, filter.when, dict(filter.data))

    def upd2(self, filter: CfgCmprFilter):
        """
        Filter. Update self.d2 at path with data dict.
        """
        self.upd_path(self.d2, filter.path, filter.when, dict(filter.data))


def config_compare(f1: str, f2: str, settings: dict, filters: list[dict]) -> dict:
    """
    Ansible filter. Compare two config files with filters.
    """

    # dirty hack: transform filters from AnsibleBaseYAMLObject into native python objects.
    filters = json.loads(json.dumps(filters)) if filters else list()
    settings = json.loads(json.dumps(settings))

    # init cc object
    cc = ConfigCompare(f1, f2, settings, filters)

    # return diff_dict and text diff form.
    return {'diff_dict': cc.diff_dict, 'diff_lines': cc.dump()}


class FilterModule(object):
    def filters(self):
        return {'config_compare': config_compare}


if __name__ == "__main__":

    hostname = "UD0-4e05-EBLF-1-A"
    group = 'all'

    from nogs.app.chegen.src.ansible_inventory.inventory import hostvars_from_site_settings
    all_vars = hostvars_from_site_settings({'file_ansible_inventory': 'inventory.yml'}, group=group)


    v = all_vars[hostname]
    cc = config_compare(f'tmp_diff/desired_{hostname}.cfg', f'tmp_diff/oper_{hostname}.cfg', v['cc_settings'], v['cc_filters'])

    pass