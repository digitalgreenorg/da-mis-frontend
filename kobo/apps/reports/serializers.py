# coding: utf-8
from rest_framework import serializers
from rest_framework.reverse import reverse

from kobo.apps.reports import report_data


class ReportsListSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        request = self.context['request']
        return {
            'url': reverse('reports-detail', args=(obj.uid,), request=request),
        }


class ReportsDetailSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        request = self.context['request']
        if 'names' in request.query_params:
            vnames = filter(lambda x: len(x) > 1,
                            request.query_params.get('names', '').split(','))
        else:
            vnames = None
        
        filters = {}
        if 'query' in request.query_params:
            filters['query'] = request.query_params['query']
            
        split_by = request.query_params.get('split_by', None)
        submission_stream = obj.deployment.get_submissions(request.user.id, **filters)

        vnames_by_gender = ['Gender', 'Graduation']
        vnames = ['Education_Level']
        _list_by_gender = report_data.data_by_identifiers(obj, vnames_by_gender, split_by='Specialization',
                                                submission_stream=submission_stream)

        submission_stream = obj.deployment.get_submissions(request.user.id, **filters)
        _list = report_data.data_by_identifiers(obj, vnames, split_by=split_by,
                                                submission_stream=submission_stream)
        
        

        return {
            'url': reverse('reports-detail', args=(obj.uid,), request=request),
            'count': len(_list_by_gender+_list),
            'list': _list_by_gender+_list,
        }
