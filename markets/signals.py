from django.db.models import Avg
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from markets.models import Market
from products.models import Product


@receiver(post_save, sender=Product)
def on_post_product_save(sender, instance: Product, created: bool, raw: bool, using, update_fields, **kwargs):
    market: Market = instance.market

    review_point = market.product_set.aggregate(Avg('review_point'))['review_point__avg']
    market.review_point = review_point
    market.save()
