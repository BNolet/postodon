import os
os.makedirs("database", exist_ok=True)

from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from libs.web import app
from libs.mastodon import post_random_to_mastodon



load_dotenv()

app.secret_key = os.getenv("flask_secret_key")

try:
    interval = int(os.getenv("interval"))
except TypeError:
    print("Interval not set in environment, defaulting to 86400 seconds (24 hours)")
    interval = 86400

try:
    port = int(os.getenv("port"))
except TypeError:
    print("Port not set in environment, defaulting to 5001")
    port = 5001

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
    app.run(host='0.0.0.0', port=port)