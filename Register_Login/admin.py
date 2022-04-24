from Register_Login.models import AccessToken, Newsletter,Profile
from django.contrib import admin

# Register your models here.


class Register(admin.ModelAdmin):
    # list_filter = ("email","first_name", "last_name", "last_modified")
    list_display = ("email","first_name", 'last_name','last_modified','is_active'
                  )




class NewsletterAdmin(admin.ModelAdmin):
    model = Newsletter
    list_display = ('email',)



admin.site.register(Profile, Register)
admin.site.register(Newsletter, NewsletterAdmin)


