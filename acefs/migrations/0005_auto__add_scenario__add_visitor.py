# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Scenario'
        db.create_table('acefs_scenario', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('visitor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['acefs.Visitor'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('anonymous', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('college', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['acefs.College'])),
            ('alt', self.gf('django.db.models.fields.related.ForeignKey')(related_name='alt_scenario_set', to=orm['acefs.DOLSalary'])),
            ('sec', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sec_scenario_set', to=orm['acefs.DOLSalary'])),
            ('pick', self.gf('django.db.models.fields.IntegerField')()),
            ('pos', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('acefs', ['Scenario'])

        # Adding model 'Visitor'
        db.create_table('acefs_visitor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modx_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('acefs', ['Visitor'])


    def backwards(self, orm):
        
        # Deleting model 'Scenario'
        db.delete_table('acefs_scenario')

        # Deleting model 'Visitor'
        db.delete_table('acefs_visitor')


    models = {
        'acefs.college': {
            'Meta': {'object_name': 'College'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mid_career': ('django.db.models.fields.IntegerField', [], {}),
            'mid_fx': ('django.db.models.fields.FloatField', [], {}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_fx': ('django.db.models.fields.FloatField', [], {}),
            'starting': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'acefs.dolsalary': {
            'Meta': {'object_name': 'DOLSalary'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sal10': ('django.db.models.fields.IntegerField', [], {}),
            'sal25': ('django.db.models.fields.IntegerField', [], {}),
            'sal50': ('django.db.models.fields.IntegerField', [], {}),
            'sal75': ('django.db.models.fields.IntegerField', [], {}),
            'sal90': ('django.db.models.fields.IntegerField', [], {})
        },
        'acefs.mlbdata': {
            'Meta': {'object_name': 'MLBData'},
            'draft_cell': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'acefs.prmajorsdata': {
            'Meta': {'object_name': 'PrMajorsData'},
            'draft_cell': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'acefs.proutposition': {
            'Meta': {'object_name': 'PrOutPosition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'acefs.proutstatus': {
            'Meta': {'object_name': 'PrOutStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'acefs.scenario': {
            'Meta': {'object_name': 'Scenario'},
            'alt': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alt_scenario_set'", 'to': "orm['acefs.DOLSalary']"}),
            'anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'college': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['acefs.College']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pick': ('django.db.models.fields.IntegerField', [], {}),
            'pos': ('django.db.models.fields.IntegerField', [], {}),
            'sec': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sec_scenario_set'", 'to': "orm['acefs.DOLSalary']"}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'visitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['acefs.Visitor']"})
        },
        'acefs.signingbonus': {
            'Meta': {'object_name': 'SigningBonus'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'draft_cell': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {})
        },
        'acefs.slotbonus': {
            'Meta': {'object_name': 'SlotBonus'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'draft_cell': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pick': ('django.db.models.fields.IntegerField', [], {})
        },
        'acefs.visitor': {
            'Meta': {'object_name': 'Visitor'},
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'modx_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['acefs']
