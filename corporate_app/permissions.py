from rest_framework import permissions
from .models import *
import jwt


class AdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.is_staff)
        return request.method == "GET" or admin_permission


def permissions_list(request):


        user = User.objects.get(id=request.user.id)
        roleperms = RolePermission.objects.filter(role=user.role)
        perms = [i.permission.name for i in roleperms]
        return perms


class RoleCreatePermission:
    def has_permission(self, request, view):
        perms = permissions_list(request)

        if 'all' in perms or 'role.create' in perms:
            return True
        
        return False

class RoleReadPermission:
    def has_permission(self, request, view):
        perms = permissions_list(request)
        if 'all' in perms or 'role.read' in perms:
            return True
        return False

# class IsSuperAdmin:
#     def has_permission(self, request, view):
#         perms = permissions_list(request)
#         if 'all' in perms:
#             return True
#         return False


class RoleUpdatePermisson:
    def has_permission(self, request, view):
        perms = permissions_list(request)
        if 'all' in perms or 'role.update' in perms:
            return True
        return False


class PermissionReadPermission:
    def has_permission(self, request, view):
        perms = permissions_list(request)
        if 'all' in perms or 'permission.read' in perms:
            return True
        return False


class RoleDeletePermission:

    def has_permission(self, request, view):
        perms = permissions_list(request)
        if 'all' in perms or 'role.delete' in perms:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        perms = permissions_list(request)
        if 'all' in perms or 'role.delete' in perms:
            return True
        return False


class TaskReadPermission:
    def has_permission(self, request, view):
        perms = permissions_list(request)
        if 'all' in perms or 'task.read' in perms:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        perms = permissions_list(request)
        if 'all' in perms or 'task.read' in perms:
            return True
        return False

class TaskCreatePermission:
    def has_permission(self, request, view):
        perms = permissions_list(request)
        if 'all' in perms or 'task.create' in perms:
            return True
        return False



class TaskUpdatePermission:
    def has_permission(self, request, view):
        perms = permissions_list(request)
        if 'all' in perms or 'task.update' in perms:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        perms = permissions_list(request)
        if 'all' in perms or 'task.update' in perms:
            return True
        return False


class TaskDeletePermission:
    def has_permission(self, request, view):
        perms = permissions_list(request)
        if 'all' in perms or 'task.delete' in perms:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        perms = permissions_list(request)
        if 'all' in perms or 'task.delete' in perms:
            return True
        return False

class FolderReadPermission:

    def has_permission(self, request, view):
        perms = permissions_list(request)
        if 'all' in perms or ('folder.read' in perms and 'file.read' in perms):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        perms = permissions_list(request)
        if 'all' in perms or ('folder.read' in perms and 'file.read' in perms):
            return True
        return False


class FolderCreatePermission:

    def has_permission(self, request, view):
        perms = permissions_list(request)
        if 'all' in perms or 'folder.create' in perms:
            return True
        return False


class FolderUpdatePermission:

    def has_permission(self, request, view):
        perms = permissions_list(request)
        if 'all' in perms or 'folder.update' in perms:
            return True
        return False


class FolderDeletePermission:

    def has_permission(self, request, view):
        perms = permissions_list(request)
        if 'all' in perms or 'folder.delete' in perms:
            return True
        return False


class FileCreatePermission:

    def has_permission(self, request, view):
        perms = permissions_list(request)
        if 'all' in perms or 'file.create' in perms:
            return True
        return False


class FileReadPermission:

    def has_permission(self, request, view):
        perms = permissions_list(request)
        if 'all' in perms or 'file.read' in perms:
            return True
        return False


class FileUpdatePermission:

    def has_permission(self, request, view):
        perms = permissions_list(request)
        if 'all' in perms or 'file.update' in perms:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        perms = permissions_list(request)
        if 'all' in perms or 'file.update' in perms:
            return True
        return False

class FileDeletePermission:

    def has_permission(self, request, view):
        perms = permissions_list(request)
        if 'all' in perms or 'file.delete' in perms:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        perms = permissions_list(request)
        if 'all' in perms or 'file.delete' in perms:
            return True
        return False


