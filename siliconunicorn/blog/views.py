from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from django.utils.text import slugify

from .forms import UnicornUserCreationForm, NewPostForm
from .models import Post, UnicornUser, Tag
# Create your views here.
import datetime

# def home(request):
#     template = loader.get_template('blog/home.html')
#     return HttpResponse(template.render({}, request))

def login(request):
    template = loader.get_template('blog/login.html')
    return HttpResponse(template.render({}, request))

def post(request):
    template = loader.get_template('blog/post.html')
    return HttpResponse(template.render({}, request))

# def newPost(request):
#     template = loader.get_template('blog/new_post.html')
#     return HttpResponse(template.render({}, request))

class SignUp(CreateView):
    form_class = UnicornUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'blog/signup.html'

class NewPost(CreateView):
    model = Post
    fields = ['title', 'content']
    # exclude = ['author','tags']

    success_url = reverse_lazy('home')
    template_name = 'blog/new_post.html'

    def get (self, request, *args, **kwargs):
        if (not request.user.is_authenticated):
            return redirect('/signup/')
        return super(NewPost, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = UnicornUser.objects.get(username=self.request.user)

        # create list of tags from request and remove empty strings
        tags = self.request.POST.get('tags').replace('#','').split(',')
        tags = list(filter(None, tags))

        for tag in tags:
            if Tag.objects.filter(name=tag).exists():
                pass
            else:
                new_tag = Tag(name=tag)
                new_tag.save()
        all_tags = Tag.objects.filter(name__in=tags)
        print(all_tags)

        timestamp = datetime.datetime.now()

        slug = slugify(post.title)
        existing_posts = Post.objects.filter(slug=slug)
        if len(existing_posts) > 0:
            slug += f'_{timestamp.month}_{timestamp.day}_{timestamp.year}'
            existing_posts = Post.objects.filter(slug=slug)
            if len(existing_posts) > 0:
                slug += f'_str{timestamp.hour}_{timestamp.minute}'

        post.slug = slug
        post.date_published = timestamp
        post.save()

        post.tags.set(all_tags)
        post.save()

        return HttpResponseRedirect('/')

class MostRecentEntriesList(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'blog/home.html'
    paginate_by = 5

    # def get_context_data(self, **kwargs):
    #     print('getting context data')
    #     context = super().get_context_data(**kwargs)
    #     context["tags"] = self.get_object.tags.all().order_by('name')
    #     print(context)
    #     print(context["tags"])
    #     return context

class PostDetail(DetailView):
    model = Post
    template_name='blog/post.html'
    context_object_name = 'post'
