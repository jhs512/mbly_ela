from django.forms import ModelForm

from cart.models import CartItem
from products.models import ProductReal


class ProductCartAddForm(ModelForm):
    def __init__(self, *args, **kwargs):
        product_id: int = kwargs.pop('product_id', '')
        super().__init__(*args, **kwargs)
        self.fields['product_real'].label = "옵션"

        if product_id:
            product_reals = ProductReal.objects.filter(product_id=product_id)
            product_real_choices = [(i.id, f'{i.option_1_display_name} / {i.option_2_display_name}') for i in
                                    product_reals]

            self.fields['product_real'].choices = product_real_choices

        self.fields['quantity'].widget.attrs.update(min=1)
        self.fields['quantity'].widget.attrs.update(max=100)

    class Meta:
        model = CartItem
        fields = ['product_real', 'quantity']
