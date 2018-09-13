import json
import datetime

from django.shortcuts import redirect

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader

from django.utils.text import slugify

from .forms import UnicornUserCreationForm, CommentForm, BlogImageForm
from .models import Post, UnicornUser, Tag, Comment
# Create your views here.

# def home(request):
#     template = loader.get_template('blog/home.html')
#     return HttpResponse(template.render({}, request))


# def login(request):
#     template = loader.get_template('blog/login.html')
#     return HttpResponse(template.render({}, request))


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

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get(
            'username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


class NewPost(CreateView):
    model = Post
    fields = ['title', 'content']
    # exclude = ['author','tags']

    success_url = reverse_lazy('home')
    template_name = 'blog/new_post.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
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
        if existing_posts:
            slug += f'_{timestamp.month}_{timestamp.day}_{timestamp.year}'
            existing_posts = Post.objects.filter(slug=slug)
            if existing_posts:
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
        c_form = CommentForm(request.POST)
        if c_form.is_valid():

            if request.user.is_anonymous:
                author = None
            else:
                author = UnicornUser.objects.get(username=self.request.user)

            display_author = c_form.cleaned_data['display_author']
            content = c_form.cleaned_data['content']
            post = self.get_object()

            c = Comment(author=author, display_author=display_author,
                        content=content, parent_post=post)
            c.save()

            return HttpResponseRedirect(request.path)

        obj = self.get_object()
        context = self.get_context_data(object=obj)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)

        context['comments'] = self.get_object().post_comments.all().filter(
            active=True).order_by('timestamp')
        context['form'] = self.form_class(initial=self.initial)
        # context['comments'] = self.model.comments.all().order()
        return context


#  AJAX TESTS #
def ajax_comment_add(request):
    print('posting')

    body = json.loads(request.body)
    form = CommentForm(body)
    data = {'status': 'received'}

    if form.is_valid():
        print('form is valid')
        is_anonymous = False
        if request.user.is_anonymous:
            author = None
            is_anonymous = True
        else:
            author = UnicornUser.objects.get(username=request.user)

        display_author = form.cleaned_data['display_author']
        content = form.cleaned_data['content']

        post = Post.objects.get(id=body['pid'])

        new_comment = Comment(author=author, display_author=display_author,
                              content=content, parent_post=post)
        new_comment.save()

        data.update({'display_author': display_author,
                     'content': content,
                     'timestamp': new_comment.timestamp,
                     'cid': new_comment.pk,
                     'isAuthor': new_comment.author == post.author,
                     'isAnonymous': is_anonymous,
                     'status': 'success'})

        return JsonResponse(data)
    else:
        data.update({"status": "failed to add comment"})
        return JsonResponse(data)


@login_required
def ajax_comment_delete(request):
    body = json.loads(request.body)
    comment = Comment.objects.get(pk=body['cid'])
    comment.active = body['active']
    comment.save()

    data = {'deleted': 'comment deleted'}
    return JsonResponse(data)


@login_required
def ajax_comment_edit(request):
    body = json.loads(request.body)
    comment = Comment.objects.get(pk=body['cid'])
    comment.content = body['content']
    comment.last_edited = datetime.datetime.now()
    comment.save()

    data = {'edited': 'comment edited'}
    return JsonResponse(data)


@login_required
def ajax_comment_heart(request):
    body = json.loads(request.body)
    comment = Comment.objects.get(pk=body['cid'])
    status = ''
    if comment.likes.filter(username=request.user).exists():
        comment.likes.remove(request.user)
        status = 'unhearted'
    else:
        comment.likes.add(request.user)
        status = 'hearted'
    comment.save()

    data = {'hearted': status}
    return JsonResponse(data)


@login_required
def ajax_post_heart(request):
    body = json.loads(request.body)
    post = Post.objects.get(pk=body['pid'])
    status = ''
    if post.likes.filter(username=request.user).exists():
        post.likes.remove(request.user)
        status = 'unhearted'
    else:
        post.likes.add(request.user)
        status = 'hearted'
    post.save()

    data = {'hearted': status}
    return JsonResponse(data)


def ajax_img_upload(request):
    files = request.FILES

    form = BlogImageForm(request, files=files)

    data = {}

    if form.is_valid():
        img = form.save()
        data = {
            'url': img.docfile.url
        }

    return JsonResponse(data)
