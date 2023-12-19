from django.contrib import admin
from .models import Product, Customer , Cart , Payment , OrderPlaced , Wishlist
# from django.utls.html import format_html
# from django.urls import reverse
# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','discounted_price','category','product_image']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','zipcode']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):    
    list_display = ['id','user','product','quantity']
    # def product(self,obj):
    #     link = reverse("admin:ecomerce_product_change",args=[object.product.pk])
    #     return format_html("<a href="{}">{}</a>",link,obj.Product.title)
@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):    
    list_display = ['id','user','razorpay_order_id','razorpay_payment_status','razorpay_payment_id', 'paid' ]   

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):    
    list_display = ['id','user','customer','product','quantity', 'ordered_date', 'status', 'payment' ]   

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):    
    list_display = ['id','user','product']   

