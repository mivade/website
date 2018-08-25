---
title: Using websockets with Flask via Tornado
date: 2014-12-15 19:44
tags: python, flask, tornado, javascript, websockets
---

I've been working on some projects for the lab that involve remotely
controlling hardware to perform various tasks. Since the hardware in
question is shared between different experiments, some sort of
asynchronous solution is needed, and a web-based client coupled with
[websockets][] seemed to be the best bet (this also leaves the option
open in the future to write a standalone client that is not
browser-based if desired).

There is no shortage of web frameworks for Python. Some of the more
popular ones are [Django][], [Flask][], [Tornado][], and
[Pyramid][]. Of these, I greatly prefer Flask for a number of reasons:

* Very thorough and easy to read documentation, including "snippets"
  with helpful tips and a very helpful community.
* Extreme ease of use for both small and large projects.
* Great use of decorators to further ease development.
* A large number of extensions to build up a complex project without
  requiring overhead for simple projects.

This is not to say that the other options are bad, but having looked
at all of them, Flask suits me best. The one problem: only Tornado
directly supports websockets since it is both an HTTP server and a web
framework in one, whereas the others utilize [WSGI][] for deployment.

Luckily, it is possible to leverage both the excellent asynchronous
features of Tornado and the power and ease of use of Flask through
Tornado's ability to serve WSGI apps with
`tornado.wsgi.WSGIContainer`. The Flask documentation shows a very
simple
[example](http://flask.pocoo.org/docs/0.10/deploying/wsgi-standalone/#tornado)
on how to do just that.

Integrating websockets into a Flask app is now pretty easy. Here's an
example on the server side:

```python
from __future__ import print_function
from flask import Flask, render_template
from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop

class WebSocket(WebSocketHandler):
	def open(self):
		print("Socket opened.")

    def on_message(self, message):
		self.write_message("Received: " + message)
		print("Received message: " + message)

def on_close(self):
	print("Socket closed.")

app = Flask('flasknado')

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == "__main__":
	container = WSGIContainer(app)
	server = Application([
		(r'/websocket/', WebSocket),
		(r'.*', FallbackHandler, dict(fallback=container))
	])
	server.listen(8080)
	IOLoop.instance().start()
```

The client-side Javascript is simple as well:

```javascript
var socket = null;
$(document).ready(function() {
	socket = new WebSocket("ws://" + document.domain + ":8080/websocket/");

    socket.onopen = function() {
		socket.send("Joined");
	}

	socket.onmessage = function(message) {
		var txt = message.data;
		$(".container").append("<p>" + txt + "</p>");
	}
});

function submit() {
	var text = $("input#message").val();
	socket.send(text);
	$("input#message").val('');
}
```

The full demo example can be found
[here](https://github.com/mivade/flasknado).

## Additional notes ##

There already exist at least two extensions for Flask to use
websockets:

* [Flask-Sockets](https://github.com/kennethreitz/flask-sockets)
* [Flask-SocketIO](https://github.com/miguelgrinberg/Flask-SocketIO)

However, both of these are based on
[gevent](http://gevent.org/). While gevent is nice, it still has
limited Python 3 support and does not work on Windows (sadly, a
requirement for some hardware drivers).

[websockets]: https://en.wikipedia.org/wiki/WebSocket
[Django]: https://www.djangoproject.com/
[Flask]: http://flask.pocoo.org/
[Tornado]: http://tornadoweb.org/
[Pyramid]: http://www.pylonsproject.org/
[WSGI]: https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface
