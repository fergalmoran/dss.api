import os

def generate_save_file_name(uid, prefix, filename):
    filename, extension = os.path.splitext(filename)
    ret = "%s%s" % ('/'.join([prefix, uid]), extension)
    return ret
