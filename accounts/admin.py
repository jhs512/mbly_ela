from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from accounts.models import User
from products.models import ProductPickedUser


class ProductPickedUserInline(admin.TabularInline):
    verbose_name = '고객이 PICK한 상품들'
    verbose_name_plural = '고객이 PICK한 상품'
    model = ProductPickedUser


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    list_display = ('id', 'profile_img_display', 'reg_date', 'update_date', 'username', 'name', 'gender', 'provider_type_code_display', 'provider_accounts_id', 'is_active', 'is_staff')
    list_display_links = tuple(list_display_field for list_display_field in list_display if list_display_field not in ['is_active', 'is_staff', 'provider_type_code_display'])
    list_filter = ('is_active', 'is_staff', 'gender')
    search_fields = ['username', 'name']
    inlines = (ProductPickedUserInline,)

    @admin.display(description="프로필", empty_value="이미지없음")
    def profile_img_display(self, user: User):
        return mark_safe(f"<img src={user.profile_img_url} style='width: 50px; border-radius:10px;' />")

    @admin.display(description="프로바이더")
    def provider_type_code_display(self, user: User):
        if user.provider_type_code == 'local':
            return user.get_provider_type_code_display()

        return mark_safe(f'<a href="{user.provider_link}" target="_blank">{user.get_provider_type_code_display()}</a>')
