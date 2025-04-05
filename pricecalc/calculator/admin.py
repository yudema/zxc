from django.contrib import admin
from .models import Category, Product, PriceModifier, SupportTicket, SupportMessage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'created_at', 'updated_at')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(PriceModifier)
class PriceModifierAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'price_adjustment', 'is_percentage', 'created_at', 'updated_at')
    list_filter = ('product', 'is_percentage')
    search_fields = ('name',)

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('email', 'subject')
    readonly_fields = ('session_id',)

@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'is_staff', 'message', 'created_at')
    list_filter = ('is_staff', 'ticket')
    search_fields = ('message',)
    readonly_fields = ('created_at',)
