from itertools import product

from django.http import HttpResponse
import json
from django.http import JsonResponse

from django.db import connection
from django.db import models
from django.http import JsonResponse
from django.shortcuts import redirect

from rest_framework.decorators import api_view

from .serializers import *
import json
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from cellphoneApp.models import *

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
def get_detail_product(request, branch_id, product_id):
    # type_of_product = 1
    p = Product.objects.get(Id=product_id)
    # print('product lay dc laaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', p.Type)
    table = 0
    operator_system = ''
    # Định nghĩa giá trị table dựa trên giá trị của type_of_product
    if p.Type == 'phone':
        table = "cellphoneapp_smartphone"
        operator_system = "Operator_System"
    elif p.Type == 'laptop':
        table = "cellphoneapp_laptop"
        operator_system = "operatorSystem"

    else:
        table = "unknown_table"

    # In giá trị table
    print('bang de selecttttttttttttttttttttttttttttt', table)

    with connection.cursor() as cursor:
        cursor.execute("""
                     SELECT  pc.Id AS ProductColorId, pc.idProduct_id AS productID, pc.Price,pc.nameColor_id as mau_cua_san_pham,  bpp.discountRate, p.timeStart, p.timeEnd, bp.Amount, b.Name AS branch_name, p2.Name AS product_name, m.names AS manufacturer_name,i.linkImg, r.Title AS review_title, r.Content AS review_content, s.{1}, s.CPU, s.RAM, s.ROM, s.Battery, s.Others, bpc.Amount,i.Name as name_cua_anh, bp.Id
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

    if not rows:
        with connection.cursor() as cursor:
            cursor.execute("""
                        select pc.Id,pc.idProduct_id as product_id,pc.Price,pc.nameColor_id,p.Name, p.nameManufacture_id,image.linkImg,	r.Title,r.Content,s.{1},s.CPU,s.RAM,s.ROM,s.Battery,s.Others,bpc.Amount,image.Name as namecuaanh ,bpc.Id from cellphoneapp_product p,cellphoneapp_product_color pc, cellphoneapp_branch_product_color bpc,cellphoneapp_imageproduct image, cellphoneapp_review,cellphoneapp_review r,{0} s
                        where p.Id = pc.idProduct_id and
                        pc.Id = bpc.idProductColor_id
                        and p.id = s.product_ptr_id 
                        and p.id = image.idProduct_id
                        and bpc.idBranch_id = %s and p.Id = %s and pc.nameColor_id like image.Name
                        group by pc.Id

                       """.format(table, operator_system), [branch_id, product_id])
            rows = cursor.fetchall()
        print('rows mới trả về khi mà nó không có khuyến mãi ', rows[0][4])
        name_TMP = rows[0][4]
        with connection.cursor() as cursor:
            cursor.execute("""
                        select pc.Id,pc.idProduct_id as product_id,pc.Price,pc.nameColor_id,p.Name, p.nameManufacture_id,image.linkImg,	r.Title,r.Content,s.{1},s.CPU,s.RAM,s.ROM,s.Battery,s.Others,bpc.Amount,image.Name as namecuaanh,bpc.Id from cellphoneapp_product p,cellphoneapp_product_color pc, cellphoneapp_branch_product_color bpc,cellphoneapp_imageproduct image, cellphoneapp_review,cellphoneapp_review r,{0} s
                        where p.Id = pc.idProduct_id and
                        pc.Id = bpc.idProductColor_id
                        and p.id = s.product_ptr_id 
                        and p.id = image.idProduct_id
                        and bpc.idBranch_id = %s and p.Name = %s and pc.nameColor_id like image.Name
                        group by pc.idProduct_id

                               """.format(table, operator_system), [branch_id, name_TMP])
            pb = cursor.fetchall()
        options = []
        for i in pb:
            tmp = {}
            tmp["idProduct"] = i[1]
            tmp["ram"] = i[11]
            tmp["rom"] = i[12]
            options.append(tmp)
        print('thong so phien bangggggggg moi', pb)

        data = []
        color = []
        for i in rows:
            cl = {}
            cl['id_branch_product_color'] = i[17]
            cl['color'] = i[3]
            cl['price'] = i[2]
            color.append(cl)
        print("xan pham nay co id mau laaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa moi ", name_TMP)
        for row in rows:
            print('moi dong laaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', row)
            image = []
            for i in rows:
                print('chay')
                if i[1] == row[1]:
                    imageProduct = {}
                    imageProduct['name'] = i[16]
                    imageProduct['link'] = i[6]
                    image.append(imageProduct)

            d = {}
            d['image'] = image
            d['id'] = row[1]
            d['name'] = row[4]
            d['nameManufacture'] = row[5]
            d['price'] = row[2]

            d['currentPrice'] = row[2]
            d['id_product_color'] = row[0]
            d['name_color_id'] = row[3]
            d['image_link'] = row[6]
            d['reviewTitle'] = row[7]
            d['introduce'] = row[8]
            d['operatorSystem'] = row[9]
            d['CPU'] = row[10]
            d['RAM'] = row[11]
            d['ROM'] = row[12]
            d['Battery'] = row[13]
            d['Others'] = row[14]
            d['amount'] = row[15]
            d['options'] = options
            d['color'] = color

            data.append(d)

        return JsonResponse(data, safe=False)

    else:
        name_TMP = rows[0][9]
        print('nam tam cua co no la', name_TMP)

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
                    WHERE b.Id = %s AND s.{1} IS NOT NULL and p2.Name like %s and pc.nameColor_id like i.Name and p.Active = 1
                    group by pc.idProduct_id
                    LIMIT 0, 1000;
                """.format(table, operator_system), [branch_id, name_TMP])
            pb = cursor.fetchall()
        # print('phien ban khac' , pb)
        options = []
        for i in pb:
            tmp = {}
            tmp["idProduct"] = i[1]
            tmp["ram"] = i[16]
            tmp["rom"] = i[17]
            options.append(tmp)

        print('thong so phien bangggggggg', options)
        data = []
        color = []
        for i in rows:
            cl = {}
            cl['id_branch_product_color'] = i[22]
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
             SELECT  pc.Id AS ProductColorId, pc.idProduct_id AS productID, pc.Price, pc.nameColor_id, bpp.discountRate, p.timeStart, p.timeEnd, bp.Amount, b.Name AS branch_name, p2.Name AS product_name, m.names AS manufacturer_name,i.linkImg, r.Title AS review_title, r.Content AS review_content, s.Operator_System, s.CPU, s.RAM, s.ROM, s.Battery, s.Others, bpc.Amount ,bp.Id
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
            d['id_branch_product_color'] = row[21]
            data.append(d)

        return JsonResponse(data, safe=False)


