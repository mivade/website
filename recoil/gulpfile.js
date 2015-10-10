/** Build script for Recoil. */

var gulp = require('gulp');
var babelify = require('babelify');
var source = require('vinyl-source-stream');
var browserify = require('browserify');

var paths = {
    html: 'src/index.html',
    css: 'src/css/*.css',
    out: 'bundle.js',
    dest: 'dist',
    entry: './src/js/index.js'
};

gulp.task('copy', function () {
    gulp.src(paths.html)
        .pipe(gulp.dest(paths.dest));
    gulp.src(paths.css)
        .pipe(gulp.dest(paths.dest + '/css'));
});

gulp.task('build', function () {
    var b = browserify({
        entries: [paths.entry],
        debug: true
    });
    b.transform(babelify.configure({stage: 0}))
        .bundle()
        .pipe(source('bundle.js'))
        .pipe(gulp.dest(paths.dest + '/js'));
});

gulp.task('default', ['build', 'copy']);
