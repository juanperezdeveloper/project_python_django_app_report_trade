from django.contrib.humanize.templatetags.humanize import intcomma
from django import template

register = template.Library()

@register.filter()
def currency(dollars):
    dollars = float(dollars)
    return "$%s" % (intcomma(int(dollars)))

@register.filter()
def percentage(decimal):
    decimal = float(decimal) * 100.0
    return "%0.0f%%" % (decimal,)