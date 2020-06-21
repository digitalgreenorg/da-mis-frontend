# coding: utf-8
from django.conf import settings

from kpi.constants import PERM_SHARE_SUBMISSIONS, PERM_FROM_KC_ONLY
from kpi.models.geography import LocationAccess


class ObjectPermissionHelper:

    @staticmethod
    def user_can_share(affected_object, user_object, codename=''):
        """
        Return `True` if `user` is allowed to grant and revoke
        `codename` on `affected_object`. For `Collection`, this is always
        the same as checking that `user` has the
        `share_collection` permission on `affected_object`. For `Asset`,
        the result is determined by either `share_asset` or
        `share_submissions`, depending on the `codename`.

        :type affected_object: :py:class:Asset or :py:class:Collection
        :type user_object: auth.User
        :type codename: str
        :rtype bool
        """
        # affected_object can be deferred which doesn't return the expected
        # model_name. Using `concrete_model` does.
        model_name = affected_object._meta.concrete_model._meta.model_name
        if model_name == 'asset' and codename.endswith('_submissions'):
            share_permission = PERM_SHARE_SUBMISSIONS
        else:
            share_permission = 'share_{}'.format(model_name)
        return affected_object.has_perm(user_object, share_permission)

    @classmethod
    def get_user_permission_assignments_queryset(cls, affected_object, user):
        """
        Returns a queryset to fetch `affected_object`'s permission assignments
        that `user` is allowed to see.

        Args:
            affected_object (Collection|Asset)
            user (User)
        Returns:
             QuerySet

        """

        # `affected_object.permissions` is a `GenericRelation(ObjectPermission)`
        # Don't Prefetch `content_object`.
        # See `AssetPermissionAssignmentSerializer.to_representation()`
        queryset = affected_object.permissions.filter(deny=False).select_related(
            'permission', 'user'
        ).order_by(
                'user__username', 'permission__codename'
        ).exclude(permission__codename=PERM_FROM_KC_ONLY).all()

        # Filtering is done in `get_queryset` instead of FilteredBackend class
        # because it's specific to `ObjectPermission`.
        if not user or user.is_anonymous:
            queryset = queryset.filter(user_id=affected_object.owner_id)
        elif not cls.user_can_share(affected_object, user):
            # Display only users' permissions if they are not allowed to modify
            # others' permissions
            queryset = queryset.filter(user_id__in=[user.pk,
                                                    affected_object.owner_id,
                                                    settings.ANONYMOUS_USER_ID])

        return queryset

    @classmethod
    def get_user_permission_assignments(cls, affected_object, user,
                                        object_permission_assignments):
        """
        Works like `get_user_permission_assignments_queryset` but returns
        a list instead of a queryset. It also needs a list of all
        `affected_object`'s permission assignments to search for assignments
        `user` is allowed to see.

        Args:
            affected_object (Collection|Asset)
            user (User)
            object_permission_assignments (list):
        Returns:
             list

        """
        user_permission_assignments = []
        filtered_user_ids = None

        if not user or user.is_anonymous:
            filtered_user_ids = [affected_object.owner_id]
        elif not cls.user_can_share(affected_object, user):
            # Display only users' permissions if they are not allowed to modify
            # others' permissions
            filtered_user_ids = [affected_object.owner_id,
                                 user.pk,
                                 settings.ANONYMOUS_USER_ID]

        for permission_assignment in object_permission_assignments:
            if (filtered_user_ids is None or
                    permission_assignment.user_id in filtered_user_ids):
                user_permission_assignments.append(permission_assignment)

        return user_permission_assignments

    @staticmethod
    def get_location_filter(filters, user_id):
        if "query" in filters:
            query = filters["query"]
        else:
            query = {}
        location_access = LocationAccess.objects.filter(user_id=user_id)
        if len(location_access) == 0:
            return filters

        def _get_list_names(values):
            return [value.name for value in values]

        regions = _get_list_names(location_access[0].regions.all())
        zones = _get_list_names(location_access[0].zones.all())
        woredas = _get_list_names(location_access[0].woredas.all())
        kebeles = _get_list_names(location_access[0].kebeles.all())
        if len(regions) > 0 and "Region" not in query:
            query["Region"] = {"$in": regions}
        if len(zones) > 0 and "Zone" not in query:
            query["Zone"] = {"$in": zones}
        if len(woredas) > 0 and "Woreda" not in query:
            query["Woreda"] = {"$in": woredas}
        if len(kebeles) > 0 and "Kebele" not in query:
            query["Kebele"] = {"$in": kebeles}
        filters['query'] = query
        print(filters)
        return filters
