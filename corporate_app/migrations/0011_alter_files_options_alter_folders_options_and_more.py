# Generated by Django 4.1.5 on 2023-01-27 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corporate_app', '0010_alter_tasks_file_folders_files'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='files',
            options={'ordering': ('name',), 'verbose_name': 'File', 'verbose_name_plural': 'Files'},
        ),
        migrations.AlterModelOptions(
            name='folders',
            options={'ordering': ('name',), 'verbose_name': 'Folder', 'verbose_name_plural': 'Folders'},
        ),
        migrations.AlterField(
            model_name='files',
            name='folder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='corporate_app.folders'),
        ),
    ]
