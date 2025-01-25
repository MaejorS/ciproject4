from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import CommentForm, SubscribeForm, PostForm


# Create your views here.
class PostList(generic.ListView):

    queryset = Post.objects.filter(status=1)
    template_name = "index.html"
    paginate_by = 6


def article_detail(request, slug):
    """
    Display an individual :model:`project4.Post`.

    **Context**

    ``post``
        An instance of :model:`project4.Post`.

    **Template:**

    :template:`article_detail.html`
    """

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )

    comment_form = CommentForm()

    return render(
        request,
        "article_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        }
    )


def subscribe(request):
    """
    Handles the subscription form submission.

    **Context**

    ``form``
        An instance of :form:`project4.SubscribeForm`.

    **Template:**

    :template:`subscribe.html`
    """

    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing!")
            return redirect("subscribe")
        else:
            messages.error(request, "Submission error.Try again.")
    else:
        form = SubscribeForm()

    return render(
        request,
        "subscribe.html",
        {
            "form": form,
        }
    )


def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request,
                                 messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('article_detail', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request,
                             messages.ERROR,
                             'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('article_detail', args=[slug]))


@login_required
def post_edit(request, slug):
    """
    View to edit a post.
    Accessible only to authors and superusers.
    """
    post = get_object_or_404(Post, slug=slug)

    # Check if the logged-in user is the author or a superuser
    if request.user != post.author and not request.user.is_superuser:
        messages.error(request,
                       "You do not have permission to edit this post.")
        return redirect('article_detail', slug=slug)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('article_detail', slug=post.slug)
        else:
            messages.error(request,
                           'Error updating the post. Please check the form.')
    else:
        form = PostForm(instance=post)

    return render(request, 'post_edit.html', {'form': form, 'post': post})


@login_required
def post_delete(request, slug):
    """
    Handle the deletion of a post.
    Only accessible by superusers or the author of the post.
    """
    post = get_object_or_404(Post, slug=slug)

    # Check if the logged-in user is the author or a superuser
    if post.author == request.user or request.user.is_superuser:
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('home')
    else:
        messages.error(request,
                       'You do not have permission to delete this post.')
        return redirect('article_detail', slug=slug)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = ['title', 'slug', 'content', 'status', 'excerpt']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Automatically set the author to the logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)
