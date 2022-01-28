from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core import exceptions
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.views.decorators.http import require_GET, require_POST
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAdminUser

from accounts.models import User
from cart.forms import ProductCartAddForm
from products.models import Product, ProductCategoryItem, ProductReal
from products.serializers import ProductSerializer, ProductCreateSerializer, ProductRealSerializer, \
    ProductPatchSerializer, ProductRealCreateSerializer
from qna.forms import QuestionForm
from qna.models import Question


# 일반사용자용 뷰 시작
# 상품 리스트
@require_GET
def product_list(request: HttpRequest):
    # 카테고리 정보
    product_cate_items = ProductCategoryItem.objects.all()

    # 필터요소 1, 검색어가 있다면 저장
    search_keyword = request.GET.get('search_keyword', '')
    # 필터요소 2, 카테고리 아이템이 있다면 저장
    product_cate_item_id = request.GET.get('product_cate_item_id', '')

    # 선택된 카테고리 아이템의 이름을 저장, 없으면 빈값
    product_cate_item_name, = (product_cate_item.name for product_cate_item in product_cate_items if
                               product_cate_item.id == int(product_cate_item_id)) if product_cate_item_id else tuple(
        [''])

    # 페이징
    page = request.GET.get('page', '1')

    products = Product \
        .objects \
        .prefetch_related('cate_item') \
        .prefetch_related('product_reals') \
        .prefetch_related('market') \
        .order_by('-id')

    if request.user.is_authenticated:
        products = products \
            .prefetch_related(
            Prefetch('product_picked_users', queryset=User.objects.filter(id=request.user.id), to_attr='picked_user'))

    if search_keyword:
        products = products.filter(display_name__icontains=search_keyword)

    if product_cate_item_id:
        products = products.filter(cate_item_id=product_cate_item_id)

    paginator = Paginator(products, 8)  # 페이지당 10개씩 보여주기
    products = paginator.get_page(page)

    return render(request, "products/product_list.html", {
        "products": products,
        "product_cate_item_name": product_cate_item_name,
        "product_cate_items": product_cate_items
    })


# 공통적으로 사용되는 함수
# products/product_detail.html 을 위한 기본 데이터
def _get_product_detail_context(request: HttpRequest, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_add_form = ProductCartAddForm(product_id=product_id)

    product_reals = product.product_reals.order_by('option_1_display_name', 'option_2_display_name')
    question_create_form = QuestionForm()
    questions = product \
        .questions \
        .select_related('user') \
        .order_by('-id')

    user_picked = product.product_picked_users.filter(id=request.user.id).exists()

    return {
        "product": product,
        "product_reals": product_reals,
        "questions": questions,
        "question_create_form": question_create_form,
        "user_picked": user_picked,
        "cart_add_form": cart_add_form,
    }


# 상품 상세
@require_GET
def product_detail(request: HttpRequest, product_id):
    context = _get_product_detail_context(request, product_id)

    return render(request, "products/product_detail.html", context)


# 질문 생성화면, 질문생성 처리
@login_required
@require_POST
def question_create(request: HttpRequest, product_id):
    context = _get_product_detail_context(request, product_id)
    product: Product = context['product']

    if request.method == "POST":
        context['question_create_form'] = QuestionForm(request.POST)
        if context['question_create_form'].is_valid():
            question = context['question_create_form'].save(commit=False)
            question.content_type = ContentType.objects.get_for_model(product)
            question.object_id = product.id
            question.user = request.user
            question.save()
            messages.success(request, "질문이 등록되었습니다.")

            return redirect("products:detail", product_id=product.id)

    return render(request, "products/product_detail.html", context)


# 질문 삭제
@login_required
@require_POST
def question_delete(request: HttpRequest, product_id, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.user != question.user:
        raise exceptions.PermissionDenied()

    question.delete()

    messages.success(request, f"{question_id}번 질문이 삭제되었습니다.")

    return redirect("products:detail", product_id=product_id)


# 질문 수정
@login_required
def question_modify(request: HttpRequest, product_id, question_id):
    context = _get_product_detail_context(request, product_id)
    question = get_object_or_404(Question, id=question_id)

    if request.user != question.user:
        raise exceptions.PermissionDenied()

    if request.method == "POST":
        question_modify_form = QuestionForm(request.POST, instance=question)

        if question_modify_form.is_valid():
            question_modify_form.save()
            messages.success(request, f"{question.id}번 질문이 수정되었습니다.")
            return redirect("products:detail", product_id=product_id)
    else:
        question_modify_form = QuestionForm(None, instance=question)

    context['question_modify_form'] = question_modify_form
    context['question'] = question

    return render(request, "products/product_detail.html", context)


@login_required
@require_POST
def product_pick(request: HttpRequest, product_id):
    request.user.picked_products.add(product_id)
    messages.success(request, f"{product_id}번 상품에 좋아요.")
    return redirect("products:detail", product_id=product_id)


@login_required
@require_POST
def product_unpick(request: HttpRequest, product_id):
    request.user.picked_products.remove(product_id)
    messages.success(request, f"{product_id}번 상품에 좋아요 취소.")
    return redirect("products:detail", product_id=product_id)


# 최종관리자용 뷰 시작
# TODO 3주차 설명, Admin 용 상품 리스트와 생성 처리 뷰
class AdminApiProductListCreateView(ListCreateAPIView):
    # admin만 사용가능 하도록
    permission_classes = [IsAdminUser]

    queryset = Product \
        .objects \
        .prefetch_related('market') \
        .prefetch_related('product_reals') \
        .prefetch_related('cate_item') \
        .all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        else:
            return ProductCreateSerializer


# TODO 3주차 설명, Admin 용 상품 단건조회, 수정(PATCH), 삭제 처리 뷰
class AdminApiProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]

    # 일부러 PUT을 없애기 위해
    allowed_methods = ('GET', 'PATCH', 'DELETE', 'OPTION')

    queryset = Product \
        .objects \
        .prefetch_related('market') \
        .prefetch_related('product_reals') \
        .all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        else:
            return ProductPatchSerializer


# TODO 3주차 설명, Admin 용 상품 단건조회, 수정(PATCH), 삭제 처리 뷰
class AdminApiProductRealListCreateView(ListCreateAPIView):
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        request.data.update({'product': kwargs['product_id']})
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        product_id = self.kwargs['product_id']

        return ProductReal \
            .objects \
            .filter(product=product_id)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductRealSerializer
        else:
            return ProductRealCreateSerializer
