try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except: 
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import RedirectView
from django.utils import timezone

from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from .models import Post, Images

from rss.models import Feed
import feedparser

from django.forms import modelformset_factory

from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string

from django.contrib.auth.models import User


@login_required
def post_create(request):
	#if not request.user.is_staff or not request.user.is_superuser:
		#raise Http404
	ImagesFormset = modelformset_factory(Images, fields=('image',), extra=4)

	if request.method == 'POST':
		form = PostForm(request.POST or None)
		formset = ImagesFormset(request.POST or None, request.FILES or None)
		if form.is_valid() and formset.is_valid():
			instance = form.save()
			instance.user = request.user
			instance.save()

			for f in formset:
				if f.cleaned_data:
					try:
						photo = Images(post=instance, image=f.cleaned_data.get('image'))
						photo.save()
					except Exception as e:
						break

			return redirect(instance.get_absolute_url())

			# message success
			messages.success(request, "Post has been successfully created.")
			return HttpResponseRedirect(instance.get_absolute_url())
	else:
		form = PostForm()
		formset = ImagesFormset(queryset=Images.objects.none())


	context = {
		"submit": 'Create New Post',
		"form": form,
		"formset": formset,
	}
	return render(request, "post_form.html", context)

def post_detail(request, slug=None, id=None):
	instance = get_object_or_404(Post, slug=slug, id=id)
	queryset_list_limited = Post.objects.filter(~Q(id = instance.id)).order_by("-publish")[:6]


	favourite_posts = None
	if request.user.is_authenticated():
		favourite_posts = request.user.favourite.all()[:6]
	#if instance.publish > timezone.now().date() or instance.draft:
		#if not request.user.is_staff or not request.user.is_superuser:
			#raise Http404
	share_string = quote_plus(instance.content)

	is_favourite = False
	if instance.favourite.filter(id=request.user.id).exists():
		is_favourite = True

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)
		#return HttpResponseRedirect(new_comment.content_object.get_absolute_url())


	comments = instance.comments.order_by("timestamp")
	context = {
		"object_list_limited": queryset_list_limited,
		"favourite_posts": favourite_posts, 
		"title": instance.title,
		"is_favourite": is_favourite,
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
	}
	context_fav = {
		"favourite_posts": favourite_posts, 
		"instance": instance,
	}

	if request.is_ajax():
		html = render_to_string('comments.html', context, request=request)
		html_favorite = render_to_string('favourite_post.html', context_fav, request=request)
		return JsonResponse({'form': html, 'form_favorite':html_favorite, 'is_favourite': is_favourite})


	return render(request, "post_detail.html", context)



def post_favourite_list(request):
	today = timezone.now().date()
	user = request.user
	favourite_posts = user.favourite.all()

	query = request.GET.get("search")
	if query:
		favourite_posts = favourite_posts.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(favourite_posts, 2) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	context = {
		"favourite_posts": queryset, 
		"title": "List favourite",
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "post_favourite_list.html", context)





def favourite_post(request, slug=None, id=None):
	instance = get_object_or_404(Post, slug=slug, id=id)
	if instance.favourite.filter(id=request.user.id).exists():
		instance.favourite.remove(request.user)
	else:
		instance.favourite.add(request.user)

	return HttpResponseRedirect(instance.get_absolute_url())



	

class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        id_ = self.kwargs.get("id")
        print(slug)
        obj = get_object_or_404(Post, slug=slug, id=id_)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated():
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_

 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class PostLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, id=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, slug=slug, id=id)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        noliked = False
        if user.is_authenticated():
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
            	if user in obj.nolikes.all():
            		noliked = True
            		obj.nolikes.remove(user)
            		
            	liked = True
            	obj.likes.add(user)

            updated = True
        data = {
            "updated": updated,
            "liked": liked,
            "noliked": noliked
        }
        return Response(data)


class PostnoLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        id_ = self.kwargs.get("id")
        print(slug)
        obj = get_object_or_404(Post, slug=slug, id=id_)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated():
            if user in obj.nolikes.all():
                obj.nolikes.remove(user)
            else:
                obj.nolikes.add(user)
        return url_

class PostnoLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, id=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, slug=slug, id=id)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        noliked = False
        if user.is_authenticated():
            if user in obj.nolikes.all():
                noliked = False
                obj.nolikes.remove(user)
            else:
            	if user in obj.likes.all():
            		liked = True
            		obj.likes.remove(user)

            	noliked = True
            	obj.nolikes.add(user)

            updated = True
        data = {
            "updated": updated,
            "liked": liked,
            "noliked": noliked
        }
        return Response(data)

def post_list(request):
	today = timezone.now().date()

	url = 'https://abcnews.go.com/abcnews/technologyheadlines'
	feed = feedparser.parse(url)

	#queryset_list = Post.objects.active().order_by("-timestamp")
	#if request.user.is_staff or request.user.is_superuser:
	queryset_list = Post.objects.all().order_by("-id")
	nbr_blogs = queryset_list.count()
	nbr_users = User.objects.all().count()
	nbr_comments = Comment.objects.all().count()

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 4) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	
	context = {
		"object_list": queryset, 
		"nbr_blogs": nbr_blogs,
		"nbr_users": nbr_users,
		"nbr_comments": nbr_comments,
		"title": "List",
		"page_request_var": page_request_var,
		"today": today,
		"url": url,
		"feed": feed,
	}
	return render(request, "post_list.html", context)




@login_required
def post_update(request, slug=None, id=None):
	#if not request.user.is_staff or not request.user.is_superuser:
		#raise Http404
	instance = get_object_or_404(Post, slug=slug, id=id)
	ImagesFormset = modelformset_factory(Images, fields=('image',), extra=4, max_num=4)

	if instance.user != request.user:
		raise Http404

	if request.method == 'POST':
		form = PostForm(request.POST or None, instance=instance)
		formset = ImagesFormset(request.POST or None, request.FILES or None)
		if form.is_valid() and formset.is_valid():
			instance = form.save()
			instance.save()
			print(formset.cleaned_data)
			data = Images.objects.filter(post=instance)
			for index, f in enumerate(formset):
				if f.cleaned_data:
					if f.cleaned_data['id'] is None:
						photo = Images(post=instance, image=f.cleaned_data.get('image'))
						photo.save()
					elif f.cleaned_data['image'] is False:
						photo = Images.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
						photo.delete()
					else:
						photo = Images(post=instance, image=f.cleaned_data.get('image'))
						d = Images.objects.get(id=data[index].id)
						d.image = photo.image
						d.save()
				
			messages.success(request, "{} has been successfully updated!".format(instance.title))
			return HttpResponseRedirect(instance.get_absolute_url())
	else:
		form = PostForm(instance=instance)
		formset = ImagesFormset(queryset=Images.objects.filter(post=instance))

	context = {
		"submit": 'Update Post',
		"title": instance.title,
		"instance": instance,
		"form":form,
		"formset":formset,
	}
	return render(request, "post_edit.html", context)


@login_required
def post_delete(request, slug=None, id=None):
	#if not request.user.is_staff or not request.user.is_superuser:
		#raise Http404
	instance = get_object_or_404(Post, slug=slug, id=id)
	if instance.user != request.user:
		raise Http404

	instance.delete()
	messages.success(request, "Post has been successfully deleted!")
	return redirect("posts:list")



def about(request):
    return render(request, 'about.html', {'title': 'About'})