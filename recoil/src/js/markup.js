import marked from 'marked';

/** Fetch and convert Markdown to HTML. */
export class MarkerUpper {
    constructor(src) {
        this.src = src;
    }

    fetch() {
        var content = null,
            startTime = new Date().getTime()/1000,
            request = new XMLHttpRequest();

        request.open('GET', '/entries/' + this.src);
        request.onreadystatechange = function () {
            if (request.readystate === 4) {
                if (request.status === 200) {
                    content = request.responseText;
                } else {
                    console.log('ERROR: HTTP status code ' + request.status);
                    content = 'Error fetching Markdown source.';
                }
            }
        };
        request.send();

        while (content === null) {
            let now = new Date().getTime()/1000;
            if (now - startTime > 2) {
                content = 'Timeout while trying to fetch Markdown source.';
            }
        }

        return content;
    }

    render() {
        var content = this.fetch();
        return marked(content);
    }
}
