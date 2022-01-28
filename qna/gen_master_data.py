from django.contrib.contenttypes.models import ContentType

from products.models import Product
from qna.models import Question


def gen_master(apps, schema_editor):
    # 운영서버에서 테스트를 위해 임시로 허용
    # if not settings.DEBUG:
    #     return

    product = Product.objects.get(id=1)
    product_content_type = ContentType.objects.get_for_model(product)
    Question(user_id=2, content_type=product_content_type, object_id=product.id, body="이거 물빠짐 심한가요?").save()
    Question(user_id=3, content_type=product_content_type, object_id=product.id, body="이거 입으면 인싸?").save()

    product = Product.objects.get(id=2)
    product_content_type = ContentType.objects.get_for_model(product)
    Question(user_id=1, content_type=product_content_type, object_id=product.id, body="이거 원단이 튼튼한가요?").save()
    Question(user_id=3, content_type=product_content_type, object_id=product.id, body="이거 세탁해도 되나요?").save()
