import jdatetime
from django import template

register = template.Library()

@register.filter
def to_jalali(value, fmt="%Y/%m/%d"):
    if not value:
        return ""
    try:
        jdate = jdatetime.date.fromgregorian(date=value)
        return jdate.strftime(fmt)
    except:
        return value
