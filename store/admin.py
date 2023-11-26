from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.utils.html import format_html,urlencode
from django.urls import reverse
from . import models
from tags.models import Tag, TaggedItem



@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        #reverse('admin:name_of_app_model_page)
        #basically, when you click on the products count, we want to take the user to the products page
        #with the products sorted by the current collection
        url = (
            reverse('admin:store_product_changelist')
            +'?'
            + urlencode({
                'collection__id':collection.id
            })
            )
        return format_html("<a href='{}'>{}</a>",   url , collection.products_count)
    
    #there is no attribute called products_count on the collection model 
    #so we intercept the query set and annotate it with this field
    #we use an inbuilt method
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self,request, model_admin):
        return [
            ('<10','Low')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)



@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    #form fields
    #fields =['inventory','unit_price']
    #readonly_fields
    #exclude['inventory'] -- we use this to customise what fields should be excluded in the form
    #
    #lets say we want the slug field to be automatically populated as we type the title of the product
    #it only updates if you havent touched the title field before
    prepopulated_fields = {
        'slug':['title']
    }

    #autocomplete fields
    autocomplete_fields = ['collection']
    search_fields = ['title']
    actions = ['clear_inventory']
    list_display = ['title','unit_price','inventory_status','collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_filter = ['collection','last_update', InventoryFilter]
    list_select_related = ['collection']

    def collection_title(self, product):
        return product.collection.title

    #django doesnt know how to sort this column since it is custom so we add a decorator to this method
    #to specify the column to use for the sorting
    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    #custom bulk actions
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        #message to show to user after action
        #You can add messages.ERROR etc to show differrent types of messages
        # success or error self.message_user(request, f'{updated_count} products were successfully updated', messages.ERROR)
        self.message_user(request, f'{updated_count} products were successfully updated')


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership','order_count']
    list_editable = ['membership']
    list_per_page = 10
    #we just add a lookuptype of starts_with to make sure that we are finding values which start with our search phrase
    #the "i" stands for case insensitive. We remove the i if we want case sensitive
    search_fields = ['first_name__istartswith','last_name__istartswith']
    
    def order_count(self,customer):
        url = reverse('admin:store_order_changelist') +'?' + urlencode({'customer__id':customer.id})
        return format_html("<a href='{}'>{}</a>",url, customer.order_count)

    def get_queryset(self,request):
        return super().get_queryset(request).prefetch_related("order_set").annotate(order_count=Count('order'))


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    #by default, you will see 3 placeholder rows for the order's items
    #if you dont want to see that you can set extra=0
    extra = 0
    min_num  = 1
    max_num = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at','payment_status','customer_name']
    list_related = ['customer']
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']

    def customer_name(self, order):
        return f"{order.customer.first_name} {order.customer.last_name}"

