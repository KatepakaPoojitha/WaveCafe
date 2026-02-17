from django.contrib import admin
from .models import MenuItem, FranchisePackage, Order, OrderItem, Review

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]

admin.site.register(MenuItem)
admin.site.register(FranchisePackage)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