# api lay tất cả product không tính khuyến mãi
def get_products_phones_all(request, branch_id):
    print('hello')
    with connection.cursor() as cursor:
        cursor.execute("""
       select bpc.idBranch_id,pc.Id as idProduct_color, p.Id as product_id ,pc.Price,p.nameManufacture_id,pc.nameColor_id,m.Operator_System,m.CPU,m.RAM,m.ROM,m.Battery,m.Others, p.Name as tensanpham ,im.Name , im.linkImg, bpc.Amount from cellphoneapp_branch b,cellphoneapp_branch_product_color bpc ,cellphoneapp_product_color pc, cellphoneapp_product p,cellphoneapp_smartphone m,cellphoneapp_imageproduct im
        where b.Id = bpc.idBranch_id and
		bpc.idProductColor_id = pc.Id and
        pc.idProduct_id = p.Id and
        p.Id = m.product_ptr_id and 
		p.Id = im.idProduct_id and
        b.id = %s and
        Operator_System is not null
        group by p.id
           """, [branch_id])
        rows = cursor.fetchall()

        data = []
        for row in rows:
            d = {}
            d['id'] = row[2]
            d['name'] = row[12]
            d['nameManufacture'] = row[4]
            # row[4] theo câu truy van thi no la discount
            d['currentPrice'] = row[3]
            d['id_product_color'] = row[1]
            d['currentColor'] = row[5]
            d['currentImage'] = row[14]
            d['operatorSystem'] = row[6]
            d['CPU'] = row[7]
            d['RAM'] = row[8]
            d['ROM'] = row[9]
            d['Battery'] = row[10]
            d['Others'] = row[11]
            d['amount'] = row[15]
            data.append(d)

    return JsonResponse(data, safe=False)


