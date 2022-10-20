from loguru import logger
import django
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'pgseller',
            'USER': 'postgres',
            'PASSWORD': '6@cSo75q',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    },
    INSTALLED_APPS=[
        'products',
    ]
)

django.setup()


from products.models import Product, Basket, Product_to_Basket


def get_chunks(objects, chunk):
    reassembled = []
    elements = []
    for i in objects:
        if len(elements) < chunk:
            elements.append(i)
        else:
            reassembled.append(elements)
            elements = []
            elements.append(i)
    if len(elements) > 0:
        reassembled.append(elements)
    return reassembled


def get_catalog(chunk):
    return get_chunks(
        Product.objects.values_list(
            'id',
            'title',
            'count',
            'price',
            'photo'),
        chunk
    )


def basket_creation(telegram_id):
    basket = Basket.objects.get_or_create(owner=telegram_id)
    return basket


def get_product_by_id(id):
    return Product.objects.get(id=id)


def get_basket_by_telegram(telegram_id):
    return Basket.objects.get(owner=telegram_id)


def add_product_too_basket(product, basket, count):
    try:
        relation = Product_to_Basket.objects.get(
            product=product,
            basket=basket
        )
        relation.count += count
        if relation.count > product.count:
            raise AttributeError
        relation.save()
    except ObjectDoesNotExist as e:
        relation = Product_to_Basket(
            product=product,
            basket=basket,
            count=count
        )
        relation.save()


def change_product_in_busket(product, basket, count):
    try:
        relation = Product_to_Basket.objects.get(
            product=product,
            basket=basket
        )
        relation.count = count
        relation.save()
    except Exception as e:
        logger.info(e)


def remove_product_from_busket(product, basket):
    try:
        relation = Product_to_Basket.objects.get(
            product=product,
            basket=basket
        )
        relation.delete()
    except Exception as e:
        logger.info(e)


def get_products_in_basket(basket):
    products = Product_to_Basket.objects.all().filter(basket=basket[0].id)
    products = products.values_list('product', 'count')
    data = []
    for i in products:
        product = Product.objects.get(id=i[0])
        data.append({
            'id': i[0],
            'title': product.title,
            'count': i[1],
            'price': product.price
        })
    return data


def clear_busket(basket):
    Product_to_Basket.objects.filter(basket=basket).delete()
