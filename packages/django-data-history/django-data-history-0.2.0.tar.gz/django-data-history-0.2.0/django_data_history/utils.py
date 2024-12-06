#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

import json
from django.db.models.manager import BaseManager
from django.core.serializers import serialize


def post_admin_autodiscover(callback):
    from django.contrib import admin
    admin_old_autodiscover = admin.autodiscover
    def admin_new_autodiscover():
        admin_old_autodiscover()
        callback()
    admin.autodiscover = admin_new_autodiscover


def pre_admin_autodiscover(callback):
    from django.contrib import admin
    admin_old_autodiscover = admin.autodiscover
    def admin_new_autodiscover():
        callback()
        admin_old_autodiscover()
    admin.autodiscover = admin_new_autodiscover


def get_item_data(item):
    text = serialize("json", [item], use_natural_foreign_keys=True)
    info = json.loads(text)
    data = info[0]["fields"]
    data["id"] = info[0]["pk"]

    for name in item.__class__._meta.fields_map.keys():
        if "+" in name:
            continue
        if not hasattr(item, name):
            continue
        iqueryset = getattr(item, name)
        if isinstance(iqueryset, BaseManager):
            text = serialize("json", iqueryset.all(), use_natural_foreign_keys=True)
        else:
            text = serialize("json", [iqueryset], use_natural_foreign_keys=True)
        infos = json.loads(text)
        data2 = []
        for info in infos:
            data3 = info["fields"]
            data3["id"] = info["pk"]
            data2.append(data3)
        data[name] = data2

    django_data_history_excludes = getattr(item.__class__, "django_data_history_excludes", [])
    for field in django_data_history_excludes:
        if field in data:
            del data[field]

    return data
