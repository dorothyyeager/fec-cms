# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-05 00:44
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0046_auto_20170105_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutlandingpage',
            name='sections',
            field=wagtail.wagtailcore.fields.StreamField((('sections', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('intro', wagtail.wagtailcore.blocks.RichTextBlock(blank=False, null=False, required=False)), ('button_text', wagtail.wagtailcore.blocks.CharBlock(blank=False, null=False, required=False)), ('related_page', wagtail.wagtailcore.blocks.PageChooserBlock(required=False))))),), null=True),
        ),
        migrations.AlterField(
            model_name='presslandingpage',
            name='option_blocks',
            field=wagtail.wagtailcore.fields.StreamField((('option_blocks', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('intro', wagtail.wagtailcore.blocks.RichTextBlock(blank=False, null=False, required=False)), ('button_text', wagtail.wagtailcore.blocks.CharBlock(blank=False, null=False, required=False)), ('related_page', wagtail.wagtailcore.blocks.PageChooserBlock(required=False))))),)),
        ),
    ]