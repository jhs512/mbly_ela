from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.http import HttpRequest
# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404, resolve_url
from django.views.decorators.http import require_POST, require_GET

from cart.forms import ProductCartAddForm
from cart.models import CartItem
from products.models import ProductReal


@login_required
@require_POST
def add(request: HttpRequest):
    product_real: ProductReal = ProductReal.objects.get(id=request.POST.get('product_real'))
    form = ProductCartAddForm(request.POST)

    if form.is_valid():
        cart_items_qs: QuerySet = CartItem.objects.filter(user=request.user, product_real=product_real)

        if cart_items_qs.exists():
            old_cart_item = cart_items_qs.first()
            old_cart_item.quantity += int(form.cleaned_data['quantity'])
            old_cart_item.save()
        else:
            cart_item = form.save(commit=False)
            cart_item.user = request.user
            cart_item.save()

        name = f'{product_real.product.display_name}/{product_real.option_1_display_name}/{product_real.option_2_display_name}'

        messages.success(request,
                         f"장바구니에 상품({name})이 {form.cleaned_data['quantity']}개 추가되었습니다. <a href='{resolve_url('cart:list')}'>장바구니로 이동</a>")
        return redirect('products:detail', product_real.product.id)

    messages.error(request, form['quantity'].errors, 'danger')
    return redirect('products:detail', product_real.product.id)


@login_required
@require_GET
def list(request: HttpRequest):
    cart_items = CartItem \
        .objects \
        .select_related('product_real', 'product_real__product', 'product_real__product__market', 'product_real__product__cate_item') \
        .filter(user=request.user)

    return render(request, "cart/list.html", {
        "cart_items": cart_items
    })


@login_required
@require_POST
def delete_items(request: HttpRequest):
    if not request.POST.get('ids', ''):
        raise ValidationError("ids 가 입력되지 않았습니다.")

    ids = map(int, request.POST.get('ids').split(','))

    cart_items = CartItem.objects.filter(id__in=ids)

    for cart_item in cart_items:
        if cart_item.user != request.user:
            raise PermissionError()
        cart_item.delete()

    messages.success(request, "해당 장바구니 품목들이 삭제되었습니다.")

    return redirect('cart:list')


@login_required
@require_GET
def delete(request: HttpRequest, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if cart_item.user != request.user:
        raise PermissionError()

    cart_item.delete()

    messages.success(request, "해당 장바구니 품목이 삭제되었습니다.")

    return redirect('cart:list')


@login_required
@require_POST
def modify(request: HttpRequest, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if cart_item.user != request.user:
        raise PermissionError()

    cart_item.quantity = int(request.POST.get('quantity'))
    cart_item.save()

    messages.success(request, "해당 장바구니 품목의 개수가 수정되었습니다.")

    return redirect('cart:list')
