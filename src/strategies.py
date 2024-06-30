from datetime import datetime, timedelta
from lunarcalendar import Converter, Solar, Lunar, DateNotExist
from .logic.strategy import register


@register
def monthly_9th(now: datetime):
    """每月9号纪念日"""
    target_date = datetime(now.year, now.month, 9)
    if now.day > 9:
        next_month = now.month + 1 if now.month < 12 else 1
        next_year = now.year if now.month < 12 else now.year + 1
        target_date = datetime(next_year, next_month, 9)
    delta = target_date - now
    return delta.total_seconds()


@register
def yearly_birthday(now: datetime):
    """生日"""
    target_date = datetime(now.year, 2, 9)
    if now > target_date:
        target_date = datetime(now.year + 1, 2, 9)
    delta = target_date - now
    return delta.total_seconds()


@register
def hundred_days_since_march_9th(now: datetime):
    """整百纪念日"""
    start = datetime(2022, 4, 9)
    delta = (now - start).days
    next_delta = ((delta // 100) + 1) * 100
    return (start + timedelta(days=next_delta) - now).total_seconds()


@register
def valentines_day(now: datetime):
    """2月14日 情人节"""
    target_date = datetime(now.year, 2, 14)
    if now > target_date:
        target_date = datetime(now.year + 1, 2, 14)
    delta = target_date - now
    return delta.total_seconds()


@register
def mothers_day(now: datetime):
    """3月8日 妇女节"""
    target_date = datetime(now.year, 3, 8)
    if now > target_date:
        target_date = datetime(now.year + 1, 3, 8)
    delta = target_date - now
    return delta.total_seconds()


@register
def singles_day(now: datetime):
    """11月11日 光棍节（情人节）"""
    target_date = datetime(now.year, 11, 11)
    if now > target_date:
        target_date = datetime(now.year + 1, 11, 11)
    delta = target_date - now
    return delta.total_seconds()


@register
def christmas_day(now: datetime):
    """12月25日 圣诞节"""
    target_date = datetime(now.year, 12, 25)
    if now > target_date:
        target_date = datetime(now.year + 1, 12, 25)
    delta = target_date - now
    return delta.total_seconds()


@register
def new_years_day(now: datetime):
    """1月1日 元旦"""
    target_date = datetime(now.year + 1, 1, 1)
    if now > target_date:
        target_date = datetime(now.year + 1, 1, 1)
    delta = target_date - now
    return delta.total_seconds()


@register
def may_20th(now: datetime):
    """5月20日 情人节"""
    target_date = datetime(now.year, 5, 20)
    if now > target_date:
        target_date = datetime(now.year + 1, 5, 20)
    delta = target_date - now
    return delta.total_seconds()


@register
def lunar_new_year_eve(now: datetime):
    """农历12月30 除夕"""
    current_lunar = Converter.Solar2Lunar(Solar(now.year, now.month, now.day))
    try:
        target_lunar = Lunar(current_lunar.year, 12, 30)
        target_solar = Converter.Lunar2Solar(target_lunar)
    except DateNotExist:
        target_lunar = Lunar(current_lunar.year, 12, 29)
        target_solar = Converter.Lunar2Solar(target_lunar)

    target_date = datetime(target_solar.year, target_solar.month, target_solar.day)
    if now > target_date:
        current_lunar = Converter.Solar2Lunar(Solar(now.year + 1, now.month, now.day))
        try:
            target_lunar = Lunar(current_lunar.year, 12, 30)
            target_solar = Converter.Lunar2Solar(target_lunar)
        except DateNotExist:
            target_lunar = Lunar(current_lunar.year, 12, 29)
            target_solar = Converter.Lunar2Solar(target_lunar)
        target_date = datetime(target_solar.year, target_solar.month, target_solar.day)
    delta = target_date - now
    return delta.total_seconds()


@register
def chinese_valentines_day(now: datetime):
    """农历7月7 七夕"""
    current_lunar = Converter.Solar2Lunar(Solar(now.year, now.month, now.day))
    target_lunar = Lunar(current_lunar.year, 7, 7)
    target_solar = Converter.Lunar2Solar(target_lunar)
    target_date = datetime(target_solar.year, target_solar.month, target_solar.day)
    if now > target_date:
        current_lunar = Converter.Solar2Lunar(Solar(now.year + 1, now.month, now.day))
        target_lunar = Lunar(current_lunar.year, 7, 7)
        target_solar = Converter.Lunar2Solar(target_lunar)
        target_date = datetime(target_solar.year, target_solar.month, target_solar.day)
    delta = target_date - now
    return delta.total_seconds()
