from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import connection


# Create your views here.

def listing(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM company")
    companylist = dictfetchall(cursor)

    context = {
        "companylist": companylist
    }

    # Message according medicines Role #
    context['heading'] = "FARMER Details";
    return render(request, 'company-details.html', context)

def lists(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM company")
    companylist = dictfetchall(cursor)

    context = {
        "companylist": companylist
    }

    # Message according medicines Role #
    context['heading'] = "FARMER Details";
    return render(request, 'company-list.html', context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM company WHERE company_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, companyId):
    context = {
        "fn": "update",
        "companyDetails": getData(companyId),
        "heading": 'Update Farmer',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE company
                   SET company_name=%s, company_description=%s WHERE company_id = %s
                """, (
            request.POST['company_name'],
            request.POST['company_description'],
            companyId
        ))
        context["companyDetails"] =  getData(companyId)
        messages.add_message(request, messages.INFO, "Farmer details updated succesfully !!!")
        return redirect('company-listing')
    else:
        return render(request, 'company.html', context)


def add(request):
    context = {
        "fn": "add",
        "heading": 'Add Framer'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO company
		   SET company_name=%s, company_description=%s
		""", (
            request.POST['company_name'],
            request.POST['company_description']))
        return redirect('company-listing')
    return render(request, 'company.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM company WHERE company_id=' + id
    cursor.execute(sql)
    messages.add_message(request, messages.INFO, "Company Deleted succesfully !!!")
    return redirect('company-listing')
