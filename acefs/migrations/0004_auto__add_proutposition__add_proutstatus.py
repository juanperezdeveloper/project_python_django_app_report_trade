# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PrOutPosition'
        db.create_table('acefs_proutposition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal('acefs', ['PrOutPosition'])

        # Adding model 'PrOutStatus'
        db.create_table('acefs_proutstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal('acefs', ['PrOutStatus'])


    def backwards(self, orm):
        
        # Deleting model 'PrOutPosition'
        db.delete_table('acefs_proutposition')

        # Deleting model 'PrOutStatus'
        db.delete_table('acefs_proutstatus')


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
        }
    }

    complete_apps = ['acefs']
