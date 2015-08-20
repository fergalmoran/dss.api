def download_file( url, file_name):
    import urllib.request, urllib.error, urllib.parse

    u = urllib.request.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print("Downloading: %s Bytes: %s" % (file_name, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        file_buffer = u.read(block_sz)
        if not file_buffer:
            break

        file_size_dl += len(file_buffer)
        f.write(file_buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status += chr(8) * (len(status) + 1)
        print(status, end=' ')

    f.close()
