from django.contrib.admin.options import ModelAdmin, TabularInline
from django_mlds.acefs.models import College, SlotBonus, MLBData, DOLSalary, PrMajorsData, SigningBonus, Visitor, Scenario
from django.contrib import admin

class CollegeAdmin(ModelAdmin):
    list_filter = ('type',)
    search_fields = ('school',)
    list_display = ('school', 'type', 'starting', 'mid_career','start_fx', 'mid_fx')
admin.site.register(College, CollegeAdmin)

class SlotBonusAdmin(ModelAdmin):
    list_filter = ('draft_cell', )
    list_display = ('pick', 'amount', 'draft_cell')
admin.site.register(SlotBonus, SlotBonusAdmin)

class MLBDataAdmin(ModelAdmin):
    list_filter = ('position', 'status', 'draft_cell', 'year')
    list_display = ('position', 'status', 'draft_cell', 'year', 'value')
admin.site.register(MLBData, MLBDataAdmin)

class DOLSalaryAdmin(ModelAdmin):
    search_fields = ('occupation',)
    list_display = ('occupation', 'sal10', 'sal25', 'sal50', 'sal75', 'sal90')
admin.site.register(DOLSalary, DOLSalaryAdmin)

class PrMajorsDataAdmin(ModelAdmin):
    list_filter = ('position', 'status', 'draft_cell')
    list_display = ('position', 'status', 'draft_cell', 'value')
admin.site.register(PrMajorsData, PrMajorsDataAdmin)

class SigningBonusAdmin(ModelAdmin):
    list_filter = ('draft_cell', 'status')
    list_display = ('draft_cell', 'status', 'amount')
admin.site.register(SigningBonus, SigningBonusAdmin)

class ScenarioInline(TabularInline):
    model = Scenario
    readonly_fields = ('anonymous','college','alt','sec','pick','pos','status')
    extra = 0

class VisitorAdmin(ModelAdmin):
    list_display = ('username', 'fullname', 'ip')
    readonly_fields = ('modx_id','username','fullname','ip','user_agent')
    inlines = [ScenarioInline,]
admin.site.register(Visitor, VisitorAdmin)

