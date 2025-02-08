from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(field, css_class):
    """Adds a CSS class to a form field's widget."""
    if hasattr(field, 'field'):  # Check if it's a BoundField (important!)
        return field.as_widget(attrs={'class': css_class})
    return field  # Return the field unchanged if it's not a BoundField