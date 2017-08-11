import calendar

from django import template
register = template.Library()

@register.filter(name='month_name')
def month_name(month_number):
    return calendar.month_name[month_number]
