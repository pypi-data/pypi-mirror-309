#!/usr/bin/env python
# -*- coding:utf-8 -*-
import inspect
import os
from collections.abc import Callable, Mapping, Iterable
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin

from requests import Response
from requests_toolbelt import MultipartEncoder

from . import HttpMethod, RestFul, Hooks
from ._meta import BaseFile, RestStreamMultiFile, BaseStreamFile

from ..character import StringBuilder
from ..collections import ArrayList
from ..exceptions import HttpException
from ..generic import T
from ..maps import Dictionary
from ..utils.strings import StringUtils

from ._constants import _BODY_SHOW_MAX_LEN, _Constant, _OPTIONAL_ARGS_KEYS, _HTTP_RE, _REST_FILE

__all__ = []

_UTILS_FILE = str(Path(__file__).absolute())


def _call_stack_check(*valid_functions):
    def decorate(func):
        def wrap(*args, **kwargs):
            stack_curr = inspect.stack()[0]
            if stack_curr.filename != _UTILS_FILE:
                raise Exception(f"permission denied: disable access to '_call_stack_check'")
            if valid_functions:
                stack = inspect.stack()[1]
                if stack.function in valid_functions and stack.filename == _REST_FILE:
                    result = func(*args, **kwargs)
                    return result
                raise Exception(f"permission denied: disable access to '{func.__name__}'")

        return wrap

    return decorate


@_call_stack_check("__request")
def bulk_header(content: str) -> dict:
    """
    Format the header copied from the browser
    """
    tmp = {}
    if issubclass(type(content), str):
        for line in content.strip().split("\n"):
            line = line.strip()
            is_http2_header = False
            if line.startswith(":"):
                is_http2_header = True
                line = line[1:]
            kvs = ArrayList(line.split(":", 1), str)
            if is_http2_header:
                tmp[f":{StringUtils.trip(kvs[0])}"] = StringUtils.trip(kvs[1])
            else:
                tmp[StringUtils.trip(kvs[0])] = StringUtils.trip(kvs[1])
        return tmp
    else:
        return {"content": content}


@_call_stack_check("__request")
def build_log_message(origin: StringBuilder, msg: str):
    origin.append(f"\n{msg}\n")


@_call_stack_check("__request")
def url_handler(host, api, restful):
    return urljoin(host, api).format(**restful)



@_call_stack_check("__request")
def server_desc_handler(origin: str, server_dict: dict) -> str:
    desc: str = origin
    if not desc:
        desc: str = server_dict.get("desc")
    return desc


@_call_stack_check("__request")
def api_desc_handler(default: T, server_dict: dict, api_name, key: str) -> T:
    default_: dict = default
    if not default_ and _Constant.APIS in server_dict:
        api_list: list[dict] = server_dict.get(_Constant.APIS)
        if not api_list:
            return default_
        for api in api_list:
            if isinstance(api, dict) and api.get(_Constant.API_NAME) == api_name:
                return api.get(key)
    return default_


@_call_stack_check("__request")
def api_name_handler(api_name: str) -> str:
    if isinstance(api_name, str) and api_name.strip() != "":
        return api_name
    raise RuntimeError("api name is a must")


@_call_stack_check("__request")
def optional_args_handler(api_info: dict, opts: dict) -> dict:
    optional_args: dict = Dictionary()
    api_info_: dict = api_info if issubclass(type(api_info), dict) else {}
    for key in _OPTIONAL_ARGS_KEYS:
        if key in api_info_:
            optional_args[key] = api_info_.get(key)
    if optional_args:
        for k in list(optional_args.keys())[::]:
            if not optional_args[k]:
                del optional_args[k]
    if opts:
        optional_args.update(opts)
    return optional_args


def _header_has_key(headers: dict, verify_key: str, ignore_case: bool = False) -> bool:
    if not headers:
        return False
    if ignore_case:
        tmp_verify_key = verify_key.lower()
    else:
        tmp_verify_key = verify_key
    for k in headers.keys():
        if ignore_case:
            key = k.lower()
        else:
            key = k
        if tmp_verify_key == key:
            return True
        else:
            continue
    else:
        return False


