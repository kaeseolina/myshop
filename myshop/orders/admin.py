import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from .models import Order, OrderItem


# Импортируйте вашу модель Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']



def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={opts.verbose_name}.csv'
    writer = csv.writer(response)

    # Получаем поля модели, исключая многие ко многим и один ко многим
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    # Записываем первую строку с заголовками
    writer.writerow([field.verbose_name for field in fields])

    # Записываем строки данных
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)

    return response


export_to_csv.short_description = 'Экспортировать в CSV'

class OrderAdmin(admin.ModelAdmin):
    # ваши другие настройки
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    actions = [export_to_csv]

# Зарегистрируйте вашу модель Order с кастомным админом
admin.site.register(Order, OrderAdmin)
