from django.shortcuts import render, redirect,get_object_or_404 as goo404
from django.http import HttpResponse
from .models import CodeShare
import hashlib
from django.contrib import messages
import random

def home(request):
    if request.method == 'GET':
        return render(request, 'app_code_share/homepage.html',{})   
    if request.method == 'POST':
        code_share = request.POST.get('code_snippet')
        file_name = request.POST.get('file_name')
        a=random.randrange(0,6)
        hash_value = str(hash(code_share))[a:a+8]
        if CodeShare.objects.filter(file_name=file_name).exists() == True and file_name != '':
              messages.error(request,'Awww!! An error. Probably we might have a file with same name. Damn those folks.')
              return render(request, 'app_code_share/homepage.html',{})
        CodeShare.objects.create(code=code_share, 
                                 hash_value=hash_value,
                                 file_name=file_name)
        return redirect('code_share:view_by_hash', hash_id=hash_value)

    
    
def view_by_hash(request, hash_id):  
    if request.method == 'GET':
        code_share = CodeShare.objects.get(hash_value=hash_id)
        return render(request, 'app_code_share/homepage.html', {'code_share': code_share,"filename":"yes"})   
    if request.method == 'POST':
        code_share = request.POST.get('code_snippet')
        code_obj = goo404(CodeShare,hash_value=hash_id)
        code_obj.code = code_share
        code_obj.save()
        return redirect('code_share:view_by_hash', hash_id=hash_id)


def view_by_file(request, file_name):  
    if request.method == 'GET':
        code_share = CodeShare.objects.get(file_name=file_name)
        return render(request, 'app_code_share/homepage.html', {'code_share': code_share,"filename":"yes"})   
    if request.method == 'POST':
        code_share = request.POST.get('code_snippet')
        code_obj = goo404(CodeShare,file_name=file_name)
        code_obj.code = code_share
        code_obj.save()
        return redirect('code_share:view_by_file', file_name=file_name)

    
    
