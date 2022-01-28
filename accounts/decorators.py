from django.contrib.auth.decorators import user_passes_test


# TODO 3주차 설명, 이런거 만들어서 사용하면 편해요.
def logout_required(function=None, url_if_logined='/'):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=url_if_logined
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
