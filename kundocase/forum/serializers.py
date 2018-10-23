import json

from django.core import serializers
from django.http import JsonResponse


def strip_dict(d):
    obj = dict(d.get('fields', {}))
    obj['id'] = d.pop('pk')
    return obj


def CustomResponse(data):

    data_list = []

    for row in data:
        obj = {}
        if type(row) is list:
            for row2 in row:
                obj = strip_dict(row2)
        else:
            obj = strip_dict(row)

        data_list.append(obj)

    return JsonResponse(data_list, safe=False)


def serialize(obj):
    return json.loads(serializers.serialize('json', obj))
