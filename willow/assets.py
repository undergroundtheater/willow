from flask.ext.assets import Bundle, Environment

assets_env = Environment()

common_css = Bundle(
        '../static/bower_components/selectize/dist/css/selectize.css',
        '../static/bower_components/selectize/dist/css/selectize.bootstrap3.css',
        '../static/bower_components/sweetalert/lib/sweet-alert.css',
        '../static/base_theme.css',
        '../static/locals.css',
        Bundle(
            '../static/less/*.less',
            filters='less'
            ),
        output='../public/css/common.css'
        )

assets_env.register('common_css', common_css)

common_js = Bundle(
        '../static/bower_components/jquery/dist/jquery.js',
        '../static/bower_components/bootstrap/dist/js/bootstrap.js',
        '../static/bower_components/microplugin/src/microplugin.js',
        '../static/bower_components/sifter/sifter.js',
        '../static/bower_components/selectize/dist/js/selectize.js',
        '../static/bower_components/sweetalert/lib/sweet-alert.js',
        output='../public/js/common.js'
        )

assets_env.register('common_js', common_js)
