import subprocess
import traceback
import uuid
import os
from dss import settings


def generate_waveform(input_file, output_file):
    try:
        print("Starting decode : %s\n\tIn: %s\n\tOut: %s" % \
              (settings.DSS_LAME_PATH, input_file, output_file))
        convert_command = "%s %s -c 1 -t wav - | %s -w 1170 -h 140 -o %s /dev/stdin" % \
                          (settings.DSS_LAME_PATH, input_file, settings.DSS_WAVE_PATH, output_file)
        print("Convert command: %s" % convert_command)
        result = os.system(convert_command)
        print(result)

        if os.path.exists(output_file):
            #crop the image as it looks nice with zoom
            from PIL import Image
            import glob

            im = Image.open(output_file)
            w, h = im.size
            im.crop((0, 0, w, h / 2)).save(output_file)

            return output_file
        else:
            print("Unable to find working file, did LAME succeed?")
            return ""

    except Exception as ex:
        print("Error generating waveform %s" % (ex))

