from flask import Flask, render_template, request
import urllib.request
import xml.etree.ElementTree as ET

app = Flask(__name__)

def fetch_rss_feed(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except Exception as e:
        print(f"Error: {e}")
        return None

def parse_rss_feed(content):
    try:
        root = ET.fromstring(content)
        channel = root.find('channel')
        feed_title = channel.find('title').text if channel.find('title') is not None else "No Title"
        feed_description = channel.find('description').text if channel.find('description') is not None else "No Description"
        items = []
        for item in channel.findall('item'):
            title = item.find('title').text if item.find('title') is not None else "No Title"
            link = item.find('link').text if item.find('link') is not None else "#"
            description = item.find('description').text if item.find('description') is not None else "No Description"
            items.append({'title': title, 'link': link, 'description': description})
        return feed_title, feed_description, items
    except ET.ParseError as e:
        print(f"Parsing error: {e}")
        return None, None, []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        rss_url = request.form['rss_url']
        content = fetch_rss_feed(rss_url)
        if content:
            feed_title, feed_description, items = parse_rss_feed(content)
            return render_template('index.html', feed_title=feed_title, 
                                   feed_description=feed_description, items=items)
        else:
            return render_template('index.html', error="Could not fetch the RSS feed.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
