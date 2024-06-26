# orders/translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import Order, OrderItem

@register(Order)
class OrderTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'address', ...)  # Укажите поля для перевода

@register(OrderItem)
class OrderItemTranslationOptions(TranslationOptions):
    fields = ('product',)  # Укажите поля для перевода
