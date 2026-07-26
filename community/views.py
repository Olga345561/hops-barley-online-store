from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CommunityPost
from .forms import CommunityPostForm


def community_list(view_request):
    """Виводить список усіх активних дописів у спільноті"""
    posts = CommunityPost.objects.filter(is_active=True)
    context = {
        'posts': posts,
    }
    return render(view_request, 'pages/community_list.html', context)


@login_required  # Дозвіл створювати пости лише для залогінених користувачів
def create_community_post(view_request):
    """Логіка створення нового допису користувачем"""
    if view_request.method == 'POST':
        form = CommunityPostForm(view_request.POST, view_request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # Прив'язуємо поточного користувача як автора
            post.user = view_request.user
            post.save()
            return redirect('community:community_list')
    else:
        form = CommunityPostForm()

    context = {
        'form': form,
    }
    return render(view_request, 'pages/community_create_post.html', context)