from flask import Flask, render_template, redirect, request, flash
import random
import string
import json
import re

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flashing messages
shortened_urls = {}

def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))

def is_valid_url(url):
    # Simple regex to validate URLs
    regex = re.compile(
        r'^(https?:\/\/)?'  # Optional scheme
        r'([a-zA-Z0-9\-_]+\.)+[a-zA-Z]{2,}'  # Domain name
        r'(\/[a-zA-Z0-9\-_#?&%=~]*)*$',  # Optional path
        re.IGNORECASE
    )
    return re.match(regex, url)

@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None
    if request.method == "POST":
        long_url = request.form.get("long_url")

        # Validate the URL
        if not is_valid_url(long_url):
            flash("Please enter a valid URL!")
            return render_template("index.html", short_url=None)

        # Generate short URL
        short_url = generate_short_url()
        while short_url in shortened_urls:
            short_url = generate_short_url()

        shortened_urls[short_url] = long_url

        # Save to JSON file
        with open("urls.json", "w") as file:
            json.dump(shortened_urls, file)

    return render_template("index.html", short_url=short_url)


@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    return "URL not found", 404


if __name__ == "__main__":
    app.run(debug=True)
