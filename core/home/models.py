from django.db import models

# Create your models here.
class color(models.Model):
    color_name=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.color_name


class person(models.Model):
    name= models.CharField(max_length=100)
    age=models.IntegerField()
    color = models.ForeignKey(color,null=True,blank=True,on_delete=models.CASCADE , related_name="color")
