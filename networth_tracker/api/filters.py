# networth_tracker/api/filters.py

from rest_framework import filters


class UserFilterBackend(filters.BaseFilterBackend):
    """
    Custom filter backend to filter objects based on the requesting user.
    """

    def get_queryset(self, request, queryset, view):
        """
        This method filters the queryset based on the requesting user.
        If the user is not an admin or a superuser, only objects
        owned by the user will be returned.
        """

        if not request.user.is_superuser or not request.user.is_staff:
            return queryset.filter(user=request.user)
        return queryset

    def filter_queryset(self, request, queryset, view):
        """
        This method is required by BaseFilterBackend.
        We call the get_queryset method to perform filtering
        and return the filtered queryset.
        """

        return self.get_queryset(request, queryset, view)
