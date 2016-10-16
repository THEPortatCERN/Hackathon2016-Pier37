'use strict';

var path = {
    theme:  '/',
    sass:   'sass',
    css:    'stylesheets',
    js:     'javascripts',
    img:    'images',
    tpl:    'templates',
    fonts:  'fonts'
};

/* Set paths */
path.sass   = path.theme + path.sass;
path.css    = path.theme + path.css;
path.js     = path.theme + path.js;
path.img    = path.theme + path.img;
path.tpl    = path.theme + path.tpl;
path.fonts  = path.theme + path.fonts;

var gulp          = require('gulp'),
    util          = require('gulp-util'),
    sass          = require('gulp-sass'),
    globbing      = require('gulp-css-globbing'),
    postcss       = require('gulp-postcss'),
    autoprefixer  = require('autoprefixer'),
    mqpacker      = require('css-mqpacker'),
    csswring      = require('csswring'),
    webserver     = require('gulp-webserver');

gulp.task('webserver', function() {
  gulp.src('.')
    .pipe(webserver({
      livereload: true,
      directoryListing: true,
      open: true
    }));
});

gulp.task('sass', function () {
  var processors = [
        autoprefixer({browsers: ['last 10 versions', 'ie 10']})
      ],
      processors_prod = [
        autoprefixer({browsers: ['last 10 versions', 'ie 10']}),
        csswring
      ],
      processors = dev ? processors : processors_prod;

  gulp.src(path.sass + '/**/*.scss')
    .pipe(sourcemaps.init())
    .pipe(globbing({ extensions: ['.scss'] }))
    .pipe(sass.sync().on('error', sass.logError).on('error', process.exit.bind(process, 1)))
    .pipe(postcss(processors))
    .pipe(sourcemaps.write('./map'))
    .pipe(gulp.dest('./' + path.css));
});

/*SVG Minify*/
gulp.task('svg', function() {
  return gulp.src(path.img + '/**/*.svg')
  .pipe(imagemin({
      progressive: true,
      interlaced: true,
      multipass: true,
      svgoPlugins: [{removeViewBox: false}]
  }))
  .pipe(imageminSvgo()())
  .pipe(gulp.dest(path.img + '/'))
  .pipe(duration('minified SVGs'));
});

/* Gulp jshint taskc*/
gulp.task('jshint', function() {
  return gulp.src(path.js + '/**/*.js')
    .pipe(jshint())
    .pipe(jshint.reporter('jshint-stylish'));
});

gulp.task('default', ['webserver']);
gulp.task('compile', ['sass']);
