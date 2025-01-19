from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from .models import Post
from .forms import CommentForm, SubscribeForm

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
            messages.error(request, "There was an error with your submission. Please try again.")
    else:
        form = SubscribeForm()

    return render(
        request,
        "subscribe.html",
        {
        "form": form,
        }
    )