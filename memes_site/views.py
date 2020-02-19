from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods

from memes_site.forms import UploadImageForm
from memes_site.models import Image, Vote, Comment, CommentVote
from memes_site.utils import format_date, prepare_data, count_rating, voted_comments


def index_page(request, page_number=1):
    """
    Start page view
    Displays :model:`memes_site.Image` with at least 1 up vote sorted by date descending
    :param request:
    :param page_number: default is equal 1
    :return: two images from selected page
    """
    images_list = [image for image in Image.objects.order_by('-id')
                   if Vote.objects.filter(image=image, type="UP").count() >= 1]

    paginator = Paginator(images_list, 2)
    page_images = paginator.get_page(page_number)
    format_date(page_images)
    data = prepare_data(page_images, request, paginator, page_number)
    return render(request, 'memes_site/index.html', data)


def fresh_view(request, page_number=1):
    """
    Displays all :model:`memes_site.Image` sorted by date descending
    :param request:
    :param page_number: default is equal 1
    :return: two images from selected page
    """
    images_list = Image.objects.order_by('-id')
    paginator = Paginator(images_list, 2)
    page_images = paginator.get_page(page_number)
    format_date(page_images)
    data = prepare_data(page_images, request, paginator, page_number)
    data['fresh'] = 1
    return render(request, 'memes_site/index.html', data)


def image_view(request, image_id):
    """
    Displays a single :model:`memes_site.Image`
    :param request:
    :param image_id:
    :return: Image with related comments
    """
    image = Image.objects.get(pk=image_id)
    image.date = image.date.strftime("%H:%M %d-%m-%Y")
    image.up_votes = Vote.objects.filter(image=image, type="UP").count()
    image.down_votes = Vote.objects.filter(image=image, type="DOWN").count()
    comments_number = Comment.objects.filter(image=image).count()
    comments_list = Comment.objects.filter(image=image)
    format_date(comments_list)
    count_rating(comments_list)
    user_voted_comments = voted_comments(comments_list, request.user.get_username())
    up_voted_comments = user_voted_comments[0]
    down_voted_comments = user_voted_comments[1]

    voted = ''
    user = User.objects.get(username=request.user.get_username())
    try:
        vote = Vote.objects.get(image=image, author=user)
        if vote.type == "UP":
            voted = "up"
        elif vote.type == "DOWN":
            voted = "down"
    except Vote.DoesNotExist:
        pass

    data = {
        'image': image,
        'comments_number': comments_number,
        'comments': comments_list,
        'down_voted': down_voted_comments,
        'up_voted': up_voted_comments,
        'username': request.user.get_username(),
        'voted': voted
    }
    return render(request, 'memes_site/image.html', data)


@require_http_methods(["POST"])
@login_required
def create_comment(request, image_id):
    """
    Adds :model:`memes_site.Comment` to database
    :param request:
    :param image_id:
    :return: redirect to commented image
    """
    user = User.objects.get(username=request.user.get_username())
    image = Image.objects.get(pk=image_id)
    comment_text = request.POST['comment']
    Comment.objects.create(author=user, content=comment_text, image=image)
    return HttpResponseRedirect('/image/%s' % image_id)


@require_http_methods(["POST"])
@login_required
def delete_comment(request):
    """
    Deletes :model:`memes_site.Comment` from database
    :param request:
    :return: redirect to main page
    """
    try:
        comment_id = request.POST['comment_id']
        next_page = request.POST['next']
        user = User.objects.get(username=request.user.get_username())
        comment = Comment.objects.get(id=comment_id, author=user)
        comment.delete()
        return HttpResponseRedirect(next_page)
    except Image.DoesNotExist:
        return HttpResponseRedirect("/")
    except KeyError:
        return HttpResponseRedirect("/")


@login_required
def image_upload_view(request):
    """
    Creates new :model:`memes_site.Image`
    :param request:
    :return: Redirect to upload view, with error if image is too wide
    """
    data = {
        'username': request.user.get_username()
    }
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(username=request.user.get_username())
            instance = Image(image=request.FILES['image'], author=user, title=request.POST['title'])
            if instance.is_valid():
                instance.save()
                return redirect("memes:image", instance.id)

            messages.add_message(request, messages.ERROR, "Zbyt szeroki obrazek!")
            return render(request, 'memes_site/upload.html', data)
    return render(request, 'memes_site/upload.html', data)


