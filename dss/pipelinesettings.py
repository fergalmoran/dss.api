PIPELINE_CSS = {
    'css': {
        'source_filenames': (
            'css/*.css',
        ),
        'variant': 'datauri',
        'output_filename': 'css/c.css'
    },
    'embedding': {
        'source_filenames': (
            'css/embedding/*.css',
        ),
        'variant': 'datauri',
        'output_filename': 'css/e.css'
    }
}

PIPELINE_JS = {
    'embedding': {
        'source_filenames': (
            'js/embedding/jquery.js',
            'js/embedding/jplayer.js',
            'js/embedding/jplayer.cleanskin.js',
        ),
        'output_filename': 'js/e.js',
    },
}
