from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm,authenticate
from django.views.generic import ListView
from django.core.paginator import Paginator



class PostList(ListView):
	paginate_by = 2
	model = Post
# from models.core.forms import SignUpForm



def index(request):
	posts = Post.objects.all()
	paginator = Paginator(posts, 2)

	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)


	return render(request, 'blog/index.html',{'page_obj': page_obj})
	# return HttpResponse('My Homepage!')

def about(request):
	return HttpResponse('<h1>This is my Homepage</h1>')


def postDetail(request, pk):
	post = Post.objects.get(id=pk)
	return render(request, 'blog/post_detail.html', {'post' : post})


@login_required
def postCreate(request):
	form = PostForm()
	if request.method == 'POST'  and request.FILES['document']:
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
		# return HttpResponse(request.POST.get('title'))
	else:
		return render(request, 'blog/post_edit.html', {'form': form})

def nehapage(request):
	print(request.user)
	return render(request,'blog/neha.html')

@login_required
def post_edit(request, pk):
	post = Post.objects.get(pk=pk)
	if request.method == "POST"  and request.FILES['document']:
	    form = PostForm(request.POST, request.FILES, instance=post)
	    if form.is_valid():
	        post = form.save(commit=False)
	        post.author = request.user
	        post.published_date = timezone.now()
	        post.save()
	        return redirect('post_detail', pk=post.pk)
	else:
	    form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})


# def logout_view(request):
#     logout(request)
#     return redirect('post_list')


# 

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})