# api lấy product laptop duoc khuyen mai
def get_products_laptop(request, branch_id):
    with connection.cursor() as cursor:
        cursor.execute("""
           SELECT  pc.Id AS ProductColorId, pc.idProduct_id AS productID, pc.Price, pc.nameColor_id, bpp.discountRate, p.timeStart, p.timeEnd, bp.Amount, b.Name AS branch_name, p2.Name AS product_name, m.names AS manufacturer_name,i.linkImg, r.Title AS review_title, r.Content AS review_content, s.operatorSystem, s.CPU, s.RAM, s.ROM, s.Battery, s.Others, bpc.Amount , bp.Id
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
            d['id_branch_product_color'] = row[21]
            data.append(d)

        return JsonResponse(data, safe=False)


# api lay tat ca laptop khong khuyen mai
def get_products_laptops_all(request, branch_id):
    print('hello')
    with connection.cursor() as cursor:
        cursor.execute("""
       select bpc.idBranch_id,pc.Id as idProduct_color, p.Id as product_id ,pc.Price,p.nameManufacture_id,pc.nameColor_id,l.operatorSystem,l.CPU,l.RAM,l.ROM,l.Battery,l.Others, p.Name as tensanpham ,im.Name , im.linkImg, bpc.Amount from cellphoneapp_branch b,cellphoneapp_branch_product_color bpc ,cellphoneapp_product_color pc, cellphoneapp_product p,cellphoneapp_laptop l,cellphoneapp_imageproduct im
        where b.Id = bpc.idBranch_id and
		bpc.idProductColor_id = pc.Id and
        pc.idProduct_id = p.Id and
        p.Id = l.product_ptr_id and 
		p.Id = im.idProduct_id and
        b.id = %s and
        operatorSystem is not null
        group by p.id
           """, [branch_id])
        rows = cursor.fetchall()

        data = []
        for row in rows:
            d = {}
            d['id'] = row[2]
            d['name'] = row[12]
            d['nameManufacture'] = row[4]
            # row[4] theo câu truy van thi no la discount
            d['currentPrice'] = row[3]
            d['id_product_color'] = row[1]
            d['currentColor'] = row[5]
            d['currentImage'] = row[14]
            d['operatorSystem'] = row[6]
            d['CPU'] = row[7]
            d['RAM'] = row[8]
            d['ROM'] = row[9]
            d['Battery'] = row[10]
            d['Others'] = row[11]
            d['amount'] = row[15]
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
                   ) as productDetail, o.orderDate,
                   bpc.Id
            FROM cellphoneapp_order o
            JOIN cellphoneapp_orderdetail od ON o.id = od.idOder_id
            JOIN cellphoneapp_branch_product_color bpc ON od.idBrandProductColor_id = bpc.id
            JOIN cellphoneapp_product_color pc ON bpc.idProductColor_id = pc.id
            JOIN cellphoneapp_product p ON pc.idProduct_id = p.id
            WHERE o.deliveryPhone = %s AND o.Status in (1,2) 
            GROUP BY o.id
        """, [deliveryPhone])
        rows = cursor.fetchall()
        data = [
            {
                'order_ID': row[0],
                'Status': row[1],
                'toltal_Price': row[2],
                'orderDate': row[4],
                'product_Detail': json.loads(row[3]),
                'id_branch_product_color': row[5]
            }
            for row in rows
        ]
    return JsonResponse(data, safe=False)


