from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django_filters.views import FilterView
from django.db import models
from .models import Category, Product, Review
from .filters import ProductFilter
from .forms import ReviewForm

class HomeView(ListView):
    model = Product
    template_name = 'shop/home.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['featured_products'] = Product.objects.filter(is_active=True)[:6]
        return context


class CategoryView(ListView):
    model = Product
    template_name = 'shop/category.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=self.category, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context


class ProductFilterView(FilterView):
    model = Product
    filterset_class = ProductFilter
    template_name = 'shop/products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        context['review_form'] = ReviewForm()
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(pk=self.object.pk)[:4]
        return context


@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.author = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('shop:product', slug=slug)
    else:
        form = ReviewForm()

    return render(request, 'shop/add_review.html', {'form': form, 'product': product})


def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(
            models.Q(name__icontains=query) | 
            models.Q(description__icontains=query)
        )

    context = {
        'products': products,
        'query': query,
        'categories': Category.objects.all(),
    }
    return render(request, 'shop/search.html', context)
