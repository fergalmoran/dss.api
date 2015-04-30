iPIPELINE_TEMPLATE_FUNC = "_.template"

PIPELINE_COMPILERS = (
    'pipeline.compilers.coffee.CoffeeScriptCompiler',
)

PIPELINE_CSS = {
    'css': {
        'source_filenames': (
            'css/dss.overrides.css',

            'css/ace/dropzone.css',
            'css/ace/uncompressed/jquery.gritter.css',
            'css/ace/uncompressed/bootstrap.css',
            'css/ace/uncompressed/ace.css',
            'css/ace/uncompressed/ace-ie.css',
            'css/ace/uncompressed/ace-skins.css',
            'css/ace/uncompressed/font-awesome.css',
            'css/ace/uncompressed/fullcalendar.css',
            'css/ace/uncompressed/bootstrap-editable.css',

            'css/jasny-bootstrap.css',
            'css/select2.css',
            'css/jquery.fileupload-ui.css',
            'css/peneloplay.css',
            'css/toastr.css',
            'css/dss.main.css',
        ),
        'output_filename': 'css/site.css'
    }
}

PIPELINE_JS = {
    'templates': {
        'source_filenames': (
            'js/dss/templates/*.jst',
        ),
        'variant': 'datauri',
        'output_filename': 'js/t.js',
    },

    'lib': {
        'source_filenames': (
            'js/lib/jquery.js',
            'js/lib/jquery-ui.js',

            'js/lib/moment.js',
            'js/lib/typeahead.js',

            'js/lib/sm/soundmanager2.js',

            'js/lib/underscore.js',
            'js/lib/underscore.templatehelpers.js',
            'js/lib/backbone.js',
            'js/lib/backbone.syphon.js',
            'js/lib/backbone.associations.js',
            'js/lib/backbone.marionette.js',

            'js/lib/ace/uncompressed/bootstrap.js',
            'js/lib/ace/uncompressed/ace.js',
            'js/lib/ace/uncompressed/ace-elements.js',
            'js/lib/ace/uncompressed/select2.js',
            'js/lib/ace/uncompressed/fuelux/fuelux.wizard.js',
            'js/lib/ace/ace/elements.wizard.js',
            'js/lib/ace/uncompressed/bootstrap-wysiwyg.js',
            'js/lib/ace/uncompressed/jquery.gritter.js',
            'js/lib/ace/uncompressed/dropzone.js',
            'js/lib/ace/uncompressed/fullcalendar.js',
            'js/lib/ace/uncompressed/x-editable/bootstrap-editable.js',
            'js/lib/ace/uncompressed/x-editable/ace-editable.js',

            'js/lib/ajaxfileupload.js',
            'js/lib/jasny.fileinput.js',
            'js/lib/jquery.fileupload.js',
            'js/lib/jquery.fileupload-process.js',
            'js/lib/jquery.fileupload-audio.js',
            'js/lib/jquery.fileupload-video.js',
            'js/lib/jquery.fileupload-validate.js',
            'js/lib/jquery.fileupload-ui.js',
            'js/lib/jquery.fileupload-image.js',
            'js/lib/jquery.iframe-transport.js',
            'js/lib/jquery.ui.widget.js',
            'js/lib/toastr.js',

            'js/dss/*.coffee',
            'js/dss/**/*.coffee',
            'js/dss/apps/**/**/*.coffee',
        ),
        'output_filename': 'js/a.js',
    },
}