def search(request, branch_id, name_product):
    print("no co vao seacrhhhhhhhhhhhhhhhhhh")
    if name_product:
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT  pc.Id AS ProductColorId, pc.idProduct_id AS productID, pc.Price, pc.nameColor_id, bpp.discountRate, p.timeStart, p.timeEnd, bp.Amount, b.Name AS branch_name, p2.Name AS product_name, m.names AS manufacturer_name,i.linkImg, r.Title AS review_title, r.Content AS review_content,  bpc.Amount ,bp.Id
                        FROM cellphoneapp_promotion p 
                        JOIN cellphoneapp_branch_promotion_product bpp ON p.Id = bpp.idPromotion_id 
                        JOIN cellphoneapp_branch_product_color bp ON bpp.idBrandProductColor_id = bp.Id 
                        JOIN cellphoneapp_product_color pc ON bp.idProductColor_id = pc.Id 
                        JOIN cellphoneapp_branch b ON bp.idBranch_id = b.Id 
                        JOIN cellphoneapp_product p2 ON pc.idProduct_id = p2.Id 
                        JOIN cellphoneapp_manufacture m ON p2.nameManufacture_id = m.names 
                        LEFT JOIN cellphoneapp_imageproduct i ON p2.Id = i.idProduct_id 
                        LEFT JOIN cellphoneapp_review r ON p2.Id = r.idProduct_id 
                        JOIN cellphoneapp_branch_product_color bpc ON b.Id = bpc.idBranch_id AND pc.Id = bpc.idProductColor_id 
                        WHERE b.Id = %s  and  pc.nameColor_id like i.Name and p.Active = 1 and p2.Name like  %s
                        group by  pc.idProduct_id
                        LIMIT 0, 1000;

                  """, [branch_id, f'%{name_product}%'])
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
                # d['operatorSystem'] = row[14]
                # d['CPU'] = row[15]
                # d['RAM'] = row[16]
                # d['ROM'] = row[17]
                # d['Battery'] = row[18]
                # d['Others'] = row[19]
                d['amount'] = row[14]
                d['id_branch_product_color'] = row[15]
                data.append(d)

        # lay tat ca hang
        with connection.cursor() as cursor:
            cursor.execute("""
                                select bpc.idBranch_id,pc.Id as idProduct_color, p.Id as product_id ,pc.Price,p.nameManufacture_id,pc.nameColor_id, p.Name as tensanpham ,im.Name , im.linkImg, bpc.Amount,bpc.Id from cellphoneapp_branch b,cellphoneapp_branch_product_color bpc ,cellphoneapp_product_color pc, cellphoneapp_product p,cellphoneapp_imageproduct im
                                where b.Id = bpc.idBranch_id and
                                bpc.idProductColor_id = pc.Id and
                                pc.idProduct_id = p.Id and
                                p.Id = im.idProduct_id and
                                b.id = %s and p.Name like %s
                                group by p.id
                             """, [branch_id, f'%{name_product}%'])
            rows2 = cursor.fetchall()
            data2 = []
            for row in rows2:
                d = {}
                d['id'] = row[2]
                d['name'] = row[6]
                d['nameManufacture'] = row[4]
                # row[4] theo câu truy van thi no la discount
                d['currentPrice'] = row[3]

                d['price'] = row[3]

                d['id_product_color'] = row[1]
                d['currentColor'] = row[5]
                d['currentImage'] = row[8]
                # d['reviewTitle'] = row[12]
                # d['introduce'] = row[13]
                # d['operatorSystem'] = row[14]
                # d['CPU'] = row[15]
                # d['RAM'] = row[16]
                # d['ROM'] = row[17]
                # d['Battery'] = row[18]
                # d['Others'] = row[19]
                d['amount'] = row[9]
                d['id_branch_product_color'] = row[10]
                data2.append(d)

            # Duyệt qua từng phần tử trong rows
            for row in data:
                # Tìm phần tử trong rows2 có cùng id_branch_product_color với row
                for i in range(len(data2)):
                    if data2[i]['id_branch_product_color'] == row['id_branch_product_color']:
                        # Thay thế giá trị của phần tử trong rows2 bằng phần tử tương ứng trong rows
                        data2[i] = row
                        break

            return JsonResponse(data2, safe=False)

def search_price(request, branch_id,from_price, to_price,type_product):
    print('gia bat dau',from_price,'gia ket thuc',to_price)
    type = ""
    if type_product is 1:
        type = "phone"
    if type_product is 2:
        type = "laptop"
    with connection.cursor() as cursor:
        cursor.execute("""
                         SELECT  pc.Id AS ProductColorId, pc.idProduct_id AS productID, pc.Price, pc.nameColor_id, bpp.discountRate, p.timeStart, p.timeEnd, bp.Amount, b.Name AS branch_name, p2.Name AS product_name, m.names AS manufacturer_name,i.linkImg, r.Title AS review_title, r.Content AS review_content,  bpc.Amount ,bp.Id
                         FROM cellphoneapp_promotion p 
                         JOIN cellphoneapp_branch_promotion_product bpp ON p.Id = bpp.idPromotion_id 
                         JOIN cellphoneapp_branch_product_color bp ON bpp.idBrandProductColor_id = bp.Id 
                         JOIN cellphoneapp_product_color pc ON bp.idProductColor_id = pc.Id 
                         JOIN cellphoneapp_branch b ON bp.idBranch_id = b.Id 
                         JOIN cellphoneapp_product p2 ON pc.idProduct_id = p2.Id 
                         JOIN cellphoneapp_manufacture m ON p2.nameManufacture_id = m.names 
                         LEFT JOIN cellphoneapp_imageproduct i ON p2.Id = i.idProduct_id 
                         LEFT JOIN cellphoneapp_review r ON p2.Id = r.idProduct_id 
                         JOIN cellphoneapp_branch_product_color bpc ON b.Id = bpc.idBranch_id AND pc.Id = bpc.idProductColor_id 
                         WHERE b.Id = %s  and  pc.nameColor_id like i.Name and p.Active = 1 and (pc.Price - (pc.Price * bpp.discountRate))  BETWEEN %s AND  %s and p2.Type = %s
                         group by  pc.idProduct_id
                         LIMIT 0, 1000;

                   """, [branch_id, from_price, to_price,type])
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
            # d['operatorSystem'] = row[14]
            # d['CPU'] = row[15]
            # d['RAM'] = row[16]
            # d['ROM'] = row[17]
            # d['Battery'] = row[18]
            # d['Others'] = row[19]
            d['amount'] = row[14]
            d['id_branch_product_color'] = row[15]
            data.append(d)

        # lay tat ca hang
    with connection.cursor() as cursor:
        cursor.execute("""
                                 select bpc.idBranch_id,pc.Id as idProduct_color, p.Id as product_id ,pc.Price,p.nameManufacture_id,pc.nameColor_id, p.Name as tensanpham ,im.Name , im.linkImg, bpc.Amount,bpc.Id from cellphoneapp_branch b,cellphoneapp_branch_product_color bpc ,cellphoneapp_product_color pc, cellphoneapp_product p,cellphoneapp_imageproduct im
                                 where b.Id = bpc.idBranch_id and
                                 bpc.idProductColor_id = pc.Id and
                                 pc.idProduct_id = p.Id and
                                 p.Id = im.idProduct_id and
                                 b.id = %s and pc.Price between %s and %s and p.Type = %s
                                 group by p.id
                              """, [branch_id,  from_price, to_price,type])
        rows2 = cursor.fetchall()
        data2 = []
        for row in rows2:
            d = {}
            d['id'] = row[2]
            d['name'] = row[6]
            d['nameManufacture'] = row[4]
            # row[4] theo câu truy van thi no la discount
            d['currentPrice'] = row[3]

            d['price'] = row[3]

            d['id_product_color'] = row[1]
            d['currentColor'] = row[5]
            d['currentImage'] = row[8]
            # d['reviewTitle'] = row[12]
            # d['introduce'] = row[13]
            # d['operatorSystem'] = row[14]
            # d['CPU'] = row[15]
            # d['RAM'] = row[16]
            # d['ROM'] = row[17]
            # d['Battery'] = row[18]
            # d['Others'] = row[19]
            d['amount'] = row[9]
            d['id_branch_product_color'] = row[10]
            data2.append(d)

        # Duyệt qua từng phần tử trong rows
        for row in data:
            # Tìm phần tử trong rows2 có cùng id_branch_product_color với row
            for i in range(len(data2)):
                if data2[i]['id_branch_product_color'] == row['id_branch_product_color']:
                    # Thay thế giá trị của phần tử trong rows2 bằng phần tử tương ứng trong rows
                    data2[i] = row
                    break

        return JsonResponse(data2, safe=False)


import stripe
from rest_framework.exceptions import APIException

stripe.api_key = "sk_test_51Mm6CAJTSCX72rEN0osGovCVaSKimGjDCkJjqJmA4vxPFvOav5pfxsJwuaNsm2GQOObTWTsiyY5zPog6FIrVBSgf00zDD66h8d"
class StripeCheckoutView(APIView):
    def post(self, request):
        try:
            data = request.data
            # Lấy thông tin khách hàng
            name = data.get('name')
            phone_number = data.get('phone_number')
            address = data.get('address')
            print(name,phone_number,address)
            print("no co vao nhâ")
            # Tạo checkout session với thông tin khách hàng
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1MmCrRJTSCX72rENQoasGImp',
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card',],
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
                metadata={
                    'name': name,
                    'phone_number': phone_number,
                    'address': address,
                }
            )

            return redirect(checkout_session.url)
            # Tạo line items
            # line_items = [
            #     {
            #         "name": "T-shirt",
            #         "description": "Comfortable cotton t-shirt",
            #         "images": ["https://example.com/t-shirt.png"],
            #         "amount": 1500,
            #         "currency": "usd",
            #         "quantity": 2,
            #     }
            # ]

            # # Tạo session trên Stripe
            # session = stripe.checkout.Session.create(
            #     payment_method_types=["card"],
            #     line_items=line_items,
            #     mode="payment",
            #     success_url="http://localhost:3000/success",
            #     cancel_url="http://localhost:3000/cancel",
            # )
            #
            # return JsonResponse({"sessionId": session.id, "lineItems": line_items})
        except stripe.error.StripeError as e:
            raise APIException(str(e))

    def get(self, request):
        # Thực hiện các thao tác xử lý yêu cầu GET ở đây
        return Response({'message': 'Hello, GET request!'})



from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def create_payment_intent(request):
    data = json.loads(request.body)
    amount = data['amount']
    products = data['products']
    customer = data['customer']
    # print('lay duoc', amount, products)
    # print("thong tin khách hang la ", customer)


    products_post = [{'name': item['name'], 'id_branch_product_color': item['id_branch_product_color'],
                 'currentPrice': item['currentPrice']} for item in products]

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount),
            currency='vnd',
            payment_method_types=['card'],
            metadata={
                'customer_name': customer.get('name', ''),
                'customer_phone': customer.get('deliveryPhone', ''),
                'customer_address': customer.get('deliveryAddress', ''),
                'products': json.dumps(products_post),

            },
            payment_method_options = {
            "card": {
                "request_three_d_secure": "automatic"
            }
        }

        )
        return JsonResponse({
            'client_secret': intent.client_secret,
        })
    except Exception as e:
        print("co loi dau do", str(e))
        return JsonResponse({'error': str(e)})


@csrf_exempt
def order(request):
    # Lưu thông tin khách hàng
    data = json.loads(request.body)
    products = data['products']
    customer = data['customer']
    amountEachProduct = data['amountEachProduct']
    orderDate = data['orderDate']
    print("Thông tin khách hàng là", customer)
    print('so luong ', amountEachProduct)
    print("ngay dac hang la", orderDate)
    # print('san phẩm : ',products)

    # Kiểm tra và tạo đối tượng Role "customer" nếu chưa tồn tại
    role, created = Role.objects.get_or_create(nameRole='customer')

    # Tạo đối tượng User với thông tin khách hàng và Role "customer"
    user_order = User(
        Name=customer['name'],
        phoneNumber=customer['deliveryPhone'],
        Hometown=customer['deliveryAddress'],
        idRole=role
    )
    # Lưu đối tượng User vào CSDL
    user_order.save()
    order_user = Order(orderDate= orderDate,
                       deliveryAddress = customer['deliveryAddress'],
                       deliveryPhone = customer['deliveryPhone'],
                       Status = 1,
                       idUser = user_order
                       )
    order_user.save()

    # print('so luong cua no la ',products[0]['id_branch_product_color'])
    List_Order_detail = []
    for item in products:
        # Quantity = amountEachProduct.get(item['id_branch_product_color'])
        branch_product_color = Branch_Product_Color.objects.get(
            Id=item['id_branch_product_color'])  # truy xuất đối tượng Branch_Product_Color tương ứng
        # print('so luong san pham dat la ', Quantity)

        Order_detail = OrderDetail(idOder = order_user,
                                   idBrandProductColor = branch_product_color,
                                   Quantity = amountEachProduct.get(str(item['id_branch_product_color'])),
                                   unit_price = item['currentPrice']
                                   )
        List_Order_detail.append(Order_detail)
        # Order_detail.save()

    print('thong tin trong list order detail la', List_Order_detail)
    # lay doc nhat
    unique_ids = set()
    unique_items = []
    for item in List_Order_detail:
        if item.idBrandProductColor not in unique_ids:
            unique_ids.add(item.idBrandProductColor)
            unique_items.append(item)

    # Lặp qua các phần tử độc nhất
    for item in unique_items:
        print(item)
    OrderDetail.objects.bulk_create(unique_items)

    print('Thông tin sau khi lưu vào CSDL là', user_order)
    print("thong tin order",order_user)
    return JsonResponse({
        'oke': 'oke',
    })
