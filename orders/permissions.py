from rest_framework import permissions

class IsBuyerOrSeller(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user == obj.buyer or user == obj.link_provider.provider
    
class IsBuyer(permissions.BasePermission):
    '''Only allow access to order that you are buyer'''
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user == obj.buyer

class IsSeller(permissions.BasePermission):
    '''Only allow access to order that you are Seller'''
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user == obj.link_provider.provider
