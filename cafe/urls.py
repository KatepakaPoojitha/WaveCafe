from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'menu-items', views.MenuItemViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/manage-menu/', views.manage_menu_items, name='manage_menu_items'),
    path('admin-dashboard/add-item/', views.add_menu_item, name='add_menu_item'),
    path('admin-dashboard/edit-item/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('special/', views.special, name='special'),
    path('contact/', views.contact, name='contact'),
    path('stats/', views.stats, name='stats'),
    path('franchise/', views.franchise, name='franchise'),
    path('hot-menu/', views.hot_menu, name='hot_menu'),
    path('ice-menu/', views.ice_menu, name='ice_menu'),
    path('smoothies/', views.smoothie_menu, name='smoothie_menu'),
    path('starters/', views.starter_menu, name='starter_menu'),
    path('combos/', views.combo_menu, name='combo_menu'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('feedback/', views.feedback, name='feedback'),
]
