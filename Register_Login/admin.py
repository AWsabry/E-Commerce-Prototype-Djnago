from Register_Login.models import AccessToken,Profile
from django.contrib import admin

# Register your models here.


class Register(admin.ModelAdmin):
    # list_filter = ("email","first_name", "last_name", "last_modified")
    list_display = ("email","first_name", 'last_name','last_modified','is_active'
                  )




class AccessTokenAdmin(admin.ModelAdmin):
    model = Profile
    fieldsets = (
        (None, {"fields": (
                'user', 'token', 'expires', 'created'
            )}),
    )
    readonly_fields = ('token','created')
    list_display = ('user', 'token', 'created')



admin.site.register(Profile, Register)
admin.site.register(AccessToken, AccessTokenAdmin)

