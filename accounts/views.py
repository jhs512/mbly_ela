import os

import requests
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    logout_then_login, LoginView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.urls import reverse
from lazy_string import LazyString
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .decorators import logout_required
from .forms import JoinForm, FindUsernameForm, LoginForm, UserEditForm
from .models import User
from .serializers import MyTokenObtainPairSerializer, ApiRefreshRefreshTokenSerializer


class MyLoginView(SuccessMessageMixin, LoginView):
    template_name = "accounts/login.html"
    next_page = "/"

    form_class = LoginForm

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.success_message = LazyString(
            lambda: f'{self.request.user.name}님 환영합니다.')

    def get_initial(self):
        initial = self.initial.copy()
        initial['username'] = self.request.GET.get('username', None)

        return initial


@logout_required
def login(request: HttpRequest):
    return MyLoginView.as_view()(request)


def logout(request: HttpRequest):
    messages.success(request, "로그아웃 되었습니다.")
    return logout_then_login(request)


@logout_required
def join(request: HttpRequest):
    if request.method == 'POST':
        form = JoinForm(request.POST, request.FILES)
        if form.is_valid():
            signed_user = User.join_by_form(form)
            auth_login(request, signed_user)
            messages.success(request, "회원가입이 완료되었습니다. 환영합니다.")
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = JoinForm()
    return render(request, 'accounts/join.html', {
        'form': form,
    })


@login_required
def edit(request: HttpRequest):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "회원정보가 수정되었습니다.")
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'accounts/edit.html', {
        'form': form,
    })


@logout_required
def find_username(request: HttpRequest):
    if request.method == 'POST':
        form = FindUsernameForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            qs: QuerySet = User.objects.filter(email=email, name=name)

            if not qs.exists():
                messages.warning(request, "일치하는 회원이 존재하지 않습니다.")
            else:
                user: User = qs.first()
                messages.success(request, f"해당회원의 아이디는 {user.username} 입니다.")
                return redirect(reverse("accounts:login") + '?username=' + user.username)
    else:
        form = FindUsernameForm()

    return render(request, 'accounts/find_username.html', {
        'form': form,
    })


@logout_required
def kakao_login(request: HttpRequest):
    REST_API_KEY = os.environ.get("KAKAO_APP__REST_API_KEY")
    REDIRECT_URI = os.environ.get("KAKAO_APP__LOGIN__REDIRECT_URI")

    next = request.GET.get('next', '')
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code&state={next}"
    )


@logout_required
def kakao_login_callback(request):
    code = request.GET.get("code")

    REST_API_KEY = os.environ.get("KAKAO_APP__REST_API_KEY")
    REDIRECT_URI = os.environ.get("KAKAO_APP__LOGIN__REDIRECT_URI")

    token_request = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}"
    )

    token_json = token_request.json()

    error = token_json.get("error", None)
    if error is not None:
        raise Exception("카카오 로그인 에러")

    access_token = token_json.get("access_token")

    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()

    id = profile_json.get("id")
    profile: dict = profile_json.get("kakao_account").get("profile")

    nickname = profile.get("nickname", "")
    thumbnail_image_url = profile.get("thumbnail_image_url", "")

    User.login_with_kakao(request, id, nickname, thumbnail_image_url)

    messages.success(request, f"{nickname}님 환영합니다. 카카오톡 계정으로 로그인되었습니다")

    next = request.GET.get('state', '')

    return redirect("main" if not next else next)


# 이걸 사용하는 이유는 JWT 토큰안의 페이로드 안에 추가적인 내용(email, profile_img_url 등)을 담기 위함
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# TODO 3주차 설명, 엑세스키와 리프레시키를 모두 재발급하는 로직이 필요합니다.
class ApiRefreshRefreshTokenView(GenericAPIView):
    permission_classes = ()  # 중요, 이렇게 해야 접근이 가능합니다.
    authentication_classes = ()  # 중요, 이렇게 해야 접근이 가능합니다.

    serializer_class = ApiRefreshRefreshTokenSerializer

    # 리프레시 토큰 자체를 다시 발급
    def post(self, request: HttpRequest):
        serializer: ApiRefreshRefreshTokenSerializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        refresh: str = serializer.validated_data['refresh']

        try:
            refresh_token: RefreshToken = RefreshToken(refresh)
        except TokenError as e:
            raise InvalidToken(e)

        user: User = get_object_or_404(User, id=refresh_token['user_id'])
        new_refresh_token = MyTokenObtainPairSerializer.get_token(user)  # 이걸로 토큰을 생성해야 합니다. 다른 방법으로 하면 페이로드에 필수데이터가 누락된 버전이 생김
        new_access_token = new_refresh_token.access_token
        refresh_token.blacklist()  # 꼭 블랙리스트에 넣어주세요.

        return Response({
            'refresh': str(new_refresh_token),
            'access': str(new_access_token),
        })
