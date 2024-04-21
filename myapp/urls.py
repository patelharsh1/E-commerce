from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('showproduct',views.showproductpage,name="show"),
    path('addproduct',views.addproductpage,name="add"),
    path('fetchproductdata',views.fetchproductdata,name="fetchproductdata"),
    path('singleproductpage/<int:pid>',views.singleproductpage,name="singleproductpage"),
    path('signup', views.signuppage, name="signuppage"),
    path('fetchregisterdata', views.fetchregisterdata, name="fetchregisterdata"),
    path('', views.loginpage, name="login"),
    path('checklogindata', views.checklogindata, name="checklogindata"),
    path('logout', views.logout, name="logout"),
    path('manageproduct', views.manageproduct, name="manageproduct"),
    path('delete/<int:id>', views.deleteproduct, name="deleteproduct"),
    path('addtocart', views.addtocart, name="addtocart"),
    path('showcart', views.showcart, name="showcart"),
    path('removeitem/<int:id>', views.removeitem, name="removeitem"),
    path('increaseitem/<int:id>', views.increaseitem, name="increaseitem"),
    path('decreaseitem/<int:id>', views.decreaseitem, name="decreaseitem"),
    path('findproduct',views.findproduct),
    path('placeorder',views.placeorder),
    path('showorders',views.yourorders),
    path('yourdetailorder/<int:id>',views.yourdetailorder),
    path('forgotpage',views.forgotpage),
    path('forgotpassword',views.forgotpassword),
    path('changepass',views.changepasswordpage),
    path('updatepass',views.updatepass),
]
