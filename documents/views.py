from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import login, logout
from .models import ViewerToken,ActivityLog,Document
from django.http import HttpResponseForbidden, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse
from django.contrib.auth.decorators import login_required


def login_with_token(request):
    if request.method == "POST":
        token = request.POST.get('token')
        try:
            viewer = ViewerToken.objects.get(token=token)
            login(request, viewer.user)
            return redirect('documents:list')
        except ViewerToken.DoesNotExist:
            return render(request, 'documents/login.html',  {'error': 'Invalid token. Please try again.'})
    return render(request, 'documents/login.html')


def logout_view(request):
    logout(request)
    return redirect('documents:login')

@staff_member_required
@login_required
def upload_document(request):
        if request.method == "POST":
            title = request.POST.get('title')
            file = request.FILES.get('file')
            Document.objects.create(title=title, file=file)
            messages.success(request, f"Document '{title}' uploaded successfully!")
            return redirect('documents:list')
        return render(request, 'documents/upload.html')
    
@login_required
def document_list(request):
    query = request.GET.get('q', '')
    documents = Document.objects.filter(title__icontains=query)
    paginator = Paginator(documents, 10)  # 10 documents per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'documents/list.html', {'page_obj': page_obj, 'query': query})

from django.http import FileResponse

# @login_required
# def serve_pdf(request, document_id):
#     document = get_object_or_404(Document, id=document_id)

#     if not document.allow_view:
#         return HttpResponseForbidden("You are not allowed to view this document.")

#     # Serve the file securely
#     response = FileResponse(document.file.open('rb'), content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename="{}"'.format(document.title)
#     return response



@login_required
def serve_pdf(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if not hasattr(document, 'allow_view') or not document.allow_view:
        return HttpResponseForbidden("You are not allowed to view this document.")
    # Serve the file securely
    return FileResponse(document.file.open("rb"), content_type="application/pdf")

