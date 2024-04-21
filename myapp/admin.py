from django.contrib import admin
from .models import productdetail , registertable , carttable , ordertable
# Register your models here.

class showproducts(admin.ModelAdmin):
    list_display = ["productname","productprice","productdesc","product_photo","status"]


admin.site.register(productdetail,showproducts)

class showregister(admin.ModelAdmin):
    list_display = ["name","email","phone","role","profile_photo"]

admin.site.register(registertable,showregister)

class showcart(admin.ModelAdmin):
    list_display = ["userid","productid","quantity","totalamount","cartstatus","orderid"]

admin.site.register(carttable,showcart)

class showorder(admin.ModelAdmin):
    list_display = ["id","userid","finaltotal","phoneno","address","paymode","timestamp"]

admin.site.register(ordertable,showorder)