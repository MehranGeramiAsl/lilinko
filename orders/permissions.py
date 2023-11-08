from rest_framework import permissions

class IsBuyerOrSeller(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user == obj.buyer or user == obj.seller
