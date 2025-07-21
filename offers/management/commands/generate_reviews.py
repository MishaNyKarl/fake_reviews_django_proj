from django.core.management.base import BaseCommand
from offers.models import Offer, Review
from faker import Faker
import random
from datetime import datetime, timedelta


fake = Faker()


class Command(BaseCommand):
    # TODO: Подвязать гпт, чтобы сделать автоматически создаваемые отзывы для продукта из админки
    help = 'Генерирует фейковые отзывы'

    def add_arguments(self, parser):
        parser.add_argument('offer_slug', type=str)
        parser.add_argument('--count', type=int, default=20)

    def handle(self, *args, **options):
        offer = Offer.objects.get(slug=options['offer_slug'])
        for _ in range(options['count']):
            Review.objects.create(
                offer=offer,
                name=fake.name(),
                avatar='avatars/default.jpg',
                rating=random.choices([4, 5], weights=[1, 4])[0],
                text=fake.paragraph(nb_sentences=random.randint(2, 10)),
                date=datetime.now() - timedelta(days=random.randint(0, 300))
            )
        self.stdout.write(self.style.SUCCESS(f'Создано {options["count"]} отзывов на оффер {offer}'))