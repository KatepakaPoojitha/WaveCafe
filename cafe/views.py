from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, FranchisePackage, Order, OrderItem, Review, Payment
from .forms import ReviewForm, MenuItemForm
import uuid
from django.db.models import Avg, Max, Min, Sum

from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import viewsets, permissions
from .serializers import MenuItemSerializer, OrderSerializer

from .utils import get_current_season

def home(request):
    season_code, season_name, season_end = get_current_season()
    featured_drinks = MenuItem.objects.filter(is_seasonal=False)[:3]
    seasonal_items = MenuItem.objects.filter(season=season_code, is_seasonal=True)
    
    context = {
        'featured_drinks': featured_drinks,
        'seasonal_items': seasonal_items,
        'current_season_name': season_name,
        'season_end_month': season_end
    }
    return render(request, 'cafe/home.html', context)

def menu(request):
    # Consolidate all categories for the unified menu
    hot_drinks = MenuItem.objects.filter(category='DRINK', temp_type='HOT')
    ice_drinks = MenuItem.objects.filter(category='DRINK', temp_type='COLD')
    smoothies = MenuItem.objects.filter(category='SMOOTHIE')
    starters = MenuItem.objects.filter(category='STARTER')
    combos = MenuItem.objects.filter(category='COMBO')
    
    season_code, season_name, _ = get_current_season()
    seasonal_items = MenuItem.objects.filter(season=season_code, is_seasonal=True)
    
    context = {
        'hot_drinks': hot_drinks,
        'ice_drinks': ice_drinks,
        'smoothies': smoothies,
        'starters': starters,
        'combos': combos,
        'seasonal_items': seasonal_items,
        'current_season_name': season_name
    }
    return render(request, 'cafe/menu.html', context)

def about(request):
    return render(request, 'cafe/about.html')

def special(request):
    # Fetching special items using the boolean flag
    special_drinks = MenuItem.objects.filter(is_special=True)
    return render(request, 'cafe/special.html', {'special_drinks': special_drinks})

def stats(request):
    total_drinks = MenuItem.objects.count()
    avg_price = MenuItem.objects.aggregate(Avg('price'))['price__avg'] or 0
    max_price_item = MenuItem.objects.order_by('-price').first()
    special_count = MenuItem.objects.filter(is_special=True).count()
    
    # Mock data for "States" presence as requested
    branch_locations = [
        {'state': 'Maharashtra', 'cities': ['Mumbai', 'Pune', 'Nagpur'], 'count': 5},
        {'state': 'Karnataka', 'cities': ['Bangalore', 'Mysore'], 'count': 3},
        {'state': 'Tamil Nadu', 'cities': ['Chennai', 'Coimbatore'], 'count': 2},
        {'state': 'Delhi', 'cities': ['New Delhi'], 'count': 4},
        {'state': 'Goa', 'cities': ['Panaji'], 'count': 1},
    ]
    
    context = {
        'total_drinks': total_drinks,
        'avg_price': round(avg_price, 2),
        'max_price': max_price_item,
        'special_count': special_count,
        'branch_locations': branch_locations,
        'total_branches': sum(loc['count'] for loc in branch_locations)
    }
    return render(request, 'cafe/stats.html', context)

def contact(request):
    return render(request, 'cafe/contact.html')

def franchise(request):
    packages = FranchisePackage.objects.all()
    return render(request, 'cafe/franchise.html', {'packages': packages})

def hot_menu(request):
    hot_drinks = MenuItem.objects.filter(temp_type='HOT', category='DRINK')
    return render(request, 'cafe/hot_menu.html', {'hot_drinks': hot_drinks})

def ice_menu(request):
    ice_drinks = MenuItem.objects.filter(temp_type='COLD', category='DRINK')
    return render(request, 'cafe/ice_menu.html', {'ice_drinks': ice_drinks})

def smoothie_menu(request):
    smoothies = MenuItem.objects.filter(category='SMOOTHIE')
    return render(request, 'cafe/smoothie_menu.html', {'smoothies': smoothies})