@login_required
def image_vote_up(request, image_id):
    """
    Creates a new image up vote or change existing one
    :param request:
    :param image_id:
    :return: redirect to previous page
    """
    image = Image.objects.get(pk=image_id)
    user = User.objects.get(username=request.user.get_username())
    try:
        vote = Vote.objects.get(image=image, author=user)
        if vote.type == 'UP':
            vote.delete()
        else:
            vote.type = 'UP'
            vote.save()
    except Vote.DoesNotExist:
        Vote.objects.create(image=image, author=user, type='UP')
    return HttpResponseRedirect("%s#%s" % (request.GET['next'], image.id))


@login_required
def image_vote_down(request, image_id):
    """
    Creates a new image down vote or change existing one
    :param request:
    :param image_id:
    :return: redirect to previous page
    """
    image = Image.objects.get(pk=image_id)
    user = User.objects.get(username=request.user.get_username())
    try:
        vote = Vote.objects.get(image=image, author=user)
        if vote.type == 'DOWN':
            vote.delete()
        else:
            vote.type = 'DOWN'
            vote.save()
    except Vote.DoesNotExist:
        Vote.objects.create(image=image, author=user, type='DOWN')
    return HttpResponseRedirect("%s#%s" % (request.GET['next'], image.id))


@login_required
def comment_vote(request, vote_type, comment_id):
    """
    Creates a new comment vote or change existing one
    :param request:
    :param vote_type: vote_down or vote_up
    :param comment_id:
    :return: redirect to voted comment
    """
    user = User.objects.get(username=request.user.get_username())
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return HttpResponseRedirect("/")
    try:
        user_comment_vote = CommentVote.objects.get(author=user, comment=comment)
        if user_comment_vote.type == 'UP':
            if vote_type == 'vote_down':
                user_comment_vote.type = 'DOWN'
                user_comment_vote.save()
            elif vote_type == 'vote_up':
                user_comment_vote.delete()
        elif user_comment_vote.type == 'DOWN':
            if vote_type == 'vote_down':
                user_comment_vote.delete()
            elif vote_type == 'vote_up':
                user_comment_vote.type = 'UP'
                user_comment_vote.save()
    except CommentVote.DoesNotExist:
        user_comment_vote = CommentVote.objects.create(author=user, comment=comment)
        if vote_type == 'vote_down':
            user_comment_vote.type = 'DOWN'
        elif vote_type == 'vote_up':
            user_comment_vote.type = 'UP'
        user_comment_vote.save()

    return HttpResponseRedirect("/image/%s/#%s" % (comment.image.id, comment_id))


@require_http_methods(["POST"])
@login_required
def image_delete(request):
    """
    Delete :model:`memes_site.Image` from database
    :param request:
    :return: Redirect to main page
    """
    try:
        image_id = request.POST['image_id']
        next_page = request.POST['next']
        user = User.objects.get(username=request.user.get_username())
        image = Image.objects.get(id=image_id, author=user)
        image.delete()
        return HttpResponseRedirect(next_page)
    except Image.DoesNotExist:
        return HttpResponseRedirect("/")
    except KeyError:
        return HttpResponseRedirect("/")


def user_view(request, username):
    """
    Display :model:`auth.User` activity
    :param request:
    :param username:
    :return: Uploaded, commented and voted images by user
    """
    user = User.objects.get(username=username)
    posts = Image.objects.filter(author=user).order_by('-id')
    user_comments = Comment.objects.filter(author=user).distinct('image')
    comments = [comment.image for comment in user_comments]
    user_votes = Vote.objects.filter(author=user)
    votes = [vote.image for vote in user_votes]
    data = {
        'posts': posts,
        'comments': comments,
        'votes': votes,
        'username': request.user.get_username(),
        'view_username': username
    }

    return render(request, 'memes_site/user.html', data)
