from django import template

register = template.Library()

@register.filter
def findVariant(variant, product):
    return variant.filter(product = product)

@register.filter
def findSubCatarogy(allProductVariants, variant):
    return allProductVariants.filter(variant = variant)