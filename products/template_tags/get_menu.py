from django import template
from django.db import connection

register = template.Library()

@register.simple_tag
def getTypesMenu():
    return getData()


def getData():
    ### Get the Topic ####
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM type")
    dataList = dictfetchall(cursor)
    return dataList
        

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]