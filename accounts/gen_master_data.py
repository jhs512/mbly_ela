from accounts.models import User


def gen_master(apps, schema_editor):
    # 운영서버에서 테스트를 위해 임시로 허용
    # if not settings.DEBUG:
    #     return

    User.objects.create_superuser(username="admin", password="admin", name="관리자", email="",
                                  gender=User.GenderChoices.FEMALE)

    for id in range(2, 6):
        username = f"user{id}"
        password = f"user{id}"
        name = f"이름{id}"
        email = f"test{id}@test.com"
        gender = User.GenderChoices.MALE

        User.objects.create_user(username=username, password=password, name=name, email=email, gender=gender)
