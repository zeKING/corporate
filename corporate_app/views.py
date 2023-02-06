from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .consumers import ChatConsumer
from .models import *
# Create your views here.
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from .permissions import *
from .permissions import AdminOrReadOnly
from .pagination import *
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


# class UserAPIGet(APIView):
#     def get(self, request, pk):
#         user = User.objects.filter(id=pk).first()
#         serializer = UserUpdateSerializer(user)
#         perms = RolePermission.objects.filter(role=user.role)
#
#
#         print(serializer.data)
#
#         perms_lst = [i.permission.name for i in perms]
#         response = dict(list(serializer.data) + perms_lst)
#         return Response(response)

class UserAPIGetAll(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]



class UserAPIUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, ]

class UserAPIDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]



class RegisterView(APIView):
    def post(self, request):

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data)

# class LoginView(APIView):
#     def post(self, request):
#         email = request.data['email']
#         password = request.data['password']
#         user = User.objects.filter(email=email).first()
#         if user is None:
#             raise AuthenticationFailed("User not found!")
#
#         if not user.check_password(password):
#             raise AuthenticationFailed("Password is incorrect")
#
#         payload = {
#             'id': user.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=300),
#             'iat': datetime.datetime.utcnow()
#         }
#         token = jwt.encode(payload, 'secret', algorithm='HS256')
#         response = Response()
#         response.set_cookie(key='jwt', value=token, httponly=True)
#         response.data = {
#             'jwt': token
#         }
#
#         return response


class UserAPIGet(APIView):
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        perms = RolePermission.objects.filter(role_id=user.role_id)
        perms_list = [i.permission.name for i in perms]
        return Response({
            'id': user.id,
            'fio': user.fio,
            'email': user.email,
            'avatar': user.avatar.url,
            'role': user.role.name,
            'permissions': perms_list

        })




class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request):
        response = Response()
        # response.delete_cookie('jwt')
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()

        response.data = {
            'message': 'success'
        }
        return response


class RolesAPIGet(APIView):
    permission_classes = [permissions.IsAuthenticated, RoleReadPermission]
    def get(self, request, pk):

        RolePerms = RolePermission.objects.filter(role_id=pk)
        RolePermsObjs = [i.permission for i in RolePerms]
        perms_all = Permission.objects.all()
        all_obj = []
        for i in perms_all:
            all_obj += [{
                "id": i.id,
                "name": i.name,
                "value": int(i in RolePermsObjs),
            }]

        return Response(all_obj)


class RolesAPIGetAll(generics.ListAPIView):
    queryset = Role.objects.all()   
    serializer_class = RoleGetSerializer
    permission_classes = [permissions.IsAuthenticated, RoleReadPermission]


class PermissionsAPIGetAll(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated, PermissionReadPermission]


class RoleAPICreate(generics.CreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated, RoleCreatePermission]


class RoleAPIUpdate(APIView):
    permission_classes = [permissions.IsAuthenticated, RoleUpdatePermisson]

    def patch(self, request, pk):
        role_permission_objects = RolePermission.objects.filter(role_id=pk)
        role_perms = [i.permission.name for i in role_permission_objects]
        perms_all = Permission.objects.all()
        data = request.data
        if data[0]["value"]:
            if not role_permission_objects.first().permission.name == 'all':
                RolePermission.objects.create(role_id=pk,
                                              permission_id=1)
            all_obj = []
            for i in perms_all:
                all_obj += [{
                    "id": i.id,
                    "name": i.name,
                    "value": 0
                }]
                all_obj[0]["value"] = 1
            return Response(all_obj)

        else:
            all_obj = []
            for i in range(1, len(perms_all)):
                if data[i]["value"]:
                    if not data[i]["name"] in role_perms:
                        RolePermission.objects.create(role_id=pk, permission_id=data[i]["id"])
                else:
                    if data[i]["name"] in role_perms:
                        RolePermission.objects.filter(role_id=pk, permission_id=data[i]["id"]).delete()

            all_obj = []
            perms_all = Permission.objects.all()

            for i in perms_all:
                all_obj += [{
                    "id": i.id,
                    "name": i.name,
                    "value": 0
                }]
                all_obj[0]["value"] = 1
            return Response(all_obj)


class RoleAPIDelete(generics.DestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated, RoleDeletePermission]


class TaskAPIGetAll(generics.ListAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, TaskReadPermission]


class TaskAPIGet(generics.RetrieveAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, TaskReadPermission]


class TaskAPICreate(generics.CreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, TaskCreatePermission]


class TaskAPIUpdate(generics.UpdateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, TaskUpdatePermission]

class TaskAPIFromMe(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, TaskReadPermission]
    def get_queryset(self):
        return Tasks.objects.filter(from_user_id=self.request.user.id)

class TaskAPIToMe(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, TaskReadPermission]
    def get_queryset(self):
        return Tasks.objects.filter(to_user_id=self.request.user.id)



class TaskAPIDelete(generics.DestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, TaskDeletePermission]


class FolderAPIGet(APIView):
    permission_classes = [permissions.IsAuthenticated, FolderReadPermission]

    def get(self, request, pk):
        files = Files.objects.filter(folder_id=pk)
        file_objs = []
        all_obj = dict()
        self_folder = Folders.objects.get(pk=pk)
        all_obj["self_folder"] = {
            "id": pk,
            "name": self_folder.name,
            "parent_id": self_folder.parent_id
        }
        folders = Folders.objects.filter(parent_id=pk)
        fold_objs = []
        for fold in folders:
            fold_objs += [{
                "id": fold.id,
                "name": fold.name,
            }]

        all_obj["folders"] = fold_objs

        for file in files:
            file_objs += [{
                "id": file.id,
                "name": file.name,
                "path": file.file.path
             }]
        all_obj["files"] = file_objs
        return Response(all_obj)


class FolderAPICreate(generics.CreateAPIView):
    queryset = Folders.objects.all()
    serializer_class = FolderCreateSerializer
    permission_classes = [permissions.IsAuthenticated, FolderCreatePermission]


class FolderAPIUpdate(generics.UpdateAPIView):
    queryset = Folders.objects.all()
    serializer_class = FolderUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, FolderUpdatePermission]


class FolderAPIGetFirst(generics.ListAPIView):
    queryset = Folders.objects.filter(parent=None)
    serializer_class = FolderCreateSerializer
    permission_classes = [permissions.IsAuthenticated, FolderReadPermission]


class FolderAPIDelete(generics.DestroyAPIView):
    queryset = Folders.objects.all()
    # serializer_class = FolderDeleteSerializer
    permission_classes = [permissions.IsAuthenticated, FolderUpdatePermission]


class FileAPICreate(generics.CreateAPIView):
    queryset = Files.objects.all()
    serializer_class = FileCreateSerializer
    permission_classes = [permissions.IsAuthenticated, FileCreatePermission]


class FileAPIUpdate(generics.UpdateAPIView):
    queryset = Files.objects.all()
    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     # context["pk"] = self.request.data
    #     print(self.request.)
    #     return context
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated, FileUpdatePermission]


class FileAPIDelete(generics.DestroyAPIView):
    queryset = Files.objects.all()
    # serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated, FileDeletePermission]


class MessagesAPIGet(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = MessagePagination

# class MessageCreate(generics.CreateAPIView):
#     queryset = Message.objects.all()
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['to_user_id'] = self.context['']
#     serializer_class = MessageSerializer

class MessageCreate(APIView):
    # permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request, from_user_id, to_user_id):

        request.data._mutable = True
        data = request.data
        data['from_user_id'] = from_user_id
        data['to_user_id'] = to_user_id
        request.data._mutable = False
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if not Dialog.objects.filter(from_user_id=from_user_id, to_user_id=to_user_id):
            Dialog.objects.create(from_user_id=from_user_id, to_user_id=to_user_id)
            Dialog.objects.create(from_user_id=to_user_id, to_user_id=from_user_id)

        else:
            Dialog.objects.filter(from_user_id=from_user_id, to_user_id=to_user_id).update()
            Dialog.objects.filter(from_user_id=to_user_id, to_user_id=from_user_id).update()
        return Response({'message': 'saved'})


class LastCompanions(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, from_user_id, to_user_id):

        last_companions = Dialog.objects.filter(from_user_id=from_user_id)

        return Response({
            "dialog_last_users": [{'id': i.to_user_id, 'name': i.to_user} for i in last_companions]
        })

# def index(request):
#     return render(request, 'index2.html')