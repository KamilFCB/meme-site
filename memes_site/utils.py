from django.contrib.auth.models import User

from memes_site.models import Vote, Comment, CommentVote


def format_date(objects):
    """
    Convert date to "H:M D-M-Y" format
    :param objects:
    :return: list of images with converted date
    """
    for obj in objects:
        obj.date = obj.date.strftime("%H:%M %d-%m-%Y")


def count_rating(comments):
    """
    Count rating of :model:`memes_site.Comment`
    :param comments:
    :return: sum of up and down votes
    """
    for comment in comments:
        comment.rating = CommentVote.objects.filter(comment=comment, type="UP").count()
        comment.rating -= CommentVote.objects.filter(comment=comment, type="DOWN").count()


def voted_comments(comments, username):
    """
    Creates list of upvoted and downvoted :model:`memes_site.Comment` by user
    :param comments:
    :param username:
    :return: Pair of lists
    """
    up_voted_comments = []
    down_voted_comments = []
    try:
        user = User.objects.get(username=username)
        for comment in comments:
            try:
                comment_vote = CommentVote.objects.get(comment=comment, author=user)
                if comment_vote.type == 'UP':
                    up_voted_comments.append(comment.id)
                else:
                    down_voted_comments.append(comment.id)
            except CommentVote.DoesNotExist:
                continue
    except User.DoesNotExist:
        pass

    return up_voted_comments, down_voted_comments


def voted_images(images, username):
    """
    Creates list of upvoted and downvoted :model:`memes_site.Image` by user
    :param images:
    :param username:
    :return: Pair of lists
    """
    down_votes = []
    up_votes = []
    try:
        user = User.objects.get(username=username)
        for image in images:
            try:
                vote = Vote.objects.get(image=image, author=user)
                if vote.type == 'UP':
                    up_votes.append(image.id)
                else:
                    down_votes.append(image.id)
            except Vote.DoesNotExist:
                continue
    except User.DoesNotExist:
        pass

    return down_votes, up_votes


def count_images_votes(images):
    """
    Adds rating to :model:`memes_site.Image`
    :param images:
    :return:
    """
    for image in images:
        image.up_votes = Vote.objects.filter(image=image, type="UP").count()
        image.down_votes = Vote.objects.filter(image=image, type="DOWN").count()


def pagination_manage(data, paginator, page_number, request):
    """
    Sets pagination data
    :param data:
    :param paginator:
    :param page_number:
    :param request:
    :return:
    """
    if page_number == paginator.page_range.start:
        data['disabled_prev'] = 1
    if page_number == paginator.page_range.stop - 1:
        data['disabled_next'] = 1
    if request.user.is_authenticated:
        data['username'] = request.user.get_username()


def page_list(paginator, page_number):
    """
    Creates list of page numbers included on the page
    :param paginator:
    :param page_number:
    :return: List of page numbers
    """
    return [i for i in range(paginator.page_range.start, paginator.page_range.stop)
            if (page_number - 2 <= i <= page_number + 2)]


def count_comments(images):
    """
    Get number of :model:`memes_site.Comment` related to :model:`memes_site.Image`
    :param images:
    :return: Number of comments
    """
    for image in images:
        image.comments_number = Comment.objects.filter(image=image).count()


def prepare_data(page_images, request, paginator, page_number):
    """
    Prepare data to display on main page and fresh images page
    :param page_images:
    :param request:
    :param paginator:
    :param page_number:
    :return: Page data
    """
    votes = voted_images(page_images, request.user.get_username())
    count_images_votes(page_images)
    count_comments(page_images)
    data = {
        'images': page_images,
        'username': request.user.get_username(),
        'comments_number': {'1': 0},
        'down_votes': votes[0],
        'up_votes': votes[1],
        'page_list': page_list(paginator, page_number),
        'page_number': page_number,
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
        'disabled_prev': 0,
        'disabled_next': 0
    }
    pagination_manage(data, paginator, page_number, request)
    return data
