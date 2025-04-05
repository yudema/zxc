from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from .models import Category, Product, PriceModifier, SupportTicket, SupportMessage
from decimal import Decimal
import json

@cache_page(60 * 15)
def index(request):
    if not request.session.session_key:
        request.session.create()
    
    products = Product.objects.select_related('category').all()
    products_data = []
    
    for product in products:
        modifiers = PriceModifier.objects.filter(product_id=product.id)
        modifiers_data = [{
            'id': modifier.id,
            'name': modifier.name,
            'price_adjustment': float(modifier.price_adjustment),
            'is_percentage': modifier.is_percentage
        } for modifier in modifiers]
        
        products_data.append({
            'id': product.id,
            'name': product.name,
            'category': product.category.name,
            'description': product.description,
            'base_price': float(product.base_price),
            'modifiers': modifiers_data
        })
    
    context = {
        'products': products_data,
    }
    return render(request, 'calculator/index.html', context)

@require_http_methods(["GET"])
def get_products(request, category_id):
    try:
        products = Product.objects.filter(category_id=category_id)
        products_data = {}
        
        for product in products:
            modifiers = PriceModifier.objects.filter(product_id=product.id)
            modifiers_data = [{
                'id': modifier.id,
                'name': modifier.name,
                'price_adjustment': float(modifier.price_adjustment),
                'is_percentage': modifier.is_percentage
            } for modifier in modifiers]
            
            products_data[str(product.id)] = {
                'id': product.id,
                'name': product.name,
                'base_price': float(product.base_price),
                'description': product.description,
                'modifiers': modifiers_data
            }
            
        return JsonResponse({
            'success': True,
            'products': products_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@require_http_methods(["GET"])
def get_product_modifiers(request, product_id):
    try:
        modifiers = PriceModifier.objects.filter(product_id=product_id)
        data = []
        for modifier in modifiers:
            data.append({
                'id': modifier.id,
                'name': modifier.name,
                'price_adjustment': float(modifier.price_adjustment),
                'is_percentage': modifier.is_percentage
            })
        return JsonResponse({'success': True, 'modifiers': data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_http_methods(["POST"])
def calculate_price(request):
    try:
        product_id = request.POST.get('product_id')
        modifier_ids = request.POST.getlist('modifiers[]')
        
        product = Product.objects.get(id=product_id)
        final_price = float(product.base_price)
        
        # Применяем модификаторы
        for modifier_id in modifier_ids:
            modifier = PriceModifier.objects.get(id=modifier_id)
            if modifier.is_percentage:
                final_price *= (1 + float(modifier.price_adjustment) / 100)
            else:
                final_price += float(modifier.price_adjustment)
        
        return JsonResponse({
            'success': True,
            'final_price': round(final_price, 2),
            'base_price': float(product.base_price)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

def support_chat(request):
    # Проверяем параметр new_ticket
    if request.GET.get('new_ticket'):
        # Если запрошено создание нового тикета, сбрасываем сессию
        request.session.flush()
        request.session.create()
        request.session.save()
        return redirect('calculator:support_chat')
    
    # Убедимся, что у пользователя есть сессия
    if not request.session.session_key:
        request.session.create()
        request.session.save()
    
    session_id = request.session.session_key
    
    # Получаем или создаем тикет для текущей сессии
    ticket = SupportTicket.objects.filter(session_id=session_id).first()
    
    context = {
        'ticket': ticket,
        'session_id': session_id,
        'messages': [] if not ticket else ticket.messages.all().order_by('created_at')
    }
    return render(request, 'calculator/support_chat.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def create_ticket(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        
        if not all([email, subject, message]):
            return JsonResponse({
                'success': False,
                'error': 'Все поля обязательны для заполнения'
            }, status=400)
        
        # Создаем тикет и первое сообщение
        ticket = SupportTicket.objects.create(
            session_id=request.session.session_key,
            email=email,
            subject=subject
        )
        
        SupportMessage.objects.create(
            ticket=ticket,
            message=message,
            is_staff=False
        )
        
        return JsonResponse({
            'success': True,
            'ticket_id': ticket.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    try:
        # Получаем данные из POST или JSON в теле
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            ticket_id = data.get('ticket_id')
            message = data.get('message')
        else:
            ticket_id = request.POST.get('ticket_id')
            message = request.POST.get('message')
        
        if not all([ticket_id, message]):
            return JsonResponse({
                'success': False,
                'error': 'Необходимо указать ID тикета и сообщение'
            }, status=400)
        
        # Проверка наличия тикета - если не найден, возвращаем дополнительную информацию для отладки
        try:
            ticket = SupportTicket.objects.get(id=ticket_id)
        except SupportTicket.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Тикет с ID {ticket_id} не найден',
                'session_id': request.session.session_key
            }, status=404)
            
        # Если тикет существует, но не соответствует текущей сессии - создаем новое сообщение все равно для отладки
        support_message = SupportMessage.objects.create(
            ticket=ticket,
            message=message,
            is_staff=False
        )
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': support_message.id,
                'message': support_message.message,
                'is_staff': support_message.is_staff,
                'created_at': support_message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

def support_admin(request):
    tickets = SupportTicket.objects.all().order_by('-created_at')
    return render(request, 'calculator/support_admin.html', {'tickets': tickets})

@csrf_exempt
@require_http_methods(["POST"])
def admin_send_message(request):
    try:
        data = json.loads(request.body)
        ticket_id = data.get('ticket_id')
        message = data.get('message')
        new_status = data.get('status')
        
        if not all([ticket_id, message]):
            return JsonResponse({
                'success': False,
                'error': 'Необходимо указать ID тикета и сообщение'
            }, status=400)
        
        ticket = SupportTicket.objects.get(id=ticket_id)
        
        if new_status and new_status in dict(SupportTicket.STATUS_CHOICES):
            ticket.status = new_status
            ticket.save()
        
        support_message = SupportMessage.objects.create(
            ticket=ticket,
            message=message,
            is_staff=True
        )
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': support_message.id,
                'message': support_message.message,
                'is_staff': support_message.is_staff,
                'created_at': support_message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
        
    except SupportTicket.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Тикет не найден'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@csrf_exempt
def get_ticket_messages(request, ticket_id):
    try:
        ticket = SupportTicket.objects.get(id=ticket_id)
        messages = ticket.messages.all().order_by('created_at')
        
        return JsonResponse({
            'success': True,
            'ticket_status': ticket.status,
            'messages': [{
                'id': msg.id,
                'message': msg.message,
                'is_staff': msg.is_staff,
                'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
            } for msg in messages]
        })
        
    except SupportTicket.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Тикет не найден'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
