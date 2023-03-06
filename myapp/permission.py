from rest_framework.permissions import BasePermission
from rest_framework import permissions

class UserCanViewOwnBlog(BasePermission):
    """
    Allows access only to the owner of the blog.
    """
    edit_methods = ("PUT", "PATCH",'DELETE')
    def has_permission(self, request, view):
        print(view.action,'****************')
        if request.user.is_authenticated:

                return True
    def has_object_permission(self, request, view, obj):
        print(obj,'+++++++++++++++++++++')
        if request.method in permissions.SAFE_METHODS:
            return True
