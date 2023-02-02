from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError

# Create your models here.

# def picture_upload_to(instance, filename):
#     relative_path = instance.url_to_upload.rfind('images/avatars') + len("images/avatars")
#     return instance.url_to_upload[relative_path:]
#


def validate_file_size(value):
    filesize = value.size
    if filesize > 10485760:
        raise ValidationError("You cannot upload file more than 10Mb")
    else:
        return value

def file_upload_to(instance, filename):
    try:
        if instance.folder:
            return file_upload_to(instance.folder, filename) + '/' + instance.folder.name + '/' + filename

        return 'files'
    except:
        if instance.parent:
            print('files' + file_upload_to(instance.parent, filename) + '/' + instance.parent.name)
            return file_upload_to(instance.parent, filename) + '/' + instance.parent.name

        return 'files'


class Role(models.Model):
    name = models.CharField("Role", max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"


class Permission(models.Model):
    name = models.CharField("Permission", max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
        ordering = ('id',)


class User(AbstractUser):
    fio = models.CharField("Fio", max_length=255)
    email = models.EmailField("Email", unique=True)
    password = models.CharField("Password", max_length=255)
    avatar = models.ImageField(
    "Picture",
    upload_to='images/avatars',
    default='images/avatars/person.png',
    blank=True,
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg']), validate_file_size],)
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.fio 

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"



class RolePermission(models.Model):
    role = models.ForeignKey(Role, related_name="role", null=True, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, related_name="permission", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.role)

    class Meta:
        verbose_name = "RolePermission"
        verbose_name_plural = "RolePermissions"
        ordering = ('role_id', 'permission')

class Tasks(models.Model):
    title = models.CharField("Title", max_length=64)
    description = models.TextField("Description")
    file = models.FileField(
    upload_to='files/tasks',
    blank=True,
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'doc', 'docx', 'xlsx', 'pptx', 'pdf'])])
    deadline = models.DateTimeField(null=True)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='From', null=True, on_delete=models.SET_NULL)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='To', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class Folders(models.Model):
    name = models.CharField("Name", max_length=64)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'

class Files(models.Model):
    name = models.CharField("Name", max_length=64)
    file = models.FileField(
        upload_to=file_upload_to,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'doc', 'docx', 'xlsx', 'pptx', 'pdf'])],
    )
    folder = models.ForeignKey(Folders, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        verbose_name = 'File'
        verbose_name_plural = 'Files'


class Message(models.Model):
    text = models.TextField("Text")
    file = models.FileField("File", blank=True, null=True, upload_to="chat_files")
    created = models.DateTimeField("Created", auto_now_add=True)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='message_from_user', on_delete=models.PROTECT)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='message_to_user', on_delete=models.PROTECT)

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.text

class LastMessagesUsers(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.PROTECT)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.PROTECT)

    class Meta:
        ordering = ('from_user', )
        # verbose_name = 'Last'
        # verbose_name_plural = 'Lasts'


