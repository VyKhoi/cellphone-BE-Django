from django.db import models
import decimal
# Create models here.

class Manufacture(models.Model):
    names = models.CharField(max_length=100, primary_key=True)

class Product(models.Model):
    Id = models.AutoField(primary_key=True) 
    Name = models.CharField(max_length=100)  
    nameManufacture = models.ForeignKey('Manufacture', on_delete = models.PROTECT)

class Color(models.Model):
    names = models.CharField(max_length=50, primary_key=True)
    idProduct = models.ManyToManyField('Product', through='Product_Color')

class Product_Color(models.Model):
    Id = models.AutoField(primary_key=True)
    idProduct = models.ForeignKey('Product', on_delete=models.CASCADE)
    nameColor = models.ForeignKey(Color, on_delete=models.CASCADE)
    Price = models.DecimalField(max_digits=10, decimal_places=2)

class Laptop(Product):
    CPU = models.CharField(max_length=50)
    RAM = models.CharField(max_length=50)
    ROM = models.CharField(max_length=50)
    Graphic_Card = models.CharField(max_length=50)
    Battery = models.CharField(max_length=30)
    operatorSystem = models.CharField(max_length=50)
    Others = models.CharField(max_length=50)

class Smartphone(Product):
    Operator_System = models.CharField(max_length=50)
    CPU = models.CharField(max_length=50)
    RAM = models.CharField(max_length=50)
    ROM = models.CharField(max_length=50)
    Battery = models.CharField(max_length=30)
    Others = models.CharField(max_length=50)

class Earphone(Product):
    connectionType = models.CharField(max_length=50)
    Design = models.CharField(max_length=50)
    Frequency_Response = models.CharField(max_length=50)

class Review(models.Model):
    Id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=100)
    Content = models.TextField()
    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)

class ImageProduct(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    linkImg = models.CharField(max_length=255)
    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    

class Branch(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    Phone = models.CharField(max_length=20)
    EstablishmentDate = models.DateField(auto_now=True)
    idProductColors = models.ManyToManyField(Product_Color, through='Branch_Product_Color')
    
class Branch_Product_Color(models.Model):
    Id = models.AutoField(primary_key=True)
    idProductColor = models.ForeignKey(Product_Color, on_delete=models.PROTECT)
    idBranch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    Amount = models.IntegerField(default=0)

class Promotion(models.Model):
    Id = models.AutoField(primary_key=True)
    timeStart = models.DateTimeField(auto_now=True)
    timeEnd = models.DateTimeField(auto_now=True)
    Active = models.BooleanField(default=False)
    idBrandProductColor = models.ManyToManyField(Branch_Product_Color, through='Branch_Promotion_Product')

class Branch_Promotion_Product(models.Model):
    Id = models.AutoField(primary_key=True)
    idPromotion = models.ForeignKey(Promotion, on_delete=models.PROTECT)
    idBrandProductColor = models.ForeignKey(Branch_Product_Color, on_delete=models.PROTECT)
    discountRate = models.FloatField(default=0.0)

class Comment(models.Model):
    Id = models.AutoField(primary_key=True)
    contentComment = models.CharField(max_length=100)
    idUser = models.ForeignKey('User', on_delete=models.CASCADE)
    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)


class Order(models.Model):
    Id = models.AutoField(primary_key=True)
    orderDate = models.DateTimeField(auto_now_add=True)
    deliveryAddress = models.CharField(max_length=50)
    deliveryPhone = models.CharField(max_length=50)
    Status = models.CharField(max_length=30)
    idBranchProductColor = models.ManyToManyField(Branch_Product_Color,through='OrderDetail')
    idUser = models.ForeignKey('User', on_delete=models.PROTECT)
    
class OrderDetail(models.Model):
    Id = models.AutoField(primary_key=True)
    idOder = models.ForeignKey(Order, on_delete=models.PROTECT)
    idBrandProductColor = models.ForeignKey(Branch_Product_Color, on_delete=models.PROTECT)
    Quantity = models.IntegerField(default=0)
    
class User(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=30)
    Email = models.EmailField(max_length=100)
    Gender = models.BooleanField(default=False)
    Hometown = models.CharField(max_length=50)
    userName = models.CharField(max_length=30)
    passWord = models.CharField(max_length=30)
    birthDay = models.DateField(auto_now=True)
    phoneNumber = models.CharField(max_length=20)
    idRole = models.ForeignKey('Role', on_delete=models.PROTECT)

class Role(models.Model):
    nameRole = models.CharField(max_length=30, primary_key = True)