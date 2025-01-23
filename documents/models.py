from django.db import models
from django.contrib.auth.models import User
import uuid
import mimetypes
from django.contrib.auth.decorators import login_required


class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    allow_download = models.BooleanField(default=True)
    allow_view = models.BooleanField(default=True)# New field

    def __str__(self):
        return self.title
    


class ViewerToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.token)
    
class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)  # e.g., "viewed" or "downloaded"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.action} {self.document.title} on {self.timestamp}"

@login_required
def serve_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    # Check permissions
    if not document.allow_view:
        return HttpResponseForbidden("You do not have permission to view this document.")

    if not document.allow_download:
        # Serve the document inline (prevents download dialogs but not saving via dev tools)
        response = FileResponse(document.file, content_type=mimetypes.guess_type(document.file.name)[0])
        response["Content-Disposition"] = f"inline; filename={document.file.name}"
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        return response

    return HttpResponseForbidden("You are not authorized to access this document.")
    
    
