#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from collections.abc import Iterable
from urllib.parse import urlparse
from openpyxl.workbook import Workbook

__all__ = []


class UrlMeta:
    """
    url metadata
    """

    def __init__(self, url, method):
        self.__url = urlparse(url)
        self.__host = f"{self.__url.scheme}://{self.__url.netloc}"
        if self.__host == "://":
            self.__host = ""
        self.__netloc = self.__url.netloc
        self.__protocol = self.__url.scheme
        self.__port = self.__url.port or ""
        self.__path = self.__url.path
        self.__method = method
        self.__count: int = 1

    @property
    def protocol(self):
        return self.__protocol

    @property
    def host(self):
        return self.__host

    @property
    def path(self):
        return self.__path

    @property
    def port(self):
        return self.__port

    @property
    def method(self):
        """
        http method.
        :return:
        """
        return self.__method

    @property
    def count(self) -> int:
        """
        request send count.
        """
        return self.__count

    def __eq__(self, other: 'UrlMeta'):
        result = self.__method == other.__method and self.__protocol == other.__protocol \
                 and self.__netloc == other.__netloc and self.__port == other.__port \
                 and self.__path == other.__path
        if result is True:
            self.__count += 1
        return result

    def __hash__(self):
        return hash(f"{self.__method}:{self.__protocol}{self.__netloc}{self.__port}{self.__path}")

    def __str__(self):
        return str({"method": self.method, "count": self.count, "url": f"{self.host}{self.path}", "path": self.path})

    def __repr__(self):
        return self.__str__()


class StatsUrlHostView:
    """
    url path statistics are performed in the host dimension
    like
    """

    def __init__(self, host):
        self.__host = host
        self.__paths: set[str] = set()
        self.__urls: set[UrlMeta] = set()

    @property
    def paths(self) -> list[str]:
        return list(self.__paths)

    @property
    def urls(self) -> list[UrlMeta]:
        return list(self.__urls)

    @property
    def host(self) -> str:
        return self.__host

    def add(self, *paths: UrlMeta):
        for p in paths:
            if p.host == self.__host:
                self.__paths.add(p.path)
                self.__urls.add(p)

    def path_numbers(self) -> int:
        return len(self.__paths)

    def __str__(self):
        return str({self.__host: {"paths": self.__paths, "urlMeta": self.__urls}})

    def __repr__(self):
        return self.__str__()


class StatsSentUrl:
    """
    statistics the URLs that have been sent.
    get_url_stats return a dict like {'host2': StatsUrlHostView, 'host2': StatsUrlHostView}
    """

    def __init__(self):
        self.__urls_stats: dict[str, StatsUrlHostView] = {}

    def __str__(self):
        return str(self.__urls_stats)

    def __repr__(self):
        return self.__str__()

    def add(self, *reqs: tuple[str, str]):
        for url, method in reqs:
            meta = UrlMeta(url, method)
            if meta.host not in self.__urls_stats:
                self.__urls_stats[meta.host] = StatsUrlHostView(meta.host)
            self.__urls_stats[meta.host].add(meta)

    @property
    def urls_stats(self) -> dict[str, StatsUrlHostView]:
        return self.__urls_stats

    def get_url_stats_by_host(self, host) -> StatsUrlHostView:
        return self.__urls_stats.get(host)


def aggregation(context, stats_do: bool = False) -> dict[str, StatsUrlHostView]:
    """
    Aggregate all REST request data
    :param context: rest context.
    :param stats_do: collect the interfaces assembled in the rest wrapper,
                    the interfaces should not be used at this time, and will still be counted.
    return struct
    {'https://localhost:8080':
        {'https://localhost:8080':
            {'paths': {'/hello1', '/hello'},
             'urlMeta': {
                         {'method': 'POST', 'count': 2, 'url': 'https://localhost:8080/hello1', 'path': '/hello1'},
                         {'method': 'GET', 'count': 2, 'url': 'https://localhost:8080/hello', 'path': '/hello'}
                        }
            }
        }
    }
    """
    stats_sent_urls: dict[str, StatsUrlHostView] = {}
    for bean in context.beans.values():
        if stats_do is True:
            views = [wrapper.api_stats_do for wrapper in bean.wrappers.values()]
        else:
            views = [bean.rest.api_stats_done]
        for view in views:
            for k, v in view.urls_stats.items():
                if k not in stats_sent_urls:
                    stats_sent_urls[k] = StatsUrlHostView(k)
                stats_sent_urls[k].add(*v.urls)
    return stats_sent_urls


def export(context, file_name, file_type="json", stats_do: bool = False):
    """
    export rest host and apis.
    :param context: rest context.
    :param file_name: export file name or path.
    :param file_type: export type. support json and xlsx. default type is json.
    :param stats_do: collect the interfaces assembled in the rest wrapper,
                    the interfaces should not be used at this time, and will still be counted.
    :return:
    """

    def out_json(data, path):
        with open(path, "wb") as f:
            f.write(json.dumps(data, indent=4).encode("utf-8"))

    class Excel:
        __xlsx_head = {"A": "host", "B": "api", "C": "method", "D": "url"}

        def __init__(self):
            self.__wb = Workbook()
            self.__ws = self.__wb.active
            self.__ws.append(list(self.__xlsx_head.values()))
            for k in self.__xlsx_head.keys():
                attr_name = f"_{self.__class__.__name__}__col_{k.lower()}_max_dimensions"
                setattr(self, attr_name, 0)

        def __cal(self, **kwargs):
            for k, v in self.__xlsx_head.items():
                if v in kwargs:
                    attr_name = f"_{self.__class__.__name__}__col_{k.lower()}_max_dimensions"
                    if (v_len := len(kwargs.get(v))) > getattr(self, attr_name):
                        setattr(self, attr_name, v_len)

        def __set_column_dimensions(self):
            for k in self.__xlsx_head.keys():
                name = f"_{self.__class__.__name__}__col_{k.lower()}_max_dimensions"
                self.__ws.column_dimensions[k].width = int(getattr(self, name) + 4)

        def add(self, **kwargs):
            self.__cal(**kwargs)
            self.__ws.append(list(kwargs.values()))

        def save(self, path):
            self.__set_column_dimensions()
            self.__wb.save(str(path))

    def out_excel(data, path):
        excel = Excel()
        for server, infos in data.items():
            for info in infos:
                excel.add(host=server, api=info['api'], method=info['method'], url=info['url'])
        excel.save(path)

    stats_sent_urls: dict[str, StatsUrlHostView] = aggregation(context, stats_do=stats_do)
    new_stats_sent_urls = {}
    if isinstance(file_type, str) and file_type.lower() not in ['json', "xlsx"]:
        raise TypeError(f"not support file type: {file_type}")
    for view in stats_sent_urls.values():
        http_metas = []

        for meta in view.urls:
            http_meta = {"method": meta.method, "api": meta.path, "url": f"{view.host}{meta.path}"}
            http_metas.append(http_meta)
        new_stats_sent_urls[view.host] = http_metas
    if file_type == "json":
        out_json(new_stats_sent_urls, file_name)
    elif file_type == "xlsx":
        out_excel(new_stats_sent_urls, file_name)
    return new_stats_sent_urls
