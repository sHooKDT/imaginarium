module.exports = function(grunt) {
    // Project configuration.
    grunt.initConfig({
        clean: {
            client: {
                options: {
                    force: true
                },
                src: ['client']
            }
        },
        sass: {
            styles: {
                options: {
                    style: 'compressed',
                    noCache: true,
                    sourcemap: 'none'
                },
                files: {
                    'client/styles/main.css': 'src/styles/main.scss',
                    'client/styles/lobby.css': 'src/styles/lobby.scss',
                    'client/styles/turn.css': 'src/styles/turn.scss',
                    'client/styles/table.css': 'src/styles/table.scss'
                }
            }
        },
        htmlmin: {
            index: {
                options: {
                    removeComments: true,
                    collapseWhitespace: true,
                    minifyJS: true,
                    minifyCSS: true
                },
                files: {
                    'client/index.html': 'src/index.html'
                }
            }
        },
        copy: {
            jsext: {
                files: [{
                    expand: true,
                    cwd: 'src/js/external/',
                    src: ['**'],
                    dest: 'client/js/external/'
                }]
            },
            font: {
                files: [{
                    expand: true,
                    cwd: 'src/res/font/',
                    src: ['**'],
                    dest: 'client/res/font/'
                }]
            },
            img: {
                files: [{
                    expand: true,
                    cwd: 'src/res/',
                    src: ['logo.svg', 'favicon.ico'],
                    dest: 'client/res/'
                }]
            }
        },
        uglify: {
            options: {
                mangle: false
            },
            js: {
                files: {
                    'client/js/main.js': ['src/js/main.js', 'src/js/socket.js']
                }
            }
        },
        imagemin: {
            cards: {
                options: {
                    optimizationLevel: 7
                },
                files: [{
                    expand: true,
                    cwd: 'src/res/cards',
                    src: ['*.jpg'],
                    dest: 'client/res/cards'
                }]
            }
        }
    });
    // Load plugins
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-htmlmin');
    grunt.loadNpmTasks('grunt-contrib-imagemin');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-clean');
    // Tasks
    grunt.registerTask('default', ['sass']);
    grunt.registerTask('build', ['clean', 'sass', 'htmlmin', 'uglify', 'imagemin', 'copy']);
};