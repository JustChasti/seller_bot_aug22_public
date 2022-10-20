from django.db import models
from PIL import Image
from django_resized import ResizedImageField


def image_validator(image):
    basewidth = 300
    img = Image.open(f'files/{image}')
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(f'files/{image}')


class Product(models.Model):
    title = models.CharField(max_length=32)
    count = models.IntegerField()
    price = models.FloatField()
    photo = ResizedImageField(
        size=[200, 200],
        crop=['middle', 'center'],
        upload_to='files/'
    )


class Basket(models.Model):
    # создается когда неизвестный пользователь нажимает start
    # меняется когда пользователь нажимает корзина
    # идет подсчет всех релайшонов в таблице ниже и меняется итоговая сумма
    owner = models.IntegerField()
    checkout = models.FloatField(default=0.0)


class Product_to_Basket(models.Model):
    product = models.ForeignKey(Product, models.PROTECT)
    basket = models.ForeignKey(Basket, models.PROTECT)
    count = models.IntegerField()
