from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
