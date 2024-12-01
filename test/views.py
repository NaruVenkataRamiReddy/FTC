from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from .models import test
from django.contrib import messages
from django.db import connection

# Create your views here.

def listing(request, doctorId = "0"):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM test_test")
    testlist = dictfetchall(cursor)
   
    context = {
        "testlist": testlist
    }
   
    # Message according test Role #
    context['heading'] = "Test Report";
    return render(request,'test-report.html',context)

def getDropDown(table, condtion):
    cursor = connection.cursor()    
    cursor.execute("SELECT * FROM "+table+" WHERE "+condtion)
    dropdownList = dictfetchall(cursor)
    return dropdownList;

def add(request):
    context = {
    "fn":"add",
    "heading":'Test'
    }
    if (request.method == "POST"):
        try:
            addTest = test(test_title = request.POST['test_title'],
            test_cost = request.POST['test_cost'],
            test_duration = request.POST['test_duration'],
            test_description = request.POST['test_description'])
            addTest.save()
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        return redirect('listing')

    else:
        return render(request,'test.html', context)

def update(request, testId):
    context = {
    "fn":"update",
    "companylist":getDropDown('company','1'),
    "heading":'Test',
    "testdetails":test.objects.get(test_id = testId)
    }
    if (request.method == "POST"):
        try:
            addTest = test(
            test_id = testId,    
            test_title = request.POST['test_title'],
            test_cost = request.POST['test_cost'],
            test_duration = request.POST['test_duration'],
            test_description = request.POST['test_description'])
            addTest.save()
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        context["testdetails"] = test.objects.get(test_id = testId)
        messages.add_message(request, messages.INFO, "Test updated succesfully !!!")
        return redirect('/test/')

    else:
        return render(request,'test.html', context)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def delete(request, testId):
    try:
        deleteTest = test.objects.get(test_id = testId)
        deleteTest.delete()
    except Exception as e:
        return HttpResponse('Something went wrong. Error Message : '+ str(e))
    messages.add_message(request, messages.INFO, "Test Deleted Successfully !!!")
    return redirect('listing')
