from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from django.utils.text import slugify

from .forms import UnicornUserCreationForm, NewPostForm, CommentForm
from .models import Post, UnicornUser, Tag, Comment
# Create your views here.
import datetime

# def home(request):
#     template = loader.get_template('blog/home.html')
#     return HttpResponse(template.render({}, request))


def login(request):
    template = loader.get_template('blog/login.html')
    return HttpResponse(template.render({}, request))


# def post(request):
#     template = loader.get_template('blog/post.html')
#     return HttpResponse(template.render({}, request))

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

    def get(self, request, *args, **kwargs):
        if (not request.user.is_authenticated):
            return redirect('/signup/')
        return super(NewPost, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = UnicornUser.objects.get(username=self.request.user)

        # create list of tags from request and remove empty strings
        tags = self.request.POST.get('tags').replace('#', '').split(',')
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

    def get_queryset(self):
        queryset = self.model.objects.all()
        tags = self.request.GET.get('tags')
        if tags:
            queryset = queryset.filter(tags__name=tags)
        return queryset

    # def get_context_data(self, **kwargs):
    #     print('getting context data')
    #     context = super().get_context_data(**kwargs)
    #     context["tags"] = self.get_object.tags.all().order_by('name')
    #     print(context)
    #     print(context["tags"])
    #     return context


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'
    form_class = CommentForm
    initial = {'comment': 'Enter comment here', 'display_author': 'nobody'}

    def post(self, request, *args, **kwargs):
        print('posting')
        # print(request.POST)
        f = CommentForm(request.POST)
        if (f.is_valid()):

            if (request.user.is_anonymous):
                author = None
            else:
                author = UnicornUser.objects.get(username=self.request.user)

            display_author = f.cleaned_data['display_author']
            content = f.cleaned_data['content']
            post = self.get_object()

            c = Comment(author=author, display_author=display_author,
                        content=content, parent_post=post)
            c.save()

            return HttpResponseRedirect(request.path)

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def form_valid(self, form):
        print('************************doest this even get called?*****************************')

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)

        # context['comments'] = self.get_object().post_comments.all().filter(active=True).order_by('timestamp')
        context['form'] = self.form_class(initial=self.initial)
        # context['comments'] = self.model.comments.all().order()
        return context
