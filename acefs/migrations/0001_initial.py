# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PrMajorsData'
        db.create_table('acefs_prmajorsdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('draft_cell', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('acefs', ['PrMajorsData'])

        # Adding model 'MLBData'
        db.create_table('acefs_mlbdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('draft_cell', self.gf('django.db.models.fields.IntegerField')()),
            ('year', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('acefs', ['MLBData'])

        # Adding model 'DOLSalary'
        db.create_table('acefs_dolsalary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('occupation', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sal10', self.gf('django.db.models.fields.IntegerField')()),
            ('sal25', self.gf('django.db.models.fields.IntegerField')()),
            ('sal50', self.gf('django.db.models.fields.IntegerField')()),
            ('sal75', self.gf('django.db.models.fields.IntegerField')()),
            ('sal90', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('acefs', ['DOLSalary'])

        # Adding model 'College'
        db.create_table('acefs_college', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('starting', self.gf('django.db.models.fields.IntegerField')()),
            ('mid_career', self.gf('django.db.models.fields.IntegerField')()),
            ('start_fx', self.gf('django.db.models.fields.FloatField')()),
            ('mid_fx', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('acefs', ['College'])

        # Adding model 'SlotBonus'
        db.create_table('acefs_slotbonus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pick', self.gf('django.db.models.fields.IntegerField')()),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
            ('draft_cell', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('acefs', ['SlotBonus'])


    def backwards(self, orm):
        
        # Deleting model 'PrMajorsData'
        db.delete_table('acefs_prmajorsdata')

        # Deleting model 'MLBData'
        db.delete_table('acefs_mlbdata')

        # Deleting model 'DOLSalary'
        db.delete_table('acefs_dolsalary')

        # Deleting model 'College'
        db.delete_table('acefs_college')

        # Deleting model 'SlotBonus'
        db.delete_table('acefs_slotbonus')


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
            'value': ('django.db.models.fields.FloatField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
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
