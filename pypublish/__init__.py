# coding=utf-8
from os import listdir, path
from os.path import isfile, join
from datetime import datetime
from getopt import getopt

import time
import re
import subprocess
import json
import sys

REGEX = "(.*/)?([^/]*)_([0-9]+)[_\.]raw\.flac$"


def main():
    # Initialize variables
    uuid = None
    preserve = False
    source = None
    item = None
    folder = None
    access_key = None
    secret_key = None

    # Parse command line arguments
    args = ["uuid=", "preserve", "source=", "item=", "folder=", "access-key=", "secret-key="]
    legacy_args = ["no-confirm", "config=", "no-wait", "episode-input-file=", "episode-number=",
                   "episode-title=", "episode-cover-art-file=", "auphonic-output-file-basename=",
                   "auphonic-year=", "auphonic-preset=", "auphonic-username=", "auphonic-password=",
                   "internetarchive-item=", "internetarchive-folder=", "internetarchive-access-key=",
                   "internetarchive-secret-key="]
    args.extend(legacy_args)
    opts, _ = getopt(sys.argv[1:], "", args)
    for opt, arg in opts:
        if opt == "--uuid":
            uuid = arg
        if opt == "--preserve":
            preserve = True
        if opt in ["--source", "--episode-input-file"]:
            source = arg
        if opt in ["--item", "--internetarchive-item"]:
            item = arg
        if opt in ["--folder", "--internetarchive-folder"]:
            folder = arg
        if opt in ["--access-key", "--internetarchive-access-key"]:
            access_key = arg
        if opt in ["--secret-key", "--internetarchive-secret-key"]:
            secret_key = arg

    good_to_go = True
    if item is None:
        print "Archive.org's item not specified"
        good_to_go = False
    if folder is None:
        print "Archive.org's folder not specified"
        good_to_go = False
    if access_key is None:
        print "Archive.org's access key not specified"
        good_to_go = False
    if secret_key is None:
        print "Archive.org's secret key not specified"
        good_to_go = False

    if not good_to_go:
        return

    print "PyPublish started"
    here = path.abspath(path.dirname("."))
    if source is None:
        print "Looking for source file"
        sourcefiles = [f for f in listdir(here) if isfile(join(here, f)) and re.search(REGEX, f)]
        if len(sourcefiles) == 0:
            print "Source file not found : it should be Podcast_Name_xxx_raw.flac"
            exit(1)
        if len(sourcefiles) > 1:
            print "Too many source files : %s" % sourcefiles
            exit(2)
        filename = sourcefiles[0]
        filepath = join(here, filename)
    else:
        filepath = source

    match = re.search(REGEX, filepath)

    if match.group(1) is not None:
        here = match.group(1)
    prefix = match.group(2)
    suffix = match.group(3)
    podcast = prefix.replace("_", " ")
    number = int(suffix)

    print here
    print podcast
    print number

    cover_art_file = join(here, "%s_%s.cover.png" % (prefix, suffix))

    print cover_art_file

    return

    now = datetime.now()

    # Auphonic data
    username = "frenchguy"
    password = "Kxtj3YOxNGQs"
    title = "%s %s" % (podcast, suffix)
    artist = podcast
    album = podcast
    track = number
    genre = "Podcast"
    year = now.year
    publisher = podcast
    url = "https://euterpiaradio.ch"
    license = "Attribution - Pas d'Utilisation Commerciale - Pas de Modification"
    license_url = "https://creativecommons.org/licenses/by-nc-nd/4.0/"
    tags = "euterpia radio, podcast, français"
    output_basename = "%s_%s" % (prefix, suffix)

    print "Source file : %s" % filepath
    print "Podcast title : %s" % podcast
    print "Episode number : %s" % number

    if uuid is None:
        print "Generating cover art"
        (out, _) = subprocess.Popen('rm -vf %s' % cover_art_file,
                                    shell=True, stdout=subprocess.PIPE).communicate()

        cmd = 'convert -verbose -background "#BB1E10" -fill white -font "Poppins-Bold" -pointsize 250 ' \
              '-interline-spacing -150 label:"Euterpia\\nRadio\\nEpisode %s" -trim -gravity center ' \
              '-extent 1800x1800 %s' % (number, cover_art_file)
        (out, _) = subprocess.Popen(cmd, shell=True).communicate()
        print "Done"

        d = {
            "metadata": {
                "title": title,
                "artist": artist,
                "album": album,
                "track": track,
                "genre": genre,
                "year": year,
                "publisher": publisher,
                "url": url,
                "license": license,
                "license_url": license_url,
                "tags": tags,
            },
            "output_basename": output_basename,
            "output_files": [
                {"format": "flac"},
                {"format": "mp3", "bitrate": "128"},
                {"format": "vorbis", "bitrate": "112"},
                {"format": "waveform"},
            ],
            "algorithms": {
                "hipfilter": True,
                "leveler": True,
                "normloudness": True,
                "denoise": True,
                "loudnesstarget": -16,
                "denoiseamount": 0,
            },
        }

        payload = json.dumps(d, ensure_ascii=False)

        print "Creating new production"
        cmd = "curl -X POST -H \"Content-Type: application/json\" https://auphonic.com/api/productions.json " \
              "-u %s:%s -d \"%s\"" % (username, password, payload.replace("\"", "\\\""))
        (out, _) = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
#        print "======================================================================================================="
#        print out
#        print "======================================================================================================="
        response = json.loads(out)
        uuid = response['data']['uuid']
        print "Production %s created" % uuid

        print "Uploading source file (%s) and cover art (%s) to production %s" % (filepath, cover_art_file, uuid)
        cmd = 'curl -X POST https://auphonic.com/api/production/%s/upload.json -u %s:%s ' \
              '-F "input_file=@%s" -F "image=@%s"' % (uuid, username, password, filepath, cover_art_file)
        (out, _) = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
#        print "======================================================================================================="
#        print out
#        print "======================================================================================================="
        print "Files uploaded to production %s" % uuid

        print "Starting production %s" % uuid
        cmd = 'curl -X POST https://auphonic.com/api/production/%s/start.json -u %s:%s' % (uuid, username, password)
        (out, _) = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
#        print "======================================================================================================="
#        print out
#        print "======================================================================================================="
        print "Production %s started" % uuid

    print "Waiting for production %s to be ready" % uuid
    ready = False
    response = None
    while not ready:
        cmd = 'curl https://auphonic.com/api/production/%s.json -u %s:%s' % (uuid, username, password)
        (out, _) = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
#        print "======================================================================================================="
#        print out
#        print "======================================================================================================="
        response = json.loads(out)
        status = response['data']['status']
        if status == 3:
            print "Production %s is ready" % uuid
            ready = True
        else:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(15)
    print "Downloading output files"
    for output_file in response['data']['output_files']:
        filename = output_file['filename']
        download_url = output_file['download_url']
        if not preserve or not path.isfile(join(here, filename)):
            print "Downloading %s" % filename
            cmd = 'curl %s -o %s -u %s:%s' % (download_url, filename, username, password)
            (out, _) = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
        else:
            print "Preserving existing file %s" % filename
