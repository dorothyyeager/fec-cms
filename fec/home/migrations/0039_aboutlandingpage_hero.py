# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-27 15:12
from __future__ import unicode_literals

from django.db import migrations
import wagtail.contrib.table_block.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0038_aboutlandingpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutlandingpage',
            name='hero',
            field=wagtail.wagtailcore.fields.StreamField([(b'heading', wagtail.wagtailcore.blocks.CharBlock(classname=b'full title')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), (b'html', wagtail.wagtailcore.blocks.RawHTMLBlock()), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'table', wagtail.contrib.table_block.blocks.TableBlock())], blank=True, null=True),
        ),
    ]
