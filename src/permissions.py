from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    اجازه دسترسی فقط به مالک پروفایل را می‌دهد. در روش‌های خواندنی (GET، HEAD، OPTIONS) همه می‌توانند دسترسی داشته باشند.
    """

    def has_permission(self, request, view):
        # اجازه دسترسی به هر کاربر احراز هویت‌شده
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # اگر درخواست به روش‌های خواندنی باشد (مثل GET، HEAD، OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # در غیر این صورت بررسی مالکیت پروفایل
        return obj.user == request.user  # بررسی اینکه آیا این پروفایل متعلق به کاربر درخواست‌کننده است
