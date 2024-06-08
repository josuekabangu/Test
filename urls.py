from django.urls import path
from . import views

urlpatterns = [
    # URL pour la liste des produits avec des options de tri
    path('', views.product_list, name='product_list'),

    # URL pour la liste des catégories
    path('categories/', views.category_list, name='category_list'),

    # URL pour les détails d'un produit spécifique
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),

    # URL pour afficher le panier de l'utilisateur
    path('cart/', views.cart_detail, name='cart_detail'),

    # URL pour ajouter un produit au panier
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # URL pour supprimer un produit du panier
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]