@_call_stack_check("__request")
def header_handler(all_params: dict, method: str = HttpMethod.GET.value, headers_by_rest: dict = None,
                   headers_by_req: dict = None, headers_by_opts: dict = None):
    headers_: dict = all_params.get("headers", {}) or {}
    if method == HttpMethod.POST.value or method == HttpMethod.PUT.value or method == HttpMethod.DELETE.value:
        content_type = _Constant.CONTENT_TYPE_JSON
    else:
        content_type = _Constant.CONTENT_TYPE_DEFAULT

    if not headers_:
        headers_[_Constant.CONTENT_TYPE] = content_type
    else:
        if not _header_has_key(headers_, _Constant.CONTENT_TYPE, True):
            headers_[_Constant.CONTENT_TYPE] = content_type
    headers_.update(headers_by_rest)
    if issubclass(type(headers_by_req), dict):
        headers_.update(headers_by_req)
    if issubclass(type(headers_by_opts), dict):
        headers_.update(headers_by_opts)
    if all_params.get(_Constant.FILES):
        del headers_[_Constant.CONTENT_TYPE]
    tmp = all_params.get(_Constant.HEADERS, {})
    tmp.update(headers_)
    all_params[_Constant.HEADERS] = tmp


def cookies_handler(req, rest_cookies, opts_cookies):
    cookie = req.get(_Constant.COOKIES, {})
    if isinstance(opts_cookies, dict):
        cookie.update(opts_cookies)
    else:
        if isinstance(rest_cookies, dict):
            cookie.update(rest_cookies)
    req[_Constant.COOKIES] = cookie


@_call_stack_check("__request")
def api_handler(server_dict: dict, api_name) -> T:
    if "apis" in server_dict:
        api_list: list[dict] = server_dict.get("apis")
        if issubclass(type(api_list), list):
            for api in api_list:
                if isinstance(api, dict) and api.get("apiName") == api_name:
                    return api
    return {}


@_call_stack_check("__request")
def http_method_handler(method: HttpMethod or str) -> str:
    if isinstance(method, HttpMethod):
        return method.value
    elif isinstance(method, str):
        return HttpMethod.get_by_value(method, HttpMethod.GET).value
    else:
        return HttpMethod.GET.value


@_call_stack_check("__request")
def server_name_handler(rest_server_name: str, server_name: str, func: callable) -> str or None:
    if isinstance(server_name, str) and server_name.strip() != "":
        return server_name
    if isinstance(rest_server_name, str) and rest_server_name.strip() != "":
        return rest_server_name
    if isinstance(func, Callable):
        return func.__qualname__.split(".")[0]
    return None


@_call_stack_check("__request")
def host_handler(rest_host: str, host: str, server_dict: dict) -> str:
    host_: str = host
    if not host_:
        host_: str = rest_host
    if not host_:
        host_: str = server_dict.get(_Constant.SERVER_HOST)
    if not _HTTP_RE.match(host_):
        raise RuntimeError(f"invalid host: {host_}")
    return host_


@_call_stack_check("__request", "__initialize")
def get_show_len(rest_len, method_show_len, opts_show_len):
    if isinstance(opts_show_len, int) and opts_show_len >= 0:
        return opts_show_len
    if isinstance(method_show_len, int) and method_show_len >= 0:
        return method_show_len
    if isinstance(rest_len, int) and rest_len >= 0:
        return rest_len
    return _BODY_SHOW_MAX_LEN


@_call_stack_check("__request")
def restful_handler(rest_restful, restful, func_restful_args, kwargs_restful) -> dict:
    rest_ful = RestFul()
    rest_ful.update(rest_restful)
    rest_ful.update(restful)
    rest_ful.update(func_restful_args or {})
    rest_ful.update(kwargs_restful or {})
    return rest_ful.to_dict()


