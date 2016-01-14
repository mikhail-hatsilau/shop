import random
from django.core.management.base import BaseCommand
from waffle.models import Flag
from shop.models import Category, Product


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='+', type=int)

    def handle(self, *args, **options):
        products_count = options['count'][0]

        categories = Category.objects.all()
        seller_flag = Flag.objects.get(name='is_seller')
        sellers = seller_flag.users.all()

        for i in range(products_count):
            category_pos = random.randint(0, len(categories) - 1)
            category = categories[category_pos]
            price = random.uniform(1, 300)
            name = 'Product_' + str(i)
            description = 'Description'
            seller_pos = random.randint(0, len(sellers) - 1)
            seller = sellers[seller_pos]
            Product.objects.create(
                name=name,
                discription=description,
                price=price,
                seller=seller,
                category=category
            )
