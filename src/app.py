import os

from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from libs.web import app
from libs.mastodon import post_random_to_mastodon



load_dotenv()

app.secret_key = os.getenv("flask_secret_key")

interval = int(os.getenv("interval")) or 86400 # 24 hours

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'templates'))
app.template_folder = template_dir
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'static'))
app.static_folder = static_dir

scheduler = BackgroundScheduler()
scheduler.add_job(func=post_random_to_mastodon, trigger="interval", seconds=interval)
scheduler.start()


if os.getenv("env") == "debug":
    app.config["DEBUG"] = True


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)