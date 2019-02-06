module.exports = function (grunt) {
    'use strict';
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        less: {
            dist: {
                options: {
                    paths: [],
                    strictMath: false,
                    sourceMap: true,
                    outputSourceFiles: true,
                    sourceMapURL: '++resource++bda.plone.shop.css.map',
                    sourceMapFilename: 'src/bda/plone/shop/browser/shop.css.map',
                    modifyVars: {
                        "isPlone": "false"
                    }
                },
                files: {
                    'src/bda/plone/shop/browser/shop.css': 'src/bda/plone/shop/browser/shop.less',
                }
            }
        },
        sed: {
            sed0: {
                path: 'src/bda/plone/shop/browser/shop.css.map',
                pattern: 'src/bda/plone/shop/browser/shop.less',
                replacement: '++resource++bda.plone.shop.less',
            }
        },
        watch: {
            scripts: {
                files: ['src/bda/plone/shop/browser/shop.less'],
                tasks: ['less', 'sed']
            }
        }
    });
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-sed');
    grunt.registerTask('default', ['watch']);
    grunt.registerTask('compile', ['less', 'sed']);
};
