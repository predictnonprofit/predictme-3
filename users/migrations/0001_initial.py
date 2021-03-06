# Generated by Django 3.0.7 on 2020-06-25 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('full_name', models.CharField(max_length=60)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('street_address', models.CharField(max_length=50)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=50)),
                ('org_name', models.CharField(max_length=50)),
                ('job_title', models.CharField(blank=True, max_length=50, null=True)),
                ('org_website', models.URLField(blank=True, max_length=100, null=True)),
                ('org_type', models.CharField(max_length=50)),
                ('annual_revenue', models.CharField(max_length=200)),
                ('total_staff', models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True)),
                ('num_of_volunteer', models.IntegerField(blank=True, null=True)),
                ('num_of_board_members', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('active', 'Active'), ('cancelled', 'Cancelled'), ('unverified', 'Un-Verified')], default='unverified', max_length=20)),
                ('member_register_token', models.CharField(blank=True, max_length=150, null=True)),
                ('stripe_card_token', models.CharField(blank=True, max_length=200, null=True)),
                ('stripe_customer_id', models.CharField(blank=True, max_length=200, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'members',
            },
        ),
        migrations.CreateModel(
            name='UnverifiedMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_date', models.DateTimeField(auto_now_add=True)),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'unverified_member',
            },
        ),
    ]
