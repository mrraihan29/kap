from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Discussion, Comment
from .forms import DiscussionForm, CommentForm

@login_required
def create_discussion(request):
    add_discuss = DiscussionForm(request.POST or None)
    if request.method == 'POST':
        if add_discuss.is_valid():
            discussion = add_discuss.save(commit=False)
            discussion.user = request.user
            discussion.save()
            return redirect('discussions:list')
    discuss_list = Discussion.objects.all()
    return render(request, 'discussions/list.html', {'form': add_discuss, 'discussions': discuss_list})

@login_required
def delete_discussion(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if request.user.role == 'operator':
        discussion.delete()
        return redirect('discussions:list')
    else:
        return render(request, 'error.html', {'message': 'You do not have permission to delete this discussion.'})

@login_required
def discussion(request, pk=None):
    discussion = None
    category = request.GET.get("category", None)

    if pk:
        discussion = get_object_or_404(Discussion, pk=pk)

    add_discuss = DiscussionForm(request.POST or None)
    if request.method == "POST":
        if add_discuss.is_valid():
            discussion = add_discuss.save(commit=False)
            discussion.user = request.user
            discussion.save()
            add_discuss = DiscussionForm()
            # return redirect("discussions:list")

    discuss_list = Discussion.objects.all().order_by("-created_at")
    if category:
        discuss_list = discuss_list.filter(category=category)
    category_options = [{'value': category[0], 'label': category[1]} for category in Discussion.category_list]
    return render(
        request,
        "discussions/list.html",
        {
            "discussion_id": discussion.id if discussion else None,
            "discussions": discuss_list,
            "form": add_discuss,
            "category_options": category_options,
        },
    )

@login_required
def comments_discussion(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    comment_form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.discussion = discussion
            comment.user = request.user
            comment.save()
    return render(request, 'discussions/comment.html', {'discussion': discussion, 'comments': discussion.comments.all(), 'comment_form': comment_form})
