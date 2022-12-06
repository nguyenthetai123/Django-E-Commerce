from django.shortcuts import render, redirect
from home.models import *
from home.form import SearchForm
import json
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from product.models import Product, Category, Images, Comment, CommentForm


# Create your views here.

def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    from django.core.paginator import Paginator

    products_slider = Product.objects.all().order_by('id')[:4]  # first 4 products
    paginator = Paginator(products_slider, 10)
    products_picked = Product.objects.all().order_by('?')[:4]  # Random selected 4 products
    products_latest = Product.objects.all().order_by('?')[:4]  # Random selected 4 products
    page = "home"
    context = {
        'setting': setting,
        'home': page,
        'category': category,
        'products_slider': products_slider,
        'products_picked': products_picked,
        'products_latest': products_latest,

    }
    return render(request, 'index.html', context)


def about(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {
        'setting': setting,
        'category': category,
    }
    return render(request, 'about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Your message has ben sent. Thank you for your message.")
            return redirect('contact')
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    form = ContactForm
    context = {
        'setting': setting,
        'form': form,
        'category': category,
    }
    return render(request, 'contactus.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')

    context = {
        'product': product,
        'images': images,
        'category': category,
        'comments': comments, }
    return render(request, 'product_detail.html', context)


def category_products(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    context = {'products': products,
               'setting': setting,
               'category': category
               }
    return render(request, 'category_products.html', context)


def search(request):
    if request.method == 'POST':  # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']  # get form input data
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(
                    title__icontains=query)  # SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)

            category = Category.objects.all()
            context = {'products': products, 'query': query,
                       'category': category}
            return render(request, 'search_products.html', context)

    return redirect('search')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title + " > " + rs.category.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
