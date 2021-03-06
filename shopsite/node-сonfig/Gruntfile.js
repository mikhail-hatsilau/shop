module.exports = function(grunt) {

  grunt.initConfig({
    bower_concat: {
      main: {
        dest: '../../ui-components/scripts/plugins.js',
        cssDest: '../../ui-components/styles/plugins.css',
        mainFiles: {
          bootstrap: ['dist/css/bootstrap.css', 'dist/js/bootstrap.js']
        }
      }
    },

    jade: {
      compile: {
        options: {
          pretty: true
        },
        files: [
          {
            dest: '../../ui-components/index.html',
            src: '../../ui-components/index.jade'
          },
          {
            cwd: '../../ui-components/templates',
            dest: '../../ui-components/templates/',
            src: '*.jade',
            expand: true,
            ext: '.html'
          }
        ]
      }
    },

    coffee: {
      compile: {
        files: [
          {dest: '../../ui-components/scripts/coffeeScripts.js', src: '../../ui-components/scripts/*.coffee'}
        ]
      }
    },

    useminPrepare: {
      html: '../../ui-components/index.html',
      options: {
        dest: '../',
        flow: {
          html: {
            steps: {
              js: ['concat'],
              css: ['concat']
            }
          }
        }
      }
    },

    usemin: {
      html: '../index.html'
    },

    copy: {
      main: {
        files: [{
          src: '../../ui-components/index.html',
          dest: '../index.html'
        }, {
          cwd: 'bower_components/bootstrap/fonts',
          src: '*',
          dest: '../static/fonts/',
          expand: true
        }, {
          cwd: '../../ui-components/templates/',
          src: '*.html',
          dest: '../static/templates/',
          expand: true
        }]
      }
    }

  });

  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-bower-concat');
  grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-usemin');
  grunt.loadNpmTasks('grunt-contrib-jade');

  grunt.registerTask('build', ['bower_concat', 'coffee', 'jade', 'copy', 'useminPrepare', 'concat:generated', 'usemin']);
}
