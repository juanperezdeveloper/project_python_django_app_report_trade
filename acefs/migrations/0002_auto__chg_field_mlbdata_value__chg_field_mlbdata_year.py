# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'MLBData.value'
        db.alter_column('acefs_mlbdata', 'value', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'MLBData.year'
        db.alter_column('acefs_mlbdata', 'year', self.gf('django.db.models.fields.IntegerField')())


    def backwards(self, orm):
        
        # Changing field 'MLBData.value'
        db.alter_column('acefs_mlbdata', 'value', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'MLBData.year'
        db.alter_column('acefs_mlbdata', 'year', self.gf('django.db.models.fields.IntegerField')(null=True))


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
        'acefs.slotbonus': {
            'Meta': {'object_name': 'SlotBonus'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'draft_cell': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pick': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['acefs']
