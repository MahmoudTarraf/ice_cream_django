from django.db import models

class SpecialOfferModel(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.TextField()
    title = models.TextField(max_length=100)
    details = models.TextField()
    category = models.CharField(max_length=50)
    newPrice = models.CharField(max_length=50)
    oldPrice = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.id)