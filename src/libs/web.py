import requests, bcrypt, os

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, LoginManager, fresh_login_required, current_user
from urllib.parse import urlencode

from .db import DB
from .models import *
from .mastodon import post_random_to_mastodon

base_url = os.getenv('domain') or '127.0.0.1'
port = os.getenv('port') or 5001

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.get_user(user_id=user_id)

db = DB()

@app.context_processor
def inject_now():
    return {'now': datetime.now(UTC)}

@app.route('/first-run', methods=['GET'])
def first_run():
    any_user_exists = db.get_user()
    if not any_user_exists:
        return render_template('first-run.html', loginout='Login')
    else:
        return render_template('403.html', reason="This page is no longer valid. Only one user is supported at this time."), 403


@app.route('/first-run', methods=['POST'])
def create_first_user():
    any_user_exists = db.get_user() # If no user exists
    if not any_user_exists:
        print('test')
        try:
            email        = request.form.get('email')
            username     = request.form.get('username')
            display_name = request.form.get('display_name')
            password     = request.form.get('password')
            pw_bytes = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
            is_admin     = True
            is_active    = True
        # TODO: Password encryption
            db.create_user(email=email,
                           username=username,
                           password=hashed_password,
                           display_name=display_name,
                           is_admin=is_admin,
                           is_active=is_active)
            return redirect(url_for('login'))
        except PermissionError:
            return render_template('403.html', reason="You are not permitted to create a new user this way."), 403
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        return render_template('403.html', reason="You are not permitted to create a new user this way."), 403

@fresh_login_required
@app.route('/add_social', methods=['GET'])
def add_social_page():
    return render_template('add_social.html')


@login_required
@app.route('/add_social/<instance_domain>', methods=['GET'])
def redirect_to_mastodon(instance_domain):
    instance = db.get_instance(instance_domain)
    user_id = current_user.id
    if not instance:
        print('REGISTERING APP')
        response = requests.post(f'https://{instance_domain}/api/v1/apps', data={
            'client_name': 'Postodon',
            'redirect_uris': f'http://{base_url}:{port}/add_social/{instance_domain}/callback',
            'scopes': 'read write',
            'website': 'https://postodon.org'
        })


        app_data = response.json()
        print(app_data)
        client_id = app_data['client_id']
        client_secret = app_data['client_secret']

        db.create_instance(domain=instance_domain,
                           client_id=client_id,
                           client_secret=client_secret)
        
        instance = db.get_instance(domain=instance_domain)

    oauth_params = {
        'client_id': instance.client_id,
        'response_type': 'code',
        'redirect_uri': f'http://{base_url}:{port}/add_social/{instance_domain}/callback',
        'scope': 'read write'
    }    
    oauth_url = f'https://{instance_domain}/oauth/authorize?' + urlencode(oauth_params)
        

    return redirect(oauth_url)

@login_required
@app.route('/add_social/<instance_domain>/callback', methods=['GET'])
def add_social(instance_domain):
    user_id = current_user.id

    code = request.args.get('code')
    if code:
        instance = db.get_instance(domain=instance_domain)

        token_response = requests.post(f'https://{instance_domain}/oauth/token', data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': f'http://{base_url}:{port}/add_social/{instance_domain}/callback',
            'client_id': instance.client_id,
            'client_secret': instance.client_secret,
            'scope': 'read write'
        })

        token_data = token_response.json()
        access_token = token_data.get('access_token')

        if access_token:
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            user_info_response = requests.get(f'https://{instance_domain}/api/v1/accounts/verify_credentials', headers=headers)
            user_info = user_info_response.json()

            db.create_social(username=user_info['username'],
                             instance_user_id=user_info['id'],
                             access_token=access_token,
                             server=instance_domain,
                             user_id=user_id)


    return redirect(url_for('index'))

@app.route('/login', methods=['GET'])
def login():
    if not db.get_user():
        return redirect(url_for('first_run'))
    
    return render_template('login.html', loginout="Login")

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    password_in_bytes = password.encode('utf-8')
    remember = True if request.form.get('remember') else False

    user = db.get_user(username=username)
    if user:
        stored_password_hash = user.password
    if not user or not bcrypt.checkpw(password_in_bytes, stored_password_hash):
        flash("Username or password incorrect. Try again.", "error")
        return redirect(url_for('login'))
    
    login_user(user, remember=remember)
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    user_id = current_user.id
    social = db.get_social(user_id=user_id)
    if not social:
        return redirect (url_for('add_social_page'))
    get_posts = requests.get(f'https://{social['instance_domain']}/api/v1/accounts/{social['instance_user_id']}/statuses', data={
        "limit": "5"
    }).json()
    posts = [{'poster':social['username'],
              'content': post['content'], 
              'posted_time': post['created_at']} for post in get_posts]
    return render_template('index.html',
                            current_page='home',
                            loginout="Logout",
                            posts=posts)

@app.route('/scheduler', methods=['GET'])
@login_required
def scheduler():
    return render_template('scheduler.html', 
                           current_page='scheduler', 
                           loginout="Logout")

@app.route('/content-manager', methods=['GET'])
@login_required
def content_manager():
    posts = db.get_posts_by_user(user_id=current_user.id)
    print(posts)

    return render_template('content-manager.html', 
                           current_page='content-manager',
                           posts=posts,
                           loginout="Logout")

@app.route('/content-manager/delete/<id>', methods=['DELETE'])
@login_required
def delete_queued_post(id):
    db.delete_post(user_id=current_user.id,post_id=id)

    posts = db.get_posts_by_user(user_id=current_user.id)
    return render_template('content-manager.html',
                            current_page='content-manager',
                            posts=posts,
                            loginlogout="Logout")


@app.route('/scheduler', methods=["POST"])
@login_required
def schedule_post():
    recurring = request.form.get("recurring")
    if recurring == "true":
        recurring = True
    else:
        recurring = False

    content = request.form.get("post_content")

    db.create_post(content=content, created_by_email=current_user.email, recurring=recurring)
    print('did something')
    return redirect(url_for('scheduler'))

@app.route('/post-to-mastodon', methods=["POST"])
def post_to_mastodon_route():
    try:
        post_random_to_mastodon()
        return jsonify({"status": "success", "message": "Post sent to Mastodon!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500