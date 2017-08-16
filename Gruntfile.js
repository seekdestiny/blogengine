module.exports = function (grunt) {
    'use strict';

    grunt.initConfig({
        copy: {
            dist: {
                expand: true,
                cwd: 'blogengine/static/bower_components/font-awesome',
                src: 'fonts/*',
                dest: 'staticfiles/',
            }
        },
        concat: {
            dist: {
                src: [
                    'blogengine/static/bower_components/bootstrap/dist/css/bootstrap.css',
                    'blogengine/static/bower_components/bootstrap/dist/css/bootstrap-theme.css',
                    'blogengine/static/bower_components/font-awesome/css/font-awesome.css',
                    'blogengine/static/css/code.css',
                    'blogengine/static/css/main.css',
                    'blogengine/static/css/sidebar.css',
                    'blogengine/static/css/archive.css',
                    'blogengine/static/css/category.css',
                ],
                dest: 'blogengine/static/css/style.css'
            }
        },
        uglify: {
            dist: {
                src: [
                    'blogengine/static/bower_components/jquery/dist/jquery.js',
                    'blogengine/static/bower_components/bootstrap/dist/js/bootstrap.js',
                    'blogengine/static/js/archive.js',
                    'blogengine/static/js/sidebar.js'
                ],
                dest: 'blogengine/static/js/all.min.js'
            }
        },
        cssmin: {
            dist: {
                src: 'blogengine/static/css/style.css',
                dest: 'blogengine/static/css/style.min.css'
            }
        },
    });

    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-cssmin');

    grunt.registerTask('default', ['copy', 'concat', 'uglify', 'cssmin']);
};
