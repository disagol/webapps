# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NodeType'
        db.create_table(u'wStationMgr_nodetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'wStationMgr', ['NodeType'])

        # Adding M2M table for field allowed_parents on 'NodeType'
        m2m_table_name = db.shorten_name(u'wStationMgr_nodetype_allowed_parents')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_nodetype', models.ForeignKey(orm[u'wStationMgr.nodetype'], null=False)),
            ('to_nodetype', models.ForeignKey(orm[u'wStationMgr.nodetype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_nodetype_id', 'to_nodetype_id'])

        # Adding model 'BaseTreeNode'
        db.create_table(u'wStationMgr_basetreenode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'polymorphic_wstationmgr.basetreenode_set', null=True, to=orm['contenttypes.ContentType'])),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('parent', self.gf('polymorphic_tree.models.PolymorphicTreeForeignKey')(blank=True, related_name='children', null=True, to=orm['wStationMgr.BaseTreeNode'])),
            ('node_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wStationMgr.NodeType'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'wStationMgr', ['BaseTreeNode'])

        # Adding model 'Network'
        db.create_table(u'wStationMgr_network', (
            (u'basetreenode_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wStationMgr.BaseTreeNode'], unique=True, primary_key=True)),
            ('security_protocol', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'wStationMgr', ['Network'])

        # Adding model 'Server'
        db.create_table(u'wStationMgr_server', (
            (u'basetreenode_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wStationMgr.BaseTreeNode'], unique=True, primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('os', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'wStationMgr', ['Server'])

        # Adding model 'LogicalDevice'
        db.create_table(u'wStationMgr_logicaldevice', (
            (u'basetreenode_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wStationMgr.BaseTreeNode'], unique=True, primary_key=True)),
            ('ref', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'wStationMgr', ['LogicalDevice'])

        # Adding model 'LogicalNode'
        db.create_table(u'wStationMgr_logicalnode', (
            (u'basetreenode_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wStationMgr.BaseTreeNode'], unique=True, primary_key=True)),
            ('ref', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'wStationMgr', ['LogicalNode'])

        # Adding model 'Data'
        db.create_table(u'wStationMgr_data', (
            (u'basetreenode_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wStationMgr.BaseTreeNode'], unique=True, primary_key=True)),
            ('ref', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('presence', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'wStationMgr', ['Data'])

        # Adding model 'CompositeData'
        db.create_table(u'wStationMgr_compositedata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ref', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('presence', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('data', self.gf('django.db.models.fields.related.ForeignKey')(related_name='composite_datas', to=orm['wStationMgr.Data'])),
        ))
        db.send_create_signal(u'wStationMgr', ['CompositeData'])

        # Adding model 'BasicType'
        db.create_table(u'wStationMgr_basictype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('length', self.gf('django.db.models.fields.IntegerField')(default=5, max_length=10, null=True, blank=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'wStationMgr', ['BasicType'])

        # Adding model 'FunctionalConstraint'
        db.create_table(u'wStationMgr_functionalconstraint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('semantic', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'wStationMgr', ['FunctionalConstraint'])

        # Adding model 'AttributeTypeData'
        db.create_table(u'wStationMgr_attributetypedata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ref', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('presence', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('basic_type', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wStationMgr.BasicType'], unique=True)),
        ))
        db.send_create_signal(u'wStationMgr', ['AttributeTypeData'])

        # Adding model 'AttributeData'
        db.create_table(u'wStationMgr_attributedata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attr_datas', to=orm['wStationMgr.Data'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('attribute_type_data', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attr_datas', to=orm['wStationMgr.AttributeTypeData'])),
            ('functional_constraint', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attr_datas', to=orm['wStationMgr.FunctionalConstraint'])),
        ))
        db.send_create_signal(u'wStationMgr', ['AttributeData'])

        # Adding model 'CompositeComponent'
        db.create_table(u'wStationMgr_compositecomponent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ref', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('presence', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('attribute_type_data', self.gf('django.db.models.fields.related.ForeignKey')(related_name='composite_components', to=orm['wStationMgr.AttributeTypeData'])),
        ))
        db.send_create_signal(u'wStationMgr', ['CompositeComponent'])


    def backwards(self, orm):
        # Deleting model 'NodeType'
        db.delete_table(u'wStationMgr_nodetype')

        # Removing M2M table for field allowed_parents on 'NodeType'
        db.delete_table(db.shorten_name(u'wStationMgr_nodetype_allowed_parents'))

        # Deleting model 'BaseTreeNode'
        db.delete_table(u'wStationMgr_basetreenode')

        # Deleting model 'Network'
        db.delete_table(u'wStationMgr_network')

        # Deleting model 'Server'
        db.delete_table(u'wStationMgr_server')

        # Deleting model 'LogicalDevice'
        db.delete_table(u'wStationMgr_logicaldevice')

        # Deleting model 'LogicalNode'
        db.delete_table(u'wStationMgr_logicalnode')

        # Deleting model 'Data'
        db.delete_table(u'wStationMgr_data')

        # Deleting model 'CompositeData'
        db.delete_table(u'wStationMgr_compositedata')

        # Deleting model 'BasicType'
        db.delete_table(u'wStationMgr_basictype')

        # Deleting model 'FunctionalConstraint'
        db.delete_table(u'wStationMgr_functionalconstraint')

        # Deleting model 'AttributeTypeData'
        db.delete_table(u'wStationMgr_attributetypedata')

        # Deleting model 'AttributeData'
        db.delete_table(u'wStationMgr_attributedata')

        # Deleting model 'CompositeComponent'
        db.delete_table(u'wStationMgr_compositecomponent')


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
            'node_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wStationMgr.NodeType']"}),
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
            'length': ('django.db.models.fields.IntegerField', [], {'default': '5', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        u'wStationMgr.compositecomponent': {
            'Meta': {'object_name': 'CompositeComponent'},
            'attribute_type_data': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'composite_components'", 'to': u"orm['wStationMgr.AttributeTypeData']"}),
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
        u'wStationMgr.nodetype': {
            'Meta': {'object_name': 'NodeType'},
            'allowed_parents': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['wStationMgr.NodeType']", 'symmetrical': 'False'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'wStationMgr.server': {
            'Meta': {'object_name': 'Server', '_ormbases': [u'wStationMgr.BaseTreeNode']},
            u'basetreenode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wStationMgr.BaseTreeNode']", 'unique': 'True', 'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['wStationMgr']