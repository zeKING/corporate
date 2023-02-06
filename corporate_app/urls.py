from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import *
urlpatterns = [
    path('auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    # path('users/<int:pk>', UserAPIGet.as_view()),
    path('auth/register', RegisterView.as_view()),
    # path('auth/login', LoginView.as_view()),
    path('auth/user', UserAPIGet.as_view()),
    path('auth/logout', LogoutView.as_view()),
    path('roles/<int:pk>', RolesAPIGet.as_view()),
    path('roles/create', RoleAPICreate.as_view()),
    path('roles', RolesAPIGetAll.as_view()),
    path('roles/update/<int:pk>', RoleAPIUpdate.as_view()),
    path('roles/delete/<int:pk>', RoleAPIDelete.as_view()),
    path('tasks', TaskAPIGetAll.as_view()),
    path('tasks/<int:pk>', TaskAPIGet.as_view()),
    path('tasks/create', TaskAPICreate.as_view()),
    path('tasks/update/<int:pk>', TaskAPIUpdate.as_view()),
    path('tasks/delete/<int:pk>', TaskAPIDelete.as_view()),
    path('tasks/from_me', TaskAPIFromMe.as_view()),
    path('tasks/to_me', TaskAPIToMe.as_view()),
    path('folders/<int:pk>', FolderAPIGet.as_view()),
    path('folders', FolderAPIGetFirst.as_view()),
    path('folders/create', FolderAPICreate.as_view()),
    path('folders/update/<int:pk>', FolderAPIUpdate.as_view()),
    path('folders/delete/<int:pk>', FolderAPIDelete.as_view()),
    path('files/create', FileAPICreate.as_view()),
    path('files/update/<int:pk>', FileAPIUpdate.as_view()),
    path('files/delete/<int:pk>', FileAPIDelete.as_view()),
    path('messages', MessagesAPIGet.as_view()),
    path('messages/send/<int:from_user_id>/<int:to_user_id>', MessageCreate.as_view()),
    path('messages/companions', LastCompanions.as_view()),

    # path('index', index, name='index'),
    path('users/update/<int:pk>', UserAPIUpdate.as_view()),
    path('users/delete/<int:pk>', UserAPIDelete.as_view()),
    path('users', UserAPIGetAll.as_view()),
    path('ws/message/<int:from_user_id>/<int:to_user_id>', MessageCreate.as_view()),
    # path('user/<int:pk>', UserAPIGet.as_view()),

]



