import random
from mastodon import Mastodon
from .db import DB

db = DB()

def post_to_mastodon(post, user):
    mastodon = Mastodon(
        access_token=user.masto_access_token,
        api_base_url=user.base_url
    )

    mastodon.status_post(post)

def post_random_to_mastodon():
    user = db.get_user()
    posts = db.get_posts_by_user(user_id=user.id)
    if posts:
            random_post = random.choice(posts)
            social = db.get_social(user_id=user.id)
            user.masto_access_token = social['access_token']
            user.base_url = social['instance_domain']
            post_to_mastodon(random_post['content'], user)
            print(f'Posted: {random_post['content']} to Mastodon')
    else:
        print("No posts available to pick from")