from .models import Public_Post


def popular():
    posts = Public_Post.objects.all()
    p_p = {}
    for post in posts:
        cnt = post.comment_set.count()
        if cnt > 0:
            p_p[post.title] = post.comment_set.count()
        else:
            continue

    # displaying posts that contains comments to console
    # print(p_p)

    # printing top posts for testing before sorting
    # top_posts = p_p.keys()
    # print(top_posts)

    # Sorting the posts based on no of comments in Descendig order
    sort_orders = sorted(p_p.items(), key=lambda x: x[1], reverse=True)

    # printing top posts (most commented posts) after sorting in reverse order
    top_posts = sort_orders
    # print(top_posts)

    # taking an empty list to store popular posts
    pop_posts = []
    # Filtering popular posts from the Posts list by title
    for k in top_posts:
        # printing posts that have most comments
        # print(k)

        # getting the post with the help of post title
        post = Public_Post.objects.get(title=k[0])
        # Adding post to the popular posts list
        pop_posts.append(post)

    # displaying posts 
    # print('pop posts are : ', pop_posts)

    # popular_posts = pop_posts[0:2]
    return pop_posts
