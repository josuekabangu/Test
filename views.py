from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Cart, CartItem
import logging

# Configurez le journal pour enregistrer les messages de débogage
logger = logging.getLogger(__name__)

# Afficher tous les produits avec des options de tri
def product_list(request):
    products = Product.objects.all()

    # Exemple de tri basé sur les paramètres de la requête
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == 'name':
        products = products.order_by('name')
    # Ajoutez d'autres options de tri si nécessaire

    return render(request, 'shop/product_list.html', {'products': products})

# Afficher la liste des catégories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/category_list.html', {'categories': categories})

# Afficher les détails d'un produit
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

# Afficher le panier d'un utilisateur
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shop/cart_detail.html', {'cart': cart})

# Ajouter un produit au panier
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        # L'article a été créé, donc la quantité par défaut est déjà 1.
        messages.success(request, "Produit ajouté au panier avec succès!")
    else:
        # L'article existe déjà dans le panier, augmentez la quantité.
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, "Quantité du produit mise à jour avec succès!")
        else:
            messages.error(request, "Quantité du produit non disponible en stock.")

    return redirect('cart_detail')

# Supprimer un produit du panier
@login_required
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, product_id=product_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.info(request, "La quantité du produit a été réduite.")
    else:
        cart_item.delete()
        messages.info(request, "Le produit a été retiré de votre panier.")
    return redirect('cart_detail')

# Modifier la quantité d'un produit dans le panier
@login_required
def change_item_quantity(request, product_id, quantity):
    cart_item = get_object_or_404(CartItem, product_id=product_id, cart__user=request.user)
    product = cart_item.product
    if 0 < quantity <= product.stock:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "La quantité du produit a été mise à jour.")
    else:
        messages.error(request, "Quantité demandée non disponible en stock.")
    return redirect('cart_detail')
