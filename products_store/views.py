from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment, Product, Basket, Product_order, Product_type
from .forms import UserRegisterForm, UserUpdateDetailsForm, User_profileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

def index(request):
    return render(request, 'products_store/index.html')

def tools(request):
    category_slug = request.GET.get('category')

    if category_slug:
        products = Product.objects.filter(prod_type__slug=category_slug)
    else:
        products = Product.objects.all()

    context = {
        'comments': Comment.objects.all(),
        'products': products,
        'categories': Product_type.objects.all(),
        'current_category': category_slug,
    }
    return render(request, 'products_store/tools.html', context)

def contact(request):
    return render(request, 'products_store/contact.html')

def delivery(request):
    return render(request, 'products_store/delivery.html')

def reg_form(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Registration completed {username}! Please login.')
            return redirect('products_store-login')
    else:
        form = UserRegisterForm()

    return render(request, 'products_store/register.html', {'form':form})

@login_required
def basket_page(request):
    order, created = Basket.objects.get_or_create(user=request.user)

    return render(request, 'products_store/basket.html', {'order':order})

@login_required
def profile_page(request):
    if request.method == 'POST':
        uud_form = UserUpdateDetailsForm(request.POST, instance=request.user)
        upu_form = User_profileUpdateForm(request.POST, request.FILES, instance=request.user.user_profile)

        if uud_form.is_valid() and upu_form.is_valid():
            uud_form.save()
            upu_form.save()
            messages.success(request, f'User details successfuly updated!')
            return redirect('products_store-profile_page')
    else:
        uud_form = UserUpdateDetailsForm(instance=request.user)
        upu_form = User_profileUpdateForm(instance=request.user.user_profile)

    content = {
        'uud_form': uud_form,
        'upu_form': upu_form
    }
    return render(request, 'products_store/profile.html', content)

def comments_view(request):
    com_consist = {
        'comments': Comment.objects.all(),
    }
    return render(request, 'products_store/comments_page.html', com_consist)

class CommentsList(ListView):
    model = Comment
    template_name = 'products_store/tools.html'
    context_object_name = 'comments'
    ordering = ['-commented_date']

class CommentsDetail(DetailView):
    model = Comment

class CommentsCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['comname', 'comtext']

    def form_valid(self, form):
        form.instance.comwriter = self.request.user
        return super().form_valid(form)
    
class CommentsUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['comname', 'comtext']

    def form_valid(self, form):
        form.instance.comwriter = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.comwriter:
            return True
        return False
    
class CommentsDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = 'products_store-comments-view'

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.comwriter:
            return True
        return False

class Power_tools(ListView):
    model = Product
    template_name = 'products_store/tools.html'
    context_object_name = 'products'
    ordering = ['prod_name']

@login_required
def add_to_basket(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Basket.objects.get_or_create(user=request.user)
    
    order_item, created = Product_order.objects.get_or_create(order=order, product=product)
    if not created:
        order_item.quantity += 1
    order_item.save()

    return redirect('products_store-basket_page')
    
@login_required
def basket_remove(request, product_id):
    order = get_object_or_404(Basket, user=request.user)
    order_item = get_object_or_404(Product_order, order=order, product_id=product_id)
    order_item.delete()

    return redirect('products_store-basket_page')
