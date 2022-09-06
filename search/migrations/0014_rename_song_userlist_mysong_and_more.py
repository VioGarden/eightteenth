# Generated by Django 4.1 on 2022-09-06 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0013_userlist_alter_mysonguser_my_songs_userlist_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userlist',
            old_name='song',
            new_name='MySong',
        ),
        migrations.RenameField(
            model_name='userlist',
            old_name='user',
            new_name='MySongUser',
        ),
        migrations.AlterUniqueTogether(
            name='userlist',
            unique_together={('MySongUser', 'MySong')},
        ),
    ]
