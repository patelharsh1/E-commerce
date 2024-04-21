from django.db.models import Sum
from django.shortcuts import render , redirect
from .models import productdetail , registertable , carttable , ordertable
from django.contrib import messages
# Create your views here.
def showproductpage(request):
    getalldata = productdetail.objects.all()
    context = {
        "prodata":getalldata
    }

    return render(request,"showproduct.html",context)
def addproductpage(request):
    return render(request,"addproduct.html")
def fetchproductdata(request):
    proname = request.POST.get("pname")
    proprice = request.POST.get("pprice")
    prodesc = request.POST.get("pdesc")
    proimg = request.FILES["pimage"]
    storedata = productdetail(productname=proname,productprice=proprice,productdesc=prodesc,productimg=proimg)
    storedata.save()
    return redirect("/showproduct")

def singleproductpage(request , pid):
    print(pid)
    getsingledata = productdetail.objects.get(id=pid)
    context = {
        "data":getsingledata
    }
    return render(request,"singleproduct.html",context)

def signuppage(request):
    return render(request,"Signup.html")
def fetchregisterdata(request):
    username = request.POST.get("uname")
    useremail = request.POST.get("uemail")
    userphone = request.POST.get("uphone")
    userpass = request.POST.get("upassword")
    userrole = request.POST.get("urole")
    userdp = request.FILES["udp"]
    try:
        checkemail = registertable.objects.get(email=useremail)
    except:
        checkemail = None
    if checkemail is None:
        storedata = registertable(name=username,email=useremail,phone=userphone,password=userpass,role=userrole,profilepic=userdp)
        storedata.save()
        messages.success(request,"Registered Successfully.")
    else:
        messages.error(request,"You are already Registered. Please login")
    return render(request,"Signup.html")

def loginpage(request):
    return render(request,"Login.html")

def checklogindata(request):
    useremail = request.POST.get("uemail") # a@B.COM , 88777887766
    userpassword = request.POST.get("upassword")

    try:
        checkuser = registertable.objects.get(email=useremail, password=userpassword)
        request.session["logid"] = checkuser.id
        request.session["logname"] = checkuser.name
        request.session["logrole"] = checkuser.role
        request.session.save()
    except:
        checkuser = None

    if checkuser is not None:
        return redirect("/showproduct")
    else:
        # messages.error(request,"Invalid email or password. please try again")
        # check data combination for phone and password
        try:
            checkquery = registertable.objects.get(phone=useremail,password=userpassword)
            request.session["logid"] = checkquery.id
            request.session["logname"] = checkquery.name
            request.session["logrole"] = checkquery.role
            request.session.save()
        except:
            checkquery = None

        if checkquery is not None:
            return redirect("/showproduct")
        else:
            messages.error(request,"invalid email or password. please try again")

    print(checkuser)
    print(useremail)
    print(userpassword)
    return render(request,"Login.html")

def logout(request):
    try:
        del request.session["logid"]
        del request.session["logname"]
        del request.session["logrole"]
    except:
        pass
    return render(request,"Login.html")


def manageproduct(request):
    getalldata = productdetail.objects.all()
    context = {
        "alldata":getalldata
    }
    return render(request,"manageproduct.html",context)

def deleteproduct(request,id):
    getproductdata = productdetail.objects.get(id=id)
    getproductdata.delete()
    return redirect("/manageproduct")


def addtocart(request):
    uid = request.session["logid"]
    proid = request.POST.get("pid")
    proprice = request.POST.get("price")
    quantity = request.POST.get("quantity")
    total = float(proprice) * int(quantity)
    print(total)

    # query to check if item is already in cart or not
    # if yes --> update quantity as well as total
    # else --> store data in cart

    try:
        checkitemcart = carttable.objects.get(productid=proid,userid=uid,cartstatus=1)
    except:
        checkitemcart = None


    print(checkitemcart)

    if checkitemcart is None:
        storedata = carttable(userid=registertable(id=uid), productid=productdetail(id=proid)
                              , quantity=quantity, totalamount=total, cartstatus=1, orderid=0)
        storedata.save()
    else:
        checkitemcart.quantity += int(quantity)
        checkitemcart.totalamount += float(total)
        checkitemcart.save()
        messages.success(request,"Item updated")
    return redirect("/showproduct")


