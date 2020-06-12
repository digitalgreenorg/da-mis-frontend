# coding: utf-8
from rest_framework import serializers
from rest_framework.reverse import reverse

from kobo.apps.reports import report_data
from datetime import datetime

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

        def dateFromString(param):
            return {
            '$dateFromString': {
                'dateString': param,
                # 'format': '%Y-%m-%d'
            }
        }

        aggregate_pipeline = [
            {
                '$addFields': {
                    'age': {
                        '$floor': {
                            '$add': [ {
                                '$divide': [{'$subtract': [datetime.now(), dateFromString('$Date_of_Birth')]}, (365 * 24*60*60*1000)]
                            }, 0.5]
                        } 
                    },
                    'year_since_graduation': {
                        '$floor': {
                            '$add': [ {
                                '$divide': [{'$subtract': [datetime.now(), dateFromString('$Graduation')]}, (365 * 24*60*60*1000)]
                            }, 0.5]
                        } 
                    },
                }
            }
        ]
        
        submission_stream = obj.deployment.get_submissions(request.user.id, aggregate_pipeline=aggregate_pipeline, **filters)
        

        vnames_by_specialization = ['Gender']
        vnames = ['Education_Level', 'tenure']
        _list_by_specialization = report_data.data_by_identifiers(obj, vnames_by_specialization, split_by='Specialization',
                                                submission_stream=submission_stream)

        vnames_by_gender = ['year_since_graduation']
        submission_stream = obj.deployment.get_submissions(request.user.id, **filters)
        _list_by_gender = report_data.data_by_identifiers(obj, vnames_by_gender, split_by='Gender',
                                                submission_stream=submission_stream)
        

        aggregate_pipeline = [
            {
                '$addFields': {
                    'months_in_kebele': {
                        '$divide': [{'$subtract': [datetime.now(), dateFromString('$Employment_Date_in_Kebele')]}, (30 * 24*60*60*1000)]
                    },
                },
            },
            {
                '$addFields': {
                    'tenure': {
                        '$switch': {
                            'branches': [
                                # {
                                #     'case': {'$eq': ["$months_in_kebele", None]},
                                #     'then': ""
                                # },
                                {
                                    'case': {'$and': [ { '$gte' : ["$months_in_kebele", 0]}, { '$lt' : ["$months_in_kebele", 6]}]}, 
                                    'then': "0 to 6 months"
                                },
                                {
                                    'case': {'$and': [ { '$gte' : ["$months_in_kebele", 6]}, { '$lt' : ["$months_in_kebele", 12]}]},
                                    'then': "6 to 12 months"
                                },
                                {
                                    'case': {'$and': [ { '$gte' : ["$months_in_kebele", 12]}, { '$lt' : ["$months_in_kebele", 24]}]},
                                    'then': "12 to 24 months"
                                },
                                {
                                    'case': {'$and': [ { '$gte' : ["$months_in_kebele", 24]}, { '$lt' : ["$months_in_kebele", 36]}]},
                                    'then': "24 to 36 months"
                                },
                            ],
                            'default': "+ 36 months"
                        }
                    }
                }
            }
        ]   
        submission_stream = obj.deployment.get_submissions(request.user.id, aggregate_pipeline=aggregate_pipeline, **filters)
        # print(list(submission_stream))
        # submission_stream = obj.deployment.get_submissions(request.user.id, **filters)
        _list = report_data.data_by_identifiers(obj, vnames, split_by=split_by,
                                                submission_stream=submission_stream)
        
        

        return {
            'url': reverse('reports-detail', args=(obj.uid,), request=request),
            'count': len(_list_by_specialization)+len(_list)+len(_list_by_gender),
            'list': _list_by_specialization+_list+_list_by_gender,
        }
