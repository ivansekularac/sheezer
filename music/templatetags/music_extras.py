from django import template
import datetime

register = template.Library()


# Perform Song duration calc
@register.filter
def duration(duration):
    """Converts duration from seconds to human-friendly mm:ss format"""
    duration = str(datetime.timedelta(seconds = duration))
    return duration[-5:]

# Perform Popularity conversion to float number
@register.filter
def popularity(value):
    """Converts rank(popularity) to round number with one decimal place"""
    return str(round(int(value) / 100000, 1))