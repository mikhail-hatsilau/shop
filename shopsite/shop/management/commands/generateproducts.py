import random
from django.core.management.base import BaseCommand
from waffle.models import Flag
from shop.models import Category, Product


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='+', type=int)

    def handle(self, *args, **options):
        products_count = options['count'][0]

        categories = list(Category.objects.all())
        seller_flag = Flag.objects.get(name='is_seller')
        sellers = list(seller_flag.users.all())
        categories_length = len(categories)
        sellers_length = len(sellers)

        for i in range(products_count):
            category_pos = random.randint(0, categories_length - 1)
            category = categories[category_pos]
            price = random.uniform(1, 300)
            name = 'Product_' + str(i)
            description = 'Description'
            seller_pos = random.randint(0, sellers_length - 1)
            seller = sellers[seller_pos]
            Product.objects.get_or_create(
                name=name,
                discription=description,
                price=price,
                seller=seller,
                category=category
            )
