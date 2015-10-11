/** Script to update the site index.json file. */

var fs = require('fs'),
    path = require('path'),
    crypto = require('crypto');

function isMarkdown(filename) {
    if(filename.substring(filename.length - 3) !== '.md') {
        console.warn('Files without an md extension are ignored.');
        console.warn('Ignoring ' + filename);
        return false;
    }
    return true;
}

function generateRecord(contents) {
    return {
        hash: crypto.createHash('sha256')
            .update(contents)
            .digest('hex')
    };
}

function generateRecords() {
    var contents = {},
        kinds = ['entries', 'pages'];
    for(var i in kinds) {
        contents[kinds[i]] = {};

        var files = fs.readdirSync(kinds[i]);

        for(var j in files) {
            if(!isMarkdown(files[j])) {
                continue;
            }

            var data = fs.readFileSync(path.join(kinds[i], files[j]));
            contents[kinds[i]][files[j]] = generateRecord(data);
        }
    }
    return contents;
}

var contents = generateRecords();
fs.writeFileSync('index.json', JSON.stringify(contents));
