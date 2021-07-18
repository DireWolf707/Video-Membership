# Generated by Django 3.2.5 on 2021-07-18 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('type', models.CharField(choices=[('ent', 'Enterprise'), ('pro', 'Professional'), ('free', 'Free')], default='free', max_length=4)),
                ('price', models.IntegerField()),
                ('stripe_plan_id', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='UserMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_customer_id', models.CharField(max_length=40)),
                ('stripe_Subscription_id', models.CharField(blank=True, max_length=40)),
                ('active', models.BooleanField(default=True)),
                ('membership', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='memberships.membership')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='membership', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
