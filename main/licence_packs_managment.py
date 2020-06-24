import datetime

from general_module.models import Company, Licence


def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return round((dt - epoch).total_seconds() * 1000)


def get_active_licence_pack(company: Company):
    now = datetime.datetime.utcnow()
    licences = Licence.objects.filter(company=company, start_time__lte=now, end_time__gte=now)
    return None if not licences else licences[0]
