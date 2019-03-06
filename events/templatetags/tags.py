from django import template

register = template.Library()

@register.filter()
def convert_to_username(email):
    return email.split("@")[0]