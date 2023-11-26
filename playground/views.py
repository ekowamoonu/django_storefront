from django.forms import DecimalField
from django.shortcuts import render
from django.db.models import Q, F, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Min, Max, Sum, Avg
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem

from store.models import *

# Create your views here.
def say_hello(request):
  
#   query_set = Order.objects.aaggregate(Count('*'))
#   product_one_sold = OrderItem.objects.filter(product__id=1).aggregate(prod_sold=Sum('quantity'))
#   customer_one_orders = Order.objects.filter(customer__id=1).aggregate(total_orders=Count('*'))
#   min_max_avg_price = Product.objects.filter(collection__id=3).aggregate(min_price=Min('unit_price'), max_price=Max('unit_price'),avg_price=Avg('unit_price'))
  
#    customers_with_last_order_id = Customer.objects.prefetch_related("order_set").latest("order__placed_at")
#    collections_and_count_of_their_products = Collection.objects.annotate(products_count = Count('product'))
#    query_results = {
#     'customers_with_last_order_id':  customers_with_last_order_id,
#     'collections_and_count_of_their_products': collections_and_count_of_their_products
#    }
   # order = Order()
   # order.customer_id=1
   # order.save()

   # item = OrderItem()
   # item.order = order
   # item.product_id=1
   # item.quantity =1 
   # item.unit_price = 10
   # item.save()

   # discounted = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
   # query_set = Product.objects.annotate(discounted_price=discounted)
 


   

   return render(request, 'hello.html',{'name':None})



