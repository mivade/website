title: Flask and server-sent events
date: 2015-02-14 13:34
tags: python, flask, javascript, sse, gevent

I recently discovered the existence of the HTML5
[server-sent events][sse] standard. Although it lacks the
bidirectional communications of a websocket, SSE is perfect for the
publish-subscribe networking pattern. This pattern just so happens to
fit in conveniently with writing software to remotely monitor hardware
that many people might want to check in on at the same time.

[sse]: https://en.wikipedia.org/wiki/Server-sent_events

In order to try SSE out within a [Flask][] framework, I put together a
simple [demo app][] using [gevent][]. The core of the demo on the
Python side looks like this:

	:::python
	app = Flask(__name__)

	def event():
		while True:
			yield 'data: ' + json.dumps(random.rand(1000).tolist()) + '\n\n'
			gevent.sleep(0.2)

	@app.route('/')
	def index():
		return render_template('index.html')

	@app.route('/stream/', methods=['GET', 'POST'])
	def stream():
		return Response(event(), mimetype="text/event-stream")

This can be run either using gevent's WSGI server or [gunicorn][]
using gevent workers.

[Flask]: http://flask.pocoo.org/
[demo app]: https://github.com/mivade/flask-sse-demo
[gevent]: http://gevent.org/
[gunicorn]: http://gunicorn.org/
