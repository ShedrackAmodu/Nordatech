from django.contrib import admin
from .models import Document, ViewerToken
from django.contrib.auth.models import User
from .utils import send_token_email
    
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'allow_download','allow_view')
    list_editable = ('allow_download','allow_view')
    search_fields = ('title','allow_view')
    list_filter = ('uploaded_at', 'allow_download','allow_view')
    ordering = ('-uploaded_at','allow_view')

    


@admin.register(ViewerToken)
class ViewerTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')
    search_fields = ('user__username',)
    list_filter = ('user__is_active',)
    actions = ['send_token_email']

    def send_token_email(self, request, queryset):
        for viewer_token in queryset:
            send_token_email(viewer_token.user.email, viewer_token.token)
        self.message_user(request, f"Tokens sent to {queryset.count()} users.")
    send_token_email.short_description = "Send login tokens via email"

def save_model(self, request, obj, form, change):
    if not obj.pk:  # If creating a new token
        user = User.objects.create_user(
            username=f"user_{obj.token}",
            password=str(obj.token)
        )
        obj.user = user
        send_token_email(user.email, obj.token)
    super().save_model(request, obj, form, change)

    
    
