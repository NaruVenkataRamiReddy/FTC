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
    cursor.execute("SELECT * FROM type")
    typelist = dictfetchall(cursor)

    context = {
        "typelist": typelist
    }

    # Message according medicines Role #
    context['heading'] = "Type Details";
    return render(request, 'type-details.html', context)

def lists(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM type")
    typelist = dictfetchall(cursor)

    context = {
        "typelist": typelist
    }

    # Message according medicines Role #
    context['heading'] = "Type Details";
    return render(request, 'type-list.html', context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM type WHERE type_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, typeId):
    context = {
        "fn": "update",
        "typeDetails": getData(typeId),
        "heading": 'Update Type',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE type
                   SET type_name=%s, type_description=%s WHERE type_id = %s
                """, (
            request.POST['type_name'],
            request.POST['type_description'],
            typeId
        ))
        context["typeDetails"] =  getData(typeId)
        messages.add_message(request, messages.INFO, "Type updated succesfully !!!")
        return redirect('type-listing')
    else:
        return render(request, 'type.html', context)


def add(request):
    context = {
        "fn": "add",
        "heading": 'Add Type'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO type
		   SET type_name=%s, type_description=%s
		""", (
            request.POST['type_name'],
            request.POST['type_description']))
        return redirect('type-listing')
    return render(request, 'type.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM type WHERE type_id=' + id
    cursor.execute(sql)
    messages.add_message(request, messages.INFO, "Type Deleted succesfully !!!")
    return redirect('type-listing')
