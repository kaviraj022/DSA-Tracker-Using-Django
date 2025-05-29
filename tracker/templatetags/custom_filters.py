from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)

@register.filter
def split(value, delimiter=','):
    """Split a string into a list using the given delimiter."""
    return value.split(delimiter)

@register.filter
def get_difficulties(problems):
    """Get unique difficulties from problems."""
    return sorted(set(item['difficulty'] for item in problems))

@register.filter
def filter_by_difficulty(problems, difficulty):
    """Filter problems by difficulty level."""
    return [item for item in problems if item['difficulty'] == difficulty] 