@_call_stack_check("__request")
def server_dict_handler(rest_server: dict, rest_server_list: list, name: str) -> dict:
    if name in rest_server:
        return rest_server.get(name)
    if rest_server_list and isinstance(rest_server_list, Iterable):
        for server in rest_server_list:
            if server.get(_Constant.SERVER_NAME) == name:
                rest_server[name] = server
                return server
    return {}


@_call_stack_check("__request")
def files_handler(req):
    def meta_handler(k, meta):
        ft = None
        fh = None
        if isinstance(meta, (tuple, list)):
            if len(meta) == 2:
                fn, fp = meta
            elif len(meta) == 3:
                fn, fp, ft = meta
            else:
                fn, fp, ft, fh = meta
        else:
            name = getattr(meta, 'name', None)
            if (name and isinstance(name, (str, bytes)) and name[0] != '<' and
                    name[-1] != '>'):
                fn = os.path.basename(name)
            else:
                fn = k
            fp = meta
        if isinstance(fn, Path):
            fn = str(fn)
        if isinstance(fp, Path):
            fp = str(fp)
        return key, (fn, fp, ft, fh)

    files = req.get(_Constant.FILES, None)
    if not files:
        return
    new_files = []
    if isinstance(files, BaseStreamFile):
        parts = files.build_encoder()
        data = req.get(_Constant.DATA, {})
        files.set_rest_data(data)
        req[_Constant.DATA] = parts.data
        headers = req.get(_Constant.HEADERS, {})
        headers.update({_Constant.CONTENT_TYPE: parts.content_type})
        req[_Constant.HEADERS] = headers
        del req[_Constant.FILES]
    else:
        if isinstance(files, BaseFile):
            new_files.append(files.build())
        elif isinstance(files, Mapping):
            for key, value in files.items():
                new_files.append(meta_handler(key, value))
        elif isinstance(files, (list, set)):
            for key, value in files:
                new_files.append(meta_handler(key, value))
        else:
            raise ValueError(f"'{files}' not a valid files arguments.")
        req[_Constant.FILES] = new_files


@_call_stack_check("__request")
def run_before_hooks(instance_hooks, method_hooks, opts_hooks, req):
    if isinstance(opts_hooks, Hooks):
        req = _run_hooks(opts_hooks.before_hooks, req)
    if isinstance(method_hooks, Hooks):
        req = _run_hooks(method_hooks.before_hooks, req)
    if isinstance(instance_hooks, Hooks):
        req = _run_hooks(instance_hooks.before_hooks, req)
    return req


@_call_stack_check("__request")
def run_after_hooks(instance_hooks, method_hooks, opts_hooks, resp):
    if isinstance(opts_hooks, Hooks):
        resp = _run_hooks(opts_hooks.after_hooks, resp)
    if isinstance(method_hooks, Hooks):
        resp = _run_hooks(method_hooks.after_hooks, resp)
    if isinstance(instance_hooks, Hooks):
        resp = _run_hooks(instance_hooks.after_hooks, resp)
    return resp


def _run_hooks(hooks, args):
    hooks.sort()
    for hook in hooks:
        _args = hook.run(args)
        if _args is not None:
            args = _args
    return args


@_call_stack_check("__request")
def action(session, http_method: str, url: str, **kwargs) -> (Response, datetime, datetime):
    if "hooks" in kwargs:
        del kwargs['hooks']
    kwargs["url"] = url
    _action = getattr(session, http_method, None)
    if action:
        try:
            start_time = datetime.now()
            resp = _action(**kwargs)
            end_time = datetime.now()
            return resp, start_time, end_time
        except BaseException as e:
            raise HttpException(f"http request happened exception: {str(e)}", e)
    else:
        raise HttpException(f"unknown http method '{http_method}'")


@_call_stack_check("__initialize")
def list_to_dict(form_array, to_map):
    for element in form_array:
        server_name = element.get('name', None)
        if server_name is None:
            raise KeyError(f"'{element}' server name is None.")
        if server_name in to_map:
            raise KeyError(f"duplicate key '{server_name}'.")
        to_map[server_name] = element
    return to_map
