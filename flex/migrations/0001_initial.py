# Generated by Django 2.2.5 on 2019-09-23 21:47

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', wagtail.core.fields.StreamField([('title_and_text', wagtail.core.blocks.StructBlock([('blocktitle', wagtail.core.blocks.CharBlock(help_text='Add title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='add text', required=True))]))], blank=True, null=True)),
                ('newsubtitle', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
