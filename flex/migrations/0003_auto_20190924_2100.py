# Generated by Django 2.2.5 on 2019-09-24 21:00

from django.db import migrations
import streams.blocks
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('flex', '0002_auto_20190923_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flexpage',
            name='content',
            field=wagtail.core.fields.StreamField([('title_and_text', wagtail.core.blocks.StructBlock([('blocktitle', wagtail.core.blocks.CharBlock(help_text='Add title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='add text', required=True))])), ('full_richtext', streams.blocks.RichtextBlock())], blank=True, null=True),
        ),
    ]
