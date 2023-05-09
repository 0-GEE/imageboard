from django.shortcuts import get_list_or_404, redirect, render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .models import *
from .forms import *
from .tags import process_query, OPERATORS
from .esets import EmptySet

BOARDNAME = "727Chan"

class IndexView(generic.ListView):
    template_name = 'imageboard/index.html'
    context_object_name = 'postlist'

    def get_queryset(self):
        """returns all posts sorted by published date"""

        return Posting.objects.order_by('-upload_date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['boardname'] = BOARDNAME
        ctx['digits'] = str(Posting.objects.count())
        return ctx



class SearchResultsView(generic.ListView):
    template_name = 'imageboard/results.html'
    context_object_name = 'results'

    def get_queryset(self):
        expression = self.request.GET.get('q')
        or_tags, and_tags, exclude_tags = process_query(expression)

        or_results = None
        and_results = None
        exclude_results = None

        # process or's:
        for tags1,tags2 in or_tags:
            pairing = Posting.objects.none()
            for tp_pairing in tags1:
                pairing |= Posting.objects.filter(pk=tp_pairing.post_id)

            for tp_pairing in tags2:
                pairing |= Posting.objects.filter(pk=tp_pairing.post_id)

            if or_results is None:
                or_results = pairing
            else:
                or_results &= pairing

                

        # process and's:
        iresult = Posting.objects.none()
        try:
            currname = and_tags.first().name
        except:
            currname = ""
        for tp_pair in and_tags:

            if tp_pair.name != currname:
                if and_results is None:
                    and_results = iresult
                else:
                    and_results &= iresult
                iresult = Posting.objects.filter(pk=tp_pair.post_id)
                currname = tp_pair.name
                continue

            iresult |= Posting.objects.filter(pk=tp_pair.post_id)

        if iresult.exists():
            if and_results is None:
                and_results = iresult
            else:
                and_results &= iresult

            

        # process excludes
        for tag in exclude_tags:
            iresult = Posting.objects.filter(pk=tag.post_id)

            if exclude_results is None:
                exclude_results = iresult
            else:
                exclude_results |= iresult


        if exclude_results is None:
            exclude_results = self.qs_return_empty()
        if and_results is None:
            and_results = EmptySet(model=Posting).none()
        if or_results is None:
            or_results = EmptySet(model=Posting).none()
        


        if isinstance(and_results, EmptySet) and isinstance(or_results, EmptySet):
            return Posting.objects.all().difference(exclude_results)
        
        if isinstance(and_results, EmptySet):
            return (and_results & or_results).difference(exclude_results)
        
        return (or_results & and_results).difference(exclude_results).order_by('-upload_date')
        


    def qs_return_empty(self):
        return Posting.objects.none()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['expression'] = self.request.GET.get('q').split(' ')
        ctx['boardname'] = BOARDNAME
        ctx['keywords'] = OPERATORS
        ctx['digits'] = str(Posting.objects.count())
        return ctx


def trace_postset(qs, name=None):
    if qs is None:
        if name:
            print("{} is None".format(name))
        else:
            print("None")
        return
    if name:
        print('\n{0} {1}:'.format(qs, name))
    else:
        print('\n{}:'.format(qs))
    for item in qs:
        print(' {0}: {1}'.format(item, item.title))
    print('end of QuerySet\n')

def trace_tp(tp, name=None):
    if tp is None:
        if name:
            print("{} is None".format(name))
        else:
            print("None")
        return
    if name:
        print('\n{0} {1}:'.format(tp, name))
    else:
        print('\n{}:'.format(tp))

    print('  tag {0} paired with post {1}'.format(tp.name, tp.post.title))

def get_detail(request, post_id):
    try:
        post = get_object_or_404(Posting, pk=post_id)
    except Http404:
        return render(request, 'imageboard/error.html', {
            'message': 'Post not found (404)',
            'boardname': BOARDNAME
        })

    comments = Comment.objects.filter(post_id=post_id)
    tags = Tag.objects.filter(post_id=post_id)

    return render(request, 'imageboard/viewpost.html', {
        'post': post,
        'tags': tags,
        'comments': comments,
        'boardname': BOARDNAME
    })


def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.instance.set_password(request.POST['password'])
            form.save()
            return HttpResponseRedirect(reverse('imageboard:index'))
    
    else:
        form = SignUpForm()

    return render(request, 'registration/register.html', {
        'form': form,
        'boardname': BOARDNAME
    })


@login_required
def post_image(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return HttpResponseRedirect(reverse('imageboard:index'))
    else:
        form = PostForm()
    
    return render(request, 'imageboard/upload.html', {
        'form': form,
        'boardname': BOARDNAME
    })


@login_required
def post_comment(request, post_id):

    try:
        parent_post = get_object_or_404(Posting, pk=post_id)
    except Http404:
        return render(request, 'imageboard/error.html', {
            'message': 'Parent post not found (404)',
            'boardname': BOARDNAME
        })

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():

            form.instance.author = request.user
            form.instance.post = parent_post
            form.save()

            return HttpResponseRedirect(reverse('imageboard:view', kwargs={'post_id': post_id}))
    else:
        form = CommentForm()

    return render(request, 'imageboard/comment.html', {
        'post': parent_post,
        'form': form,
        'boardname': BOARDNAME
    })
            

@login_required
def add_tag(request, post_id):
    try:
        parent_post = get_object_or_404(Posting, pk=post_id)
    except Http404:
        return render(request, 'imageboard/error.html', {
            'message': 'Parent post not found (404)',
            'boardname': BOARDNAME
        })

    if request.method == 'POST':
        form = TagForm(request.POST)

        if form.is_valid():

            form.instance.post = parent_post
            try:
                form.save()
            except Exception as e:
                return render(request, 'imageboard/tag.html', {
                    'post': parent_post,
                    'form': form,
                    'boardname': BOARDNAME,
                    'error': e
                })

            return HttpResponseRedirect(reverse('imageboard:view', kwargs={'post_id': post_id}))
    else:
        form = TagForm()

    return render(request, 'imageboard/tag.html', {
        'post': parent_post,
        'form': form,
        'boardname': BOARDNAME
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('imageboard:index'))
