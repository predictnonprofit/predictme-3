from django import template
register = template.Library()


@register.filter
def sub_records(all_recs, allowed_recs):
    if all_recs and allowed_recs:
        return all_recs - allowed_recs


@register.filter
def extra_fee_records(records_total):
    if records_total:
        return float(records_total * 0.50) 