def showcart(request):
    uid = request.session["logid"]
    getcartdata = carttable.objects.filter(userid=uid,cartstatus=1)
    total_amount = getcartdata.aggregate(total=Sum('totalamount'))['total']
    print(total_amount)
    context = {
        "cartdata":getcartdata,
        "finaltotal":total_amount
    }
    return render(request,"showcart.html",context)


def removeitem(request , id):
    getitem = carttable.objects.get(id=id)
    getitem.delete()
    return redirect("/showcart")

def increaseitem(request , id):
    getitemfromcart = carttable.objects.get(id=id)
    getitemfromcart.quantity += 1
    getitemfromcart.totalamount += getitemfromcart.productid.productprice
    getitemfromcart.save()
    return redirect("/showcart")
def decreaseitem(request , id):
    getitemfromcart = carttable.objects.get(id=id)
    quantity = getitemfromcart.quantity
    if quantity == 1:
        getitemfromcart.delete() # you can write code of cartstatus=0 update here
    else:
        getitemfromcart.quantity -= 1
        getitemfromcart.totalamount -= getitemfromcart.productid.productprice
        getitemfromcart.save()
    return redirect("/showcart")


def findproduct(request):
    pname = request.POST.get("pname")
    getdata = productdetail.objects.filter(productname__contains=pname)
    context = {
        "prodata":getdata
    }
    return render(request,"showproduct.html",context)

def placeorder(request):
    userid = request.session["logid"]
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    paymode = request.POST.get("payment")
    finalamount = request.POST.get("finaltotal")

    storedata = ordertable(userid=registertable(id=userid),phoneno=phone,finaltotal=finalamount,address=address,paymode=paymode)
    storedata.save()

    lastorderid = storedata.id

    getcartdata = carttable.objects.filter(userid=userid, cartstatus=1)

    for i in getcartdata:
        i.cartstatus = 2
        i.orderid = lastorderid
        i.save()
    return redirect("/showproduct")


def yourorders(request):
    userid = request.session["logid"]
    fetchorderdata = ordertable.objects.filter(userid=userid)
    context = {
        "data":fetchorderdata
    }
    return render(request,"yourorders.html",context)

def yourdetailorder(request , id):
    fetchdata = carttable.objects.filter(orderid=id)
    context = {
        'cartdata':fetchdata
    }
    return render(request,"yourdetailorder.html",context)

def forgotpage(request):
    return render(request,"forgot.html")


def forgotpassword(request):
    if request.method == 'POST':
        username = request.POST['uemail']
        try:
            user = registertable.objects.get(email=username)

        except registertable.DoesNotExist:
            user = None
        # if user exist then only below condition will run otherwise it will give error as described in else condition.
        if user is not None:
            #################### Password Generation ##########################
            import random
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                       'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

            nr_letters = 6
            nr_symbols = 1
            nr_numbers = 3
            password_list = []

            for char in range(1, nr_letters + 1):
                password_list.append(random.choice(letters))

            for char in range(1, nr_symbols + 1):
                password_list += random.choice(symbols)

            for char in range(1, nr_numbers + 1):
                password_list += random.choice(numbers)

            print(password_list)
            random.shuffle(password_list)
            print(password_list)

            password = ""  # we will get final password in this var.
            for char in password_list:
                password += char

            ##############################################################

            msg = "hello here it is your new password  " + password  # this variable will be passed as message in mail

            ############ code for sending mail ########################

            from django.core.mail import send_mail

            send_mail(
                'Your New Password',
                msg,
                'krushanuinfolabz@gmail.com',
                [username],
                fail_silently=False,
            )

            # now update the password in model
            cuser = registertable.objects.get(email=username)
            cuser.password = password
            cuser.save(update_fields=['password'])

            print('Mail sent')
            messages.info(request, 'mail is sent')
            return redirect("/")

        else:
            messages.info(request, 'This account does not exist')
    return redirect("/")

def changepasswordpage(request):
    return render(request,"changepassword.html")

def updatepass(request):
    userid = request.session["logid"]
    opass = request.POST.get("oldpass")
    npass = request.POST.get("newpass")
    ncnfpass = request.POST.get("newcnfpass")

    fetchpass = registertable.objects.get(id=userid)
    userpass = fetchpass.password

    if opass!=userpass:
        messages.error(request,"Old password Didnt Match")
        return render(request,"changepassword.html")

    if npass!=ncnfpass:
        messages.error(request,"Confirm Password didnt match")
        return render(request, "changepassword.html")

    fetchpass.password = npass
    fetchpass.save()


    return redirect("/")


