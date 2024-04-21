from django.db import models
from django.utils.safestring import mark_safe
# Create your models here.

class productdetail(models.Model):
    productname = models.CharField(max_length=40)
    productprice = models.FloatField()
    productdesc =  models.TextField()
    productimg = models.ImageField(upload_to="photos")
    status = models.BooleanField(default=True)

    def product_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.productimg.url))

    product_photo.allow_tags = True

    def __str__(self):
        return self.productname

class registertable(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.BigIntegerField()
    password = models.CharField(max_length=40)
    role = models.CharField(max_length=40)
    profilepic = models.ImageField(upload_to="photos")

    def profile_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.profilepic.url))

    profile_photo.allow_tags = True

    def __str__(self):
        return self.name

class carttable(models.Model):
    userid = models.ForeignKey(registertable,on_delete=models.CASCADE)
    productid = models.ForeignKey(productdetail,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    totalamount = models.IntegerField()
    cartstatus = models.IntegerField() # 1- item added , 2- order placed , 0 - item removed
    orderid = models.IntegerField()

class ordertable(models.Model):
    userid = models.ForeignKey(registertable,on_delete=models.CASCADE)
    finaltotal = models.IntegerField()
    phoneno = models.IntegerField()
    address = models.TextField()
    paymode = models.CharField(max_length=40)
    timestamp = models.DateTimeField(auto_now_add=True)

