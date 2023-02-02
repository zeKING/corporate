from .models import *
from rest_framework import serializers
import jwt

class UserUpdateSerializer(serializers.Serializer):
    fio = serializers.CharField(max_length=64, required=False)
    password = serializers.CharField(max_length=255, write_only=True, required=False)
    email = serializers.EmailField(required=False)
    avatar = serializers.ImageField(required=False)
    role_id = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        instance.fio = validated_data.get("fio", instance.fio)
        instance.email = validated_data.get('email', instance.email)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.role_id = validated_data.get('role_id', instance.role_id)

        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance



class RoleGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name']
        extra_kwargs = {
            'name': {'allow_null': True}
        }



class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    fio = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=255, write_only=True)
    email = serializers.EmailField()
    avatar = serializers.ImageField(required=False)
    role_id = serializers.IntegerField()


    # class Meta:
    #     model = User
    #     fields = ['id', 'fio', 'password', 'email', 'role_id']
    #     extra_kwargs = {
    #         'password': {'write_only': True},
    #     }

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        instance = User(**validated_data)
        print(instance)
        if password is not None:
            instance.set_password(password)
        instance.save() 
        return instance



class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64)
    description = serializers.CharField()
    file = serializers.FileField()
    deadline = serializers.DateTimeField()
    from_user_id = serializers.IntegerField(allow_null=True)
    to_user_id = serializers.IntegerField()

    def create(self, validated_data):
        request = self.context['request']
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload["id"]).first()
        instance = Tasks(**validated_data)
        from_id = validated_data.pop('from_user_id', None)
        instance.from_user_id = user.id
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.file = validated_data.get('file', instance.file)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.to_user_id = validated_data.get('to_user_id', instance.to_user_id)
        instance.save()
        return instance

    # class Meta:
    #     model = Tasks
    #     fields = ('title', 'description', 'file', 'deadline', 'from_user_id', 'to_user_id')


class FolderCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=64)
    parent_id = serializers.IntegerField(allow_null=True)

    def create(self, validated_data):
        instance = Folders(**validated_data)
        instance.save()
        return instance

    # class Meta:
        # model = Folders
        # fields = ('id', 'name', 'parent_id')
        # extra_kwargs = {
        #     'id': {'read_only': True}
        # }

class FolderUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folders
        fields = ("name")




class FileCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    file = serializers.FileField()
    folder_id = serializers.IntegerField()

    def create(self, validated_data):
        instance = Files.objects.create(**validated_data)
        instance.save()
        return instance


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ('name',)


class MessageSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    file = serializers.FileField(required=False)
    created = serializers.DateTimeField(required=False)
    from_user_id = serializers.IntegerField(required=False)
    to_user_id = serializers.IntegerField()

    def create(self, validated_data):
        instance = Message.objects.create(**validated_data)
        instance.save()
        return instance