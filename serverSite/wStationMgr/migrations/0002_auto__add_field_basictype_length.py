# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BasicType.length'
        db.add_column(u'wStationMgr_basictype', 'length',
                      self.gf('django.db.models.fields.IntegerField')(default=5, max_length=10, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'BasicType.length'
        db.delete_column(u'wStationMgr_basictype', 'length')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'wStationMgr.attributedata': {
            'Meta': {'object_name': 'AttributeData'},
            'attribute_type_data': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attr_datas'", 'to': u"orm['wStationMgr.AttributeTypeData']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attr_datas'", 'to': u"orm['wStationMgr.Data']"}),
            'functional_constraint': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attr_datas'", 'to': u"orm['wStationMgr.FunctionalConstraint']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'wStationMgr.attributetypedata': {
            'Meta': {'object_name': 'AttributeTypeData'},
            'basic_type': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wStationMgr.BasicType']", 'unique': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'presence': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'wStationMgr.basetreenode': {
            'Meta': {'object_name': 'BaseTreeNode'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'parent': ('polymorphic_tree.models.PolymorphicTreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['wStationMgr.BaseTreeNode']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_wstationmgr.basetreenode_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'wStationMgr.basictype': {
            'Meta': {'object_name': 'BasicType'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'default': '5', 'max_length': '10', 'null': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        u'wStationMgr.compositecomponent': {
            'Meta': {'object_name': 'CompositeComponent'},
            'attribute_type_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wStationMgr.AttributeTypeData']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'presence': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'wStationMgr.compositedata': {
            'Meta': {'object_name': 'CompositeData'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'composite_datas'", 'to': u"orm['wStationMgr.Data']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'presence': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'wStationMgr.data': {
            'Meta': {'object_name': 'Data', '_ormbases': [u'wStationMgr.BaseTreeNode']},
            u'basetreenode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wStationMgr.BaseTreeNode']", 'unique': 'True', 'primary_key': 'True'}),
            'presence': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'wStationMgr.functionalconstraint': {
            'Meta': {'object_name': 'FunctionalConstraint'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'semantic': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'wStationMgr.logicaldevice': {
            'Meta': {'object_name': 'LogicalDevice', '_ormbases': [u'wStationMgr.BaseTreeNode']},
            u'basetreenode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wStationMgr.BaseTreeNode']", 'unique': 'True', 'primary_key': 'True'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'wStationMgr.logicalnode': {
            'Meta': {'object_name': 'LogicalNode', '_ormbases': [u'wStationMgr.BaseTreeNode']},
            u'basetreenode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wStationMgr.BaseTreeNode']", 'unique': 'True', 'primary_key': 'True'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'wStationMgr.network': {
            'Meta': {'object_name': 'Network', '_ormbases': [u'wStationMgr.BaseTreeNode']},
            u'basetreenode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wStationMgr.BaseTreeNode']", 'unique': 'True', 'primary_key': 'True'}),
            'security_protocol': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'wStationMgr.server': {
            'Meta': {'object_name': 'Server', '_ormbases': [u'wStationMgr.BaseTreeNode']},
            u'basetreenode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wStationMgr.BaseTreeNode']", 'unique': 'True', 'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['wStationMgr']