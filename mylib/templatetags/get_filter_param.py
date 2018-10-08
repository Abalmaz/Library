from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_param(context):
    get_param = []
    request = context['request']
    for key, v in request.GET.items():
        value_list = request.GET.getlist(key)
        get_param.extend(['%s=%s' % (key, val) for val in value_list if key != 'page' and key != 'order_by'])
    return '&'.join(get_param)