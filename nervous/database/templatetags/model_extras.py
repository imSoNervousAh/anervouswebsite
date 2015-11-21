from django import template

register = template.Library()

@register.filter(name='unprocessed_messages_count')
def unprocessed_messages_count(account, category):
    return account.unprocessed_messages_count(category)
