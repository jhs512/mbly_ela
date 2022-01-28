from rest_framework.serializers import ModelSerializer

from markets.models import Market


class MarketSerializer(ModelSerializer):
    class Meta:
        model = Market
        fields = ['id', 'reg_date', 'update_date', 'name', 'review_point']
