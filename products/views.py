from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from .models import product
from django.contrib import messages
from django.db import connection
from FTC.utils import getDropDown, dictfetchall
import datetime

# Create your views here.
def orderlisting(request):
    cursor = connection.cursor()
    if (request.session.get('user_level_id', None) == 1):
        SQL = "SELECT * FROM `order`,`users_user`,`order_status` WHERE order_status = os_id AND order_user_id = user_id"
    else:
        customerID = str(request.session.get('user_id', None))
        SQL = "SELECT * FROM `order`,`users_user`,`order_status` WHERE order_status = os_id AND order_user_id = user_id AND user_id = " + customerID
    cursor.execute(SQL)
    orderlist = dictfetchall(cursor)

    context = {
        "orderlist": orderlist
    }

    # Message according Product #
    context['heading'] = "Order Reports";
    return render(request, 'order-listing.html', context)

# Create your views here.
def productlisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM products_product, company, type WHERE company_id = product_company_id AND type_id = product_type_id")
    productlist = dictfetchall(cursor)

    context = {
        "productlist": productlist
    }

    # Message according Product #
    context['heading'] = "Products Details";
    return render(request, 'products-listing.html', context)

# Create your views here.
def payment(request):
    orderID = request.session.get('order_id', None);
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(oi_total) as TotalCartValue FROM order_item WHERE oi_order_id = " + str(orderID))
    orderTotal = dictfetchall(cursor)
    context = {
        "orderTotal": orderTotal[0]
    }
    if (request.method == "POST"):
        request.session['order_id'] = "0"
        return redirect('order-items/'+str(orderID))
    # Message according Product #
    context['heading'] = "Products Details";
    return render(request, 'payment.html', context)

# Create your views here.
def cancel_order(request, orderID):
    cursor = connection.cursor()
    cursor.execute("""
                UPDATE `order`
                SET order_status= '5' WHERE order_id = %s
            """, (
        orderID
    ))
    messages.add_message(request, messages.INFO, "Your order has been cancelled successfully !!!")
    return redirect('orderlisting')

# Create your views here.
def order_items(request, orderID):
    cursor = connection.cursor()
    ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `products_product`, `order`, order_item, company, type WHERE product_id =  oi_product_id AND oi_order_id = order_id AND company_id = product_company_id AND type_id = product_type_id AND order_id = "+ str(orderID))
    productlist = dictfetchall(cursor)

     ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `order`, `users_user`,`order_status` WHERE order_status = os_id AND user_id =  order_user_id  AND order_id = "+ str(orderID))
    customerOrderDetails = dictfetchall(cursor)
    
    ### Get the Total Cart  ####
    cursor.execute("SELECT SUM(oi_total) as totalCartCost  FROM `products_product`, `order`, order_item, company, type WHERE product_id =  oi_product_id AND oi_order_id = order_id AND company_id = product_company_id AND type_id = product_type_id AND order_id = "+ str(orderID))
    totalCost = dictfetchall(cursor)
    
    context = {
        "productlist": productlist,
        "customerOrderDetails": customerOrderDetails[0],
        "totalCost":totalCost[0]
    }

    # Message according Product #
    context['heading'] = "Products Details";
    return render(request, 'order-items.html', context)

