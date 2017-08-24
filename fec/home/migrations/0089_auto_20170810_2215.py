# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-10 22:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import home.blocks
import wagtail.contrib.table_block.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtaildocs.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
        ('wagtailimages', '0017_reduce_focal_point_key_max_length'),
        ('home', '0088_auto_20170802_2329'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportingExamplePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('pre_title', models.CharField(blank=True, choices=[('how', 'How to report'), ('scenario', 'Example scenario')], max_length=255, null=True)),
                ('body', wagtail.wagtailcore.fields.StreamField((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('example_image', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('caption', wagtail.wagtailcore.blocks.RichTextBlock(required=True)), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=True))))), ('reporting_example_cards', wagtail.wagtailcore.blocks.StructBlock((('cards', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.PageChooserBlock(), icon='doc-empty')),)))), null=True)),
                ('related_media_title', models.CharField(blank=True, max_length=255, null=True)),
                ('related_media', wagtail.wagtailcore.fields.StreamField((('continue_learning', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('url', wagtail.wagtailcore.blocks.URLBlock()), ('media_type', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))), icon='doc-empty', template='blocks/related-media.html')),), null=True)),
                ('featured_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='collectionpage',
            name='reporting_examples',
            field=wagtail.wagtailcore.fields.StreamField((('reporting_examples', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('label', wagtail.wagtailcore.blocks.CharBlock()), ('content', wagtail.wagtailcore.blocks.RichTextBlock(help_text='Use Shift + Enter to add line breaks between citation and description')))))),), null=True),
        ),
        migrations.AlterField(
            model_name='custompage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('example_paragraph', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(required=True))))), ('example_forms', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('forms', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('url', wagtail.wagtailcore.blocks.URLBlock()), ('media_type', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))))))), ('reporting_example_cards', wagtail.wagtailcore.blocks.StructBlock((('cards', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.PageChooserBlock(), icon='doc-empty')),))))),
        ),
        migrations.AlterField(
            model_name='custompage',
            name='continue_learning',
            field=wagtail.wagtailcore.fields.StreamField((('continue_learning', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('url', wagtail.wagtailcore.blocks.URLBlock()), ('media_type', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))), icon='doc-empty')),), null=True),
        ),
        migrations.AlterField(
            model_name='resourcepage',
            name='sections',
            field=wagtail.wagtailcore.fields.StreamField((('sections', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('hide_title', wagtail.wagtailcore.blocks.BooleanBlock(help_text='Should the section title be displayed?', required=False)), ('content', wagtail.wagtailcore.blocks.StreamBlock((('text', wagtail.wagtailcore.blocks.RichTextBlock(blank=False, icon='pilcrow', null=False, required=False)), ('documents', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('url', wagtail.wagtailcore.blocks.URLBlock()), ('media_type', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))), icon='doc-empty', template='blocks/section-documents.html')), ('contact_info', wagtail.wagtailcore.blocks.StructBlock((('label', wagtail.wagtailcore.blocks.CharBlock(icon='title', required=False)), ('contact_items', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('item_label', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('item_icon', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('email', 'Email'), ('fax', 'Fax'), ('hand', 'Hand delivery'), ('phone', 'Phone'), ('mail', 'Mail')])), ('item_info', wagtail.wagtailcore.blocks.RichTextBlock(required=True))))))))), ('internal_button', wagtail.wagtailcore.blocks.StructBlock((('internal_page', wagtail.wagtailcore.blocks.PageChooserBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('external_button', wagtail.wagtailcore.blocks.StructBlock((('url', wagtail.wagtailcore.blocks.URLBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('page', wagtail.wagtailcore.blocks.PageChooserBlock(template='blocks/page-links.html')), ('disabled_page', wagtail.wagtailcore.blocks.CharBlock(blank=False, help_text='Name of a disabled link', icon='placeholder', null=False, required=False, template='blocks/disabled-page-links.html')), ('document_list', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('document', wagtail.wagtaildocs.blocks.DocumentChooserBlock()))), icon='doc-empty', template='blocks/document-list.html')), ('current_commissioners', home.blocks.CurrentCommissionersBlock()), ('fec_jobs', home.blocks.CareersBlock()), ('mur_search', home.blocks.MURSearchBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('reporting_example_cards', wagtail.wagtailcore.blocks.StructBlock((('cards', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.PageChooserBlock(), icon='doc-empty')),)))))), ('aside', wagtail.wagtailcore.blocks.StreamBlock((('title', wagtail.wagtailcore.blocks.CharBlock(icon='title', required=False)), ('document', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('url', wagtail.wagtailcore.blocks.URLBlock()), ('media_type', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('link', wagtail.wagtailcore.blocks.StructBlock((('link_type', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('calculator', 'Calculator'), ('calendar', 'Calendar'), ('record', 'Record'), ('search', 'Search')], help_text='Set an icon', icon='link', required=False)), ('url', wagtail.wagtailcore.blocks.URLBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('coming_soon', wagtail.wagtailcore.blocks.BooleanBlock(required=False)))))), icon='placeholder', template='blocks/section-aside.html'))))),), null=True),
        ),
        migrations.AlterField(
            model_name='serviceslandingpage',
            name='sections',
            field=wagtail.wagtailcore.fields.StreamField((('sections', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('hide_title', wagtail.wagtailcore.blocks.BooleanBlock(help_text='Should the section title be displayed?', required=False)), ('content', wagtail.wagtailcore.blocks.StreamBlock((('text', wagtail.wagtailcore.blocks.RichTextBlock(blank=False, icon='pilcrow', null=False, required=False)), ('documents', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('url', wagtail.wagtailcore.blocks.URLBlock()), ('media_type', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))), icon='doc-empty', template='blocks/section-documents.html')), ('contact_info', wagtail.wagtailcore.blocks.StructBlock((('label', wagtail.wagtailcore.blocks.CharBlock(icon='title', required=False)), ('contact_items', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('item_label', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('item_icon', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('email', 'Email'), ('fax', 'Fax'), ('hand', 'Hand delivery'), ('phone', 'Phone'), ('mail', 'Mail')])), ('item_info', wagtail.wagtailcore.blocks.RichTextBlock(required=True))))))))), ('internal_button', wagtail.wagtailcore.blocks.StructBlock((('internal_page', wagtail.wagtailcore.blocks.PageChooserBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('external_button', wagtail.wagtailcore.blocks.StructBlock((('url', wagtail.wagtailcore.blocks.URLBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('page', wagtail.wagtailcore.blocks.PageChooserBlock(template='blocks/page-links.html')), ('disabled_page', wagtail.wagtailcore.blocks.CharBlock(blank=False, help_text='Name of a disabled link', icon='placeholder', null=False, required=False, template='blocks/disabled-page-links.html')), ('document_list', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('document', wagtail.wagtaildocs.blocks.DocumentChooserBlock()))), icon='doc-empty', template='blocks/document-list.html')), ('current_commissioners', home.blocks.CurrentCommissionersBlock()), ('fec_jobs', home.blocks.CareersBlock()), ('mur_search', home.blocks.MURSearchBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('reporting_example_cards', wagtail.wagtailcore.blocks.StructBlock((('cards', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.PageChooserBlock(), icon='doc-empty')),)))))), ('aside', wagtail.wagtailcore.blocks.StreamBlock((('title', wagtail.wagtailcore.blocks.CharBlock(icon='title', required=False)), ('document', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('url', wagtail.wagtailcore.blocks.URLBlock()), ('media_type', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('link', wagtail.wagtailcore.blocks.StructBlock((('link_type', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('calculator', 'Calculator'), ('calendar', 'Calendar'), ('record', 'Record'), ('search', 'Search')], help_text='Set an icon', icon='link', required=False)), ('url', wagtail.wagtailcore.blocks.URLBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('coming_soon', wagtail.wagtailcore.blocks.BooleanBlock(required=False)))))), icon='placeholder', template='blocks/section-aside.html'))))),), null=True),
        ),
    ]
