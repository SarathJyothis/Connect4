from django.db import models
import jsonfield
# Create your models here.

class docMas(models.Model):
    userId = models.CharField(max_length=500)
    docId = models.CharField(max_length=500,primary_key=True)
    origFileName = models.CharField(max_length=500)
    filePath = models.CharField(max_length=500)
    status = models.CharField(max_length=25)
    class Meta:
        db_table="DocMAS"
class docDtls(models.Model):
    docId = models.CharField(max_length=500,primary_key = True)
    invoiceNumber = models.CharField(max_length=500)
    buyer = models.CharField(max_length=500)
    seller = jsonfield.JSONField()
    billTo = jsonfield.JSONField()
    shipTo = jsonfield.JSONField()
    items = jsonfield.JSONField()
    totalPrice = models.CharField(max_length=100)
    GST = models.CharField(max_length=100)
    paymentInfo = jsonfield.JSONField()
    paymentStatus = models.CharField(max_length = 100)
    additional = jsonfield.JSONField()
    class Meta:
        db_table="DocDtls"

class users(models.Model):
    username = models.CharField(max_length=500,primary_key=True)
    psswd = models.CharField(max_length=200)
    class Meta:
        db_table="Users"