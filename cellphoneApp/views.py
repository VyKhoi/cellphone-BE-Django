from itertools import product

from django.shortcuts import render
from cellphoneApp.models import *
# Create your views here.
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Q
from django.db import connection
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
import json


def hello(request):
    return HttpResponse("hello")

    JsonResponse(product, safe=False)


def get_color_names(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT names FROM cellphoneapp_color")
        rows = cursor.fetchall()
    names = [row[0] for row in rows]
    return JsonResponse({'names': names})


# cái hàm nài dùng để hien thị detail
def get_detail_product(request, branch_id, product_id, type_of_product):
    table = 0
    operator_system = ''
    # Định nghĩa giá trị table dựa trên giá trị của type_of_product
    if type_of_product == 1:
        table = "cellphoneapp_smartphone"
        operator_system = "Operator_System"
    elif type_of_product == 2:
        table = "cellphoneapp_laptop"
        operator_system = "operatorSystem"

    else:
        table = "unknown_table"

    # In giá trị table
    print('bang de selecttttttttttttttttttttttttttttt', table)

    with connection.cursor() as cursor:
        cursor.execute("""
                     SELECT  pc.Id AS ProductColorId, pc.idProduct_id AS productID, pc.Price,pc.nameColor_id as mau_cua_san_pham,  bpp.discountRate, p.timeStart, p.timeEnd, bp.Amount, b.Name AS branch_name, p2.Name AS product_name, m.names AS manufacturer_name,i.linkImg, r.Title AS review_title, r.Content AS review_content, s.{1}, s.CPU, s.RAM, s.ROM, s.Battery, s.Others, bpc.Amount,i.Name as name_cua_anh
                    FROM cellphoneapp_promotion p 
                    JOIN cellphoneapp_branch_promotion_product bpp ON p.Id = bpp.idPromotion_id 
                    JOIN cellphoneapp_branch_product_color bp ON bpp.idBrandProductColor_id = bp.Id 
                    JOIN cellphoneapp_product_color pc ON bp.idProductColor_id = pc.Id 
                    JOIN cellphoneapp_branch b ON bp.idBranch_id = b.Id 
                    JOIN cellphoneapp_product p2 ON pc.idProduct_id = p2.Id 
                    JOIN cellphoneapp_manufacture m ON p2.nameManufacture_id = m.names 
                    LEFT JOIN cellphoneapp_imageproduct i ON p2.Id = i.idProduct_id 
                    LEFT JOIN cellphoneapp_review r ON p2.Id = r.idProduct_id 
                    LEFT JOIN {0} s ON p2.Id = s.product_ptr_id 
                    JOIN cellphoneapp_branch_product_color bpc ON b.Id = bpc.idBranch_id AND pc.Id = bpc.idProductColor_id 
                    WHERE b.Id = %s AND s.{1} IS NOT NULL and p2.Id = %s and pc.nameColor_id like i.Name and p.Active = 1

                    LIMIT 0, 1000;
                """.format(table, operator_system), [branch_id, product_id])

        rows = cursor.fetchall()

    name_TMP = rows[0][9]
    print('nam tam cua co no la', rows)
    # lay phien bang
    with connection.cursor() as cursor:
        cursor.execute("""
                 SELECT  pc.Id AS ProductColorId, pc.idProduct_id AS productID, pc.Price,pc.nameColor_id as mau_cua_san_pham,  bpp.discountRate, p.timeStart, p.timeEnd, bp.Amount, b.Name AS branch_name, p2.Name AS product_name, m.names AS manufacturer_name,i.linkImg, r.Title AS review_title, r.Content AS review_content, s.Operator_System, s.CPU, s.RAM, s.ROM, s.Battery, s.Others, bpc.Amount,i.Name as name_cua_anh
                FROM cellphoneapp_promotion p 
                JOIN cellphoneapp_branch_promotion_product bpp ON p.Id = bpp.idPromotion_id 
                JOIN cellphoneapp_branch_product_color bp ON bpp.idBrandProductColor_id = bp.Id 
                JOIN cellphoneapp_product_color pc ON bp.idProductColor_id = pc.Id 
                JOIN cellphoneapp_branch b ON bp.idBranch_id = b.Id 
                JOIN cellphoneapp_product p2 ON pc.idProduct_id = p2.Id 
                JOIN cellphoneapp_manufacture m ON p2.nameManufacture_id = m.names 
                LEFT JOIN cellphoneapp_imageproduct i ON p2.Id = i.idProduct_id 
                LEFT JOIN cellphoneapp_review r ON p2.Id = r.idProduct_id 
                LEFT JOIN cellphoneapp_smartphone s ON p2.Id = s.product_ptr_id 
                JOIN cellphoneapp_branch_product_color bpc ON b.Id = bpc.idBranch_id AND pc.Id = bpc.idProductColor_id 
                WHERE b.Id = %s AND s.Operator_System IS NOT NULL and p2.Name like %s and pc.nameColor_id like i.Name and p.Active = 1
				group by pc.idProduct_id
                LIMIT 0, 1000;
            """, [branch_id, name_TMP])
        pb = cursor.fetchall()

    # print('phien ban khac' , pb)
    options = []

    for i in pb:
        # print('chay xuat id', i[1], " voi ", row[1])  # lam sao de lay anh em no
        # if i[1] == row[1]:
        tmp = {}
        tmp["idProduct"] = i[1]
        tmp["ram"] = i[16]
        tmp["rom"] = i[17]
        # cl = {}
        # cl['color'] = i[3]
        # cl['price'] = i[2]
        options.append(tmp)
        # color.append(cl)

    print('thong so phien bangggggggg', options)

    data = []
    color = []
    for i in rows:
        cl = {}
        cl['color'] = i[3]
        cl['price'] = i[2]
        color.append(cl)
    print("xan pham nay co id mau laaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", rows[0][0])
    for row in rows:
        print('moi dong laaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', row)
        image = []
        for i in rows:
            print('chay')
            if i[1] == row[1]:
                imageProduct = {}
                imageProduct['name'] = i[21]
                imageProduct['link'] = i[11]
                image.append(imageProduct)

        d = {}
        d['image'] = image
        d['branch_name'] = row[0]
        d['id'] = row[1]
        d['name'] = row[9]
        d['nameManufacture'] = row[10]
        d['price'] = row[2]
        d['discountRate'] = row[4]
        d['currentPrice'] = float(row[2]) - float(row[2]) * row[4]
        d['id_product_color'] = row[0]
        d['name_color_id'] = row[3]
        d['image_link'] = row[11]
        d['reviewTitle'] = row[12]
        d['introduce'] = row[13]
        d['operatorSystem'] = row[14]
        d['CPU'] = row[15]
        d['RAM'] = row[16]
        d['ROM'] = row[17]
        d['Battery'] = row[18]
        d['Others'] = row[19]
        d['amount'] = row[20]
        d['options'] = options
        d['color'] = color
        data.append(d)

    return JsonResponse(data, safe=False)


def get_products_phones(request, branch_id):
    with connection.cursor() as cursor:
        cursor.execute("""
             SELECT  pc.Id AS ProductColorId, pc.idProduct_id AS productID, pc.Price, pc.nameColor_id, bpp.discountRate, p.timeStart, p.timeEnd, bp.Amount, b.Name AS branch_name, p2.Name AS product_name, m.names AS manufacturer_name,i.linkImg, r.Title AS review_title, r.Content AS review_content, s.Operator_System, s.CPU, s.RAM, s.ROM, s.Battery, s.Others, bpc.Amount 
            FROM cellphoneapp_promotion p 
            JOIN cellphoneapp_branch_promotion_product bpp ON p.Id = bpp.idPromotion_id 
            JOIN cellphoneapp_branch_product_color bp ON bpp.idBrandProductColor_id = bp.Id 
            JOIN cellphoneapp_product_color pc ON bp.idProductColor_id = pc.Id 
            JOIN cellphoneapp_branch b ON bp.idBranch_id = b.Id 
            JOIN cellphoneapp_product p2 ON pc.idProduct_id = p2.Id 
            JOIN cellphoneapp_manufacture m ON p2.nameManufacture_id = m.names 
            LEFT JOIN cellphoneapp_imageproduct i ON p2.Id = i.idProduct_id 
            LEFT JOIN cellphoneapp_review r ON p2.Id = r.idProduct_id 
            LEFT JOIN cellphoneapp_smartphone s ON p2.Id = s.product_ptr_id 
            JOIN cellphoneapp_branch_product_color bpc ON b.Id = bpc.idBranch_id AND pc.Id = bpc.idProductColor_id 
            WHERE b.Id = %s AND s.Operator_System IS NOT NULL and  pc.nameColor_id like i.Name and p.Active = 1
            group by  pc.idProduct_id
            LIMIT 0, 1000;

           """, [branch_id])
        rows = cursor.fetchall()
        data = []
        for row in rows:
            d = {}
            d['branch_name'] = row[8]
            d['id'] = row[1]
            d['name'] = row[9]
            d['nameManufacture'] = row[10]
            # row[4] theo câu truy van thi no la discount
            d['currentPrice'] = float(row[2]) - float(row[2]) * row[4]

            d['price'] = row[2]
            d['discountRate'] = row[4]
            d['id_product_color'] = row[0]
            d['currentColor'] = row[3]
            d['currentImage'] = row[11]
            d['reviewTitle'] = row[12]
            d['introduce'] = row[13]
            d['operatorSystem'] = row[14]
            d['CPU'] = row[15]
            d['RAM'] = row[16]
            d['ROM'] = row[17]
            d['Battery'] = row[18]
            d['Others'] = row[19]
            d['amount'] = row[20]
            data.append(d)

        return JsonResponse(data, safe=False)


def get_products_laptop(request, branch_id):
    with connection.cursor() as cursor:
        cursor.execute("""
           SELECT  pc.Id AS ProductColorId, pc.idProduct_id AS productID, pc.Price, pc.nameColor_id, bpp.discountRate, p.timeStart, p.timeEnd, bp.Amount, b.Name AS branch_name, p2.Name AS product_name, m.names AS manufacturer_name,i.linkImg, r.Title AS review_title, r.Content AS review_content, s.operatorSystem, s.CPU, s.RAM, s.ROM, s.Battery, s.Others, bpc.Amount 
            FROM cellphoneapp_promotion p 
            JOIN cellphoneapp_branch_promotion_product bpp ON p.Id = bpp.idPromotion_id 
            JOIN cellphoneapp_branch_product_color bp ON bpp.idBrandProductColor_id = bp.Id 
            JOIN cellphoneapp_product_color pc ON bp.idProductColor_id = pc.Id 
            JOIN cellphoneapp_branch b ON bp.idBranch_id = b.Id 
            JOIN cellphoneapp_product p2 ON pc.idProduct_id = p2.Id 
            JOIN cellphoneapp_manufacture m ON p2.nameManufacture_id = m.names 
            LEFT JOIN cellphoneapp_imageproduct i ON p2.Id = i.idProduct_id 
            LEFT JOIN cellphoneapp_review r ON p2.Id = r.idProduct_id 
            LEFT JOIN cellphoneapp_laptop s ON p2.Id = s.product_ptr_id 
            JOIN cellphoneapp_branch_product_color bpc ON b.Id = bpc.idBranch_id AND pc.Id = bpc.idProductColor_id 
            WHERE b.Id = %s AND s.operatorSystem IS NOT NULL and  pc.nameColor_id like i.Name and p.Active = 1
            group by  pc.idProduct_id
            LIMIT 0, 1000;
           """, [branch_id])
        rows = cursor.fetchall()
        data = []
        for row in rows:
            d = {}
            d['branch_name'] = row[8]
            d['id'] = row[1]
            d['name'] = row[9]
            d['nameManufacture'] = row[10]
            # row[4] theo câu truy van thi no la discount
            d['currentPrice'] = float(row[2]) - float(row[2]) * row[4]

            d['price'] = row[2]
            d['discountRate'] = row[4]
            d['id_product_color'] = row[0]
            d['currentColor'] = row[3]
            d['currentImage'] = row[11]
            d['reviewTitle'] = row[12]
            d['introduce'] = row[13]
            d['operatorSystem'] = row[14]
            d['CPU'] = row[15]
            d['RAM'] = row[16]
            d['ROM'] = row[17]
            d['Battery'] = row[18]
            d['Others'] = row[19]
            d['amount'] = row[20]
            data.append(d)

        return JsonResponse(data, safe=False)


@api_view(['GET'])
def get_comments_product(request, id_product):
    comments = Comment.objects.filter(idProduct_id=id_product)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


def get_order_lockup(request, deliveryPhone):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT o.id as order_ID, o.Status, SUM(od.unit_price * od.Quantity) as 'toltal_Price', 
                   JSON_ARRAYAGG(
                       JSON_OBJECT(
                           'id_product', p.id,
                           'Name', p.Name,
                           'unitPrice', od.unit_price,
                           'quantity', od.Quantity,
                           'nameColor', pc.nameColor_id,
                           'id_branch_product_color', bpc.id
                       )
                   ) as productDetail
            FROM cellphoneapp_order o
            JOIN cellphoneapp_orderdetail od ON o.id = od.idOder_id
            JOIN cellphoneapp_branch_product_color bpc ON od.idBrandProductColor_id = bpc.id
            JOIN cellphoneapp_product_color pc ON bpc.idProductColor_id = pc.id
            JOIN cellphoneapp_product p ON pc.idProduct_id = p.id
            WHERE o.deliveryPhone = %s
            GROUP BY o.id
        """, [deliveryPhone])
        rows = cursor.fetchall()
        data = [
            {
                'order_ID': row[0],
                'Status': row[1],
                'toltal_Price': row[2],
                'product_Detail': json.loads(row[3])
            }
            for row in rows
        ]
    return JsonResponse(data, safe=False)
