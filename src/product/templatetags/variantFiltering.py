from django import template
from datetime import tzinfo, timedelta, datetime


register = template.Library()

@register.filter
def findVariant(variant, product):
    return variant.filter(product = product)

@register.filter
def findSubCatarogy(allProductVariants, variant):
    return allProductVariants.filter(variant = variant)


ZERO = timedelta(0)

class UTC(tzinfo):
  def utcoffset(self, dt):
    return ZERO
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return ZERO

utc = UTC()

def date_diff_in_seconds(dt2, dt1):
  timedelta = dt2 - dt1
  return timedelta.days * 24 * 3600 + timedelta.seconds

def dhms_from_seconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    years, days = divmod(days, 365)
    res = ""
    if years:
        res += f"{years} year{'' if years == 1 else 's'} "
    if days:
        res += f"{days} day{'' if days == 1 else 's'} "
    if hours:
        res += f"{hours} hour{'' if hours == 1 else 's'} "
    if minutes:
        res += f"{minutes} minute{'' if minutes == 1 else 's'} "
    if seconds:
        res += f"{seconds} second{'' if seconds == 1 else 's'} "
    return res

@register.filter
def duration(time):
    return dhms_from_seconds(date_diff_in_seconds(datetime.now(utc), time))