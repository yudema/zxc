from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/products/', views.get_products, name='get_products'),
    path('product/<int:product_id>/modifiers/', views.get_product_modifiers, name='get_product_modifiers'),
    path('calculate/', views.calculate_price, name='calculate_price'),
    
    # URLs для системы поддержки
    path('support/', views.support_chat, name='support_chat'),
    path('support/create/', views.create_ticket, name='create_ticket'),
    path('support/send/', views.send_message, name='send_message'),
    path('support/admin/', views.support_admin, name='support_admin'),
    path('support/admin/send/', views.admin_send_message, name='admin_send_message'),
    path('support/messages/<int:ticket_id>/', views.get_ticket_messages, name='get_ticket_messages'),
] 