def starter_menu(request):
    # Fetch items for each section
    shawarma_rolls = MenuItem.objects.filter(menu_section='SHAWARMA_ROLL')
    shawarma_plates = MenuItem.objects.filter(menu_section='SHAWARMA_PLATE')
    grilled_chicken = MenuItem.objects.filter(menu_section='GRILLED_CHICKEN')
    bbq_chicken = MenuItem.objects.filter(menu_section='BBQ_CHICKEN')
    tandoori_chicken = MenuItem.objects.filter(menu_section='TANDOORI_CHICKEN')
    veg_starters = MenuItem.objects.filter(menu_section='VEG_STARTERS')

    context = {
        'shawarma_rolls': shawarma_rolls,
        'shawarma_plates': shawarma_plates,
        'grilled_chicken': grilled_chicken,
        'bbq_chicken': bbq_chicken,
        'tandoori_chicken': tandoori_chicken,
        'veg_starters': veg_starters,
        'loaded_fries': MenuItem.objects.filter(menu_section='LOADED_FRIES'),
        'fusion_chaats': MenuItem.objects.filter(menu_section='FUSION_CHAAT'),
        'family_boxes': MenuItem.objects.filter(menu_section='FAMILY_BOX'),
        'party_packs': MenuItem.objects.filter(menu_section='PARTY_PACK'),
    }
    return render(request, 'cafe/starter_menu.html', context)

def combo_menu(request):
    combos = MenuItem.objects.filter(category='COMBO')
    return render(request, 'cafe/combos.html', {'combos': combos})

def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart_detail')

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        if cart[str(item_id)] > 1:
            cart[str(item_id)] -= 1
        else:
            del cart[str(item_id)]
    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for item_id, quantity in cart.items():
        item = get_object_or_404(MenuItem, id=item_id)
        subtotal = item.price * quantity
        total_price += subtotal
        cart_items.append({
            'item': item,
            'quantity': quantity,
            'subtotal': subtotal
        })
    
    return render(request, 'cafe/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('menu')
        
    total_price = 0
    for item_id, quantity in cart.items():
        item = get_object_or_404(MenuItem, id=item_id)
        total_price += item.price * quantity
        
    if request.method == 'POST':
        # Simulate payment processing
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        # Card details are processed here but not stored for security
        
        order = Order.objects.create(
            customer_name=name,
            email=email,
            address=address,
            total_price=total_price,
            status='PAID'
        )
        
        # Create Payment Record
        Payment.objects.create(
            order=order,
            method='CARD', # Mocked for now
            transaction_id=str(uuid.uuid4()).split('-')[0].upper(),
            amount=total_price,
            status='SUCCESS'
        )
        
        for item_id, quantity in cart.items():
            item = get_object_or_404(MenuItem, id=item_id)
            OrderItem.objects.create(
                order=order,
                menu_item=item,
                quantity=quantity,
                price=item.price
            )
            
        request.session['cart'] = {} # Clear cart
        return redirect('payment_success')
        
    return render(request, 'cafe/checkout.html', {'total_price': total_price})

def payment_success(request):
    return render(request, 'cafe/payment_success.html')

def feedback(request):
    reviews = Review.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback')
    else:
        form = ReviewForm()
    
    return render(request, 'cafe/feedback.html', {
        'form': form,
        'reviews': reviews
    })

# API ViewSets
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

# Admin Dashboard
@staff_member_required
def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(status='PAID').aggregate(Sum('total_price'))['total_price__sum'] or 0
    pending_orders = Order.objects.filter(status='PENDING').count()
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
    }
    return render(request, 'cafe/admin_dashboard.html', context)

@staff_member_required
def manage_menu_items(request):
    items = MenuItem.objects.all().order_by('category', 'name')
    return render(request, 'cafe/manage_menu.html', {'items': items})

@staff_member_required
def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_menu_items')
    else:
        form = MenuItemForm()
    return render(request, 'cafe/add_item.html', {'form': form, 'title': 'Add New Menu Item'})

@staff_member_required
def edit_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('manage_menu_items')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'cafe/add_item.html', {'form': form, 'title': 'Edit Menu Item'})

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
        
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                next_url = request.GET.get('next', 'admin_dashboard')
                return redirect(next_url)
            else:
                error = "Access denied. Only staff members can login here."
        else:
            error = "Invalid username or password. Please try again."
            
    return render(request, 'cafe/login.html', {'error': error})

def admin_logout(request):
    logout(request)
    return redirect('home')




