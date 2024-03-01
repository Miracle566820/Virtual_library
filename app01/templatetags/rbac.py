#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from django.template import Library

from app01.templatetags import urls

register = Library()


@register.simple_tag
def memory_url(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的URL（替代了模板中的url）
    :param request:
    :param name:
    :return:
    """
    return urls.memory_url(request, name, *args, **kwargs)
