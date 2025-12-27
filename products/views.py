from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def custom_404(request, exception):
    """Redirige al home si se accede a una ruta inexistente."""
    return redirect('home')

def custom_403(request, exception=None):
    return render(request, '403.html', status=403)

# --- LISTAR PRODUCTOS ---
@login_required
@admin_required
def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(category__name__icontains=query)
    ).order_by('-id')

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {'page_obj': page_obj})


# --- CREAR PRODUCTO ---
@login_required
@admin_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Producto agregado correctamente.')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})


# --- EDITAR PRODUCTO ---
@login_required
@admin_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, '✏️ Producto actualizado correctamente.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form})


# --- ELIMINAR PRODUCTO ---
@login_required
@admin_required
@require_POST
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.warning(request, '🗑️ Producto eliminado.')
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})


# --- LISTAR CATEGORÍAS ---
@login_required
@admin_required
def category_list(request):
    query = request.GET.get('q', '')
    categories = Category.objects.filter(name__icontains=query).order_by('name')

    paginator = Paginator(categories, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'categories/category_list.html', {
        'page_obj': page_obj,
        'query': query
    })


# --- CREAR CATEGORÍA ---
@login_required
@admin_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Categoría creada exitosamente.")
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'categories/category_form.html', {'form': form})


# --- EDITAR CATEGORÍA ---
@login_required
@admin_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, '✏️ Categoría actualizada exitosamente.')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'categories/category_form.html', {'form': form})

# --- ELIMINAR CATEGORÍA ---
@login_required
@admin_required
@require_POST
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.warning(request, '🗑️ Categoría eliminada.')
        return redirect('category_list')
    return render(request, 'categories/category_confirm_delete.html', {'category': category})

@login_required
def home(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    recent_products = Product.objects.order_by('-id')[:5]
    category_data = Category.objects.annotate(num_products=Count('products'))

    return render(request, 'products/home.html', {
        'total_products': total_products,
        'total_categories': total_categories,
        'recent_products': recent_products,
        'category_data': category_data,
        'now': timezone.now(),
    })

@login_required
@admin_required
def user_list(request):
    users = User.objects.all().order_by('id')
    return render(request, 'users/user_list.html', {'users': users})

@login_required
@admin_required
def user_create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('user_create')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ese nombre de usuario ya existe.")
            return redirect('user_create')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Usuario creado con éxito.")
        return redirect('user_list')

    return render(request, 'users/user_create.html')

@login_required
@admin_required
@require_POST
def user_toggle_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, "Estado del usuario actualizado.")
    return redirect('user_list')

def logout_user(request):
    logout(request)
    return redirect('login')