# Create your views here.
def order_edit(request, orderID):
    cursor = connection.cursor()
    ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `products_product`, `order`, order_item, company, type WHERE product_id =  oi_product_id AND oi_order_id = order_id AND company_id = product_company_id AND type_id = product_type_id AND order_id = "+ str(orderID))
    productlist = dictfetchall(cursor)

     ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `order`, `users_user`,`order_status` WHERE order_status = os_id AND user_id =  order_user_id  AND order_id = "+ str(orderID))
    customerOrderDetails = dictfetchall(cursor)
    customerOrderDetails = customerOrderDetails[0]
    
    ### Get the Total Cart  ####
    cursor.execute("SELECT SUM(oi_total) as totalCartCost  FROM `products_product`, `order`, order_item, company, type WHERE product_id =  oi_product_id AND oi_order_id = order_id AND company_id = product_company_id AND type_id = product_type_id AND order_id = "+ str(orderID))
    totalCost = dictfetchall(cursor)
    
    context = {
        "productlist": productlist,
        "protypelist":getDropDown('order_status', 'os_id', 'os_title', customerOrderDetails['order_status'], '1'),
        "customerOrderDetails": customerOrderDetails,
        "totalCost":totalCost[0]
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                    UPDATE `order`
                    SET order_status= %s WHERE order_id = %s
                """, (
            request.POST['order_status'],
            request.POST['order_id']
        ))
        messages.add_message(request, messages.INFO, "Your order has been cancelled successfully !!!")
        return redirect('orderlisting')
    # Message according Product #
    context['heading'] = "Products Details";
    return render(request, 'order-edit.html', context)

# Create your views here.
def cart_listing(request):
    orderID = request.session.get('order_id', None);
    cursor = connection.cursor()
    ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `products_product`, `order`, order_item, company, type WHERE product_id =  oi_product_id AND oi_order_id = order_id AND company_id = product_company_id AND type_id = product_type_id AND order_id = "+ str(orderID))
    productlist = dictfetchall(cursor)
    
    ### Get the Total Cart  ####
    cursor.execute("SELECT SUM(oi_total) as totalCartCost  FROM `products_product`, `order`, order_item, company, type WHERE product_id =  oi_product_id AND oi_order_id = order_id AND company_id = product_company_id AND type_id = product_type_id AND order_id = "+ str(orderID))
    totalCost = dictfetchall(cursor)
    
    context = {
        "productlist": productlist,
        "totalCost":totalCost[0]
    }

    # Message according Product #
    context['heading'] = "Products Details";
    return render(request, 'carts.html', context)

# Create your views here.
def products(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM products_product, company, type WHERE company_id = product_company_id AND type_id = product_type_id")
    productlist = dictfetchall(cursor)

    context = {
        "productlist": productlist
    }

    # Message according Product #
    context['heading'] = "Products Details";
    return render(request, 'products.html', context)

# Create your views here.
def product_filter(request, typeID):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM products_product, company, type WHERE company_id = product_company_id AND type_id = product_type_id AND type_id = "+ str(typeID))
    productlist = dictfetchall(cursor)

    context = {
        "productlist": productlist
    }

    # Message according Product #
    context['heading'] = "Products Details";
    return render(request, 'products.html', context)

def update(request, productId):
    productdetails = product.objects.get(product_id=productId)
    context = {
        "fn": "add",
        "procompanylist":getDropDown('company', 'company_id', 'company_name', productdetails.product_company_id, '1'),
        "protypelist":getDropDown('type', 'type_id', 'type_name', productdetails.product_type_id, '1'),
        "productdetails":productdetails
    }
    if (request.method == "POST"):
        try:
            product_image = None
            product_image = productdetails.product_image
            if(request.FILES and request.FILES['product_image']):
                productImage = request.FILES['product_image']
                fs = FileSystemStorage()
                filename = fs.save(productImage.name, productImage)
                product_image = fs.re_path(productImage)

            addProduct = product(
            product_id = productId,
            product_name = request.POST['product_name'],
            product_type_id = request.POST['product_type_id'],
            product_company_id = request.POST['product_company_id'],
            product_price = request.POST['product_price'],
            product_image = product_image,                  
            product_description = request.POST['product_description'],
            product_stock = request.POST['product_stock'])
            addProduct.save()
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        context["productdetails"] = product.objects.get(product_id = productId)
        messages.add_message(request, messages.INFO, "Product updated succesfully !!!")
        return redirect('productlisting')

    else:
        return render(request,'products-add.html', context)

def product_details(request, productId):
    if(request.session.get('authenticated', False) == False):
        messages.add_message(request, messages.ERROR, "Login to your account, to buy the product !!!")
        return redirect('/users')
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM products_product, company, type WHERE company_id = product_company_id AND type_id = product_type_id AND product_id = "+productId)
    productdetails = dictfetchall(cursor)

    context = {
        "fn": "add",
        "productdetails":productdetails[0]
    }
    if (request.method == "POST"):
        try:
            if(request.session.get('order_id', None) == "0" or request.session.get('order_id', False) == False):
                customerID = request.session.get('user_id', None)
                orderDate = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
                cursor = connection.cursor()
                cursor.execute("""
                INSERT INTO `order`
                SET order_user_id=%s, order_date=%s, order_status=%s, order_total=%s
                """, (
                    customerID,
                    orderDate,
                    1,
                    0))
                request.session['order_id'] = cursor.lastrowid    
            
            orderID = request.session.get('order_id', None);
            cursor = connection.cursor()
            totalAmount = int(request.POST['product_price']) * int(request.POST['product_quantity']);
            cursor.execute("""
            INSERT INTO order_item
            SET oi_order_id=%s, oi_product_id=%s, oi_price_per_unit=%s, oi_cart_quantity=%s, oi_total=%s
        """, (
            orderID,
            request.POST['product_id'],
            request.POST['product_price'],
            request.POST['product_quantity'],
            totalAmount))
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        context["productdetails"] = product.objects.get(product_id = productId)
        messages.add_message(request, messages.INFO, "Product updated succesfully !!!")
        return redirect('cart_listing')
    else:
        return render(request,'products-details.html', context)

def add(request):
    context = {
        "fn": "add",
        "procompanylist":getDropDown('company', 'company_id', 'company_name',0, '1'),
        "protypelist":getDropDown('type', 'type_id', 'type_name',0, '1'),
        "heading": 'Product add'
    }
    if (request.method == "POST"):
        try:
            product_image = None

            if(request.FILES and request.FILES['product_image']):
                productImage = request.FILES['product_image']
                fs = FileSystemStorage()
                filename = fs.save(productImage.name, productImage)
                product_image = fs.url(productImage)

            addProduct = product(product_name = request.POST['product_name'],
            product_type_id = request.POST['product_type_id'],
            product_company_id = request.POST['product_company_id'],
            product_price = request.POST['product_price'],
            product_image = product_image,                  
            product_description = request.POST['product_description'],
            product_stock = request.POST['product_stock'])
            addProduct.save()
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        return redirect('productlisting')

    else:
        return render(request,'products-add.html', context)

def delete_item(request, itemId):
    cursor = connection.cursor()
    sql = 'DELETE FROM order_item WHERE oi_id=' + itemId
    cursor.execute(sql)
    return redirect('cart_listing')

def delete(request, prodId):
    try:
        deleteProduct = product.objects.get(product_id = prodId)
        deleteProduct.delete()
    except Exception as e:
        return HttpResponse('Something went wrong. Error Message : '+ str(e))
    messages.add_message(request, messages.INFO, "Product Deleted Successfully !!!")
    return redirect('productlisting')

def stock(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM stock, products_product WHERE product_id = stock_product_id")
    stocklist = dictfetchall(cursor)

    context = {
        "stocklist": stocklist
    }

    # Message according Product #
    context['heading'] = "Products Stock Details";
    return render(request, 'stock.html', context)

def deletestock(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM stock WHERE stock_id=' + id
    cursor.execute(sql)
    return redirect('stock')

def companylisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM company")
    companylist = dictfetchall(cursor)

    context = {
        "companylist": companylist
    }

    # Message according Product #
    context['heading'] = "Products Company";
    return render(request, 'viewcompany.html', context)

def deletecompany(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM company WHERE company_id=' + id
    cursor.execute(sql)
    return redirect('company')

def addcompany(request):
    context = {
        "fn": "add",
        "heading": 'Add Company'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO company
		   SET company_name=%s
		""", (
            request.POST['company_name']))
        return redirect('companylisting')
    return render(request, 'addcompany.html', context)

def order(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM order_item")
    orderlist = dictfetchall(cursor)

    context = {
        "orderlist": orderlist
    }

    # Message according Orders #
    context['heading'] = "Products Order Details";
    return render(request, 'orders.html', context)
