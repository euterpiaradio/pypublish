# coding=utf-8
import subprocess
import datetime
import json
import sys
import time


def start_production(options):
    """
    :type options: dict
    """
    episode_number = int(options["episode.number"])
    d = {
        "metadata": {
            "title": "Euterpia Radio %03d" % episode_number,
            "artist": "Euterpia Radio",
            "album": "Euterpia Radio",
            "track": episode_number,
            "genre": "podcast",
            "year": datetime.datetime.now().year,
            "publisher": "Euterpia Radio",
            "url": "https://euterpiaradio.ch/podcast/euterpia-radio/%03d" % episode_number,
            "license": "Attribution - Pas d'Utilisation Commerciale - Pas de Modification",
            "license_url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
            "tags": "euterpia radio, podcast, français",
        },
        "output_basename": "Euterpia_Radio_%03d" % episode_number,
        "output_files": [
            {"format": "flac"},
            {"format": "mp3", "bitrate": "128"},
            {"format": "vorbis", "bitrate": "112"}
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

    username = options['auphonic.username']
    password = options['auphonic.password']
    cover_art_file = options['episode.coverart']
    filepath = options['episode.filename']

    print "Creating production..."
    cmd = "curl -s -X POST -H \"Content-Type: application/json\" https://auphonic.com/api/productions.json " \
          "-u %s:%s -d \"%s\"" % (username, password, payload.replace("\"", "\\\""))
    (out, _) = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
    response = json.loads(out)
    uuid = response['data']['uuid']
    print "Production %s created." % uuid
    print ""
    print "Uploading source file (%s) and cover art (%s) to production %s" % (filepath, cover_art_file, uuid)
    print ""
    cmd = 'curl -X POST https://auphonic.com/api/production/%s/upload.json -u %s:%s ' \
          '-F "input_file=@%s" -F "image=@%s"' % (uuid, username, password, filepath, cover_art_file)
    (out, _) = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
    print ""
    print "Files uploaded to production %s" % uuid
    print ""
    print "Starting production %s..." % uuid
    cmd = 'curl -s -X POST https://auphonic.com/api/production/%s/start.json -u %s:%s' % (uuid, username, password)
    (out, _) = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
    print "Production %s started." % uuid
    print ""

    return uuid


def wait_for_production(uuid, options):
    username = options['auphonic.username']
    password = options['auphonic.password']

    print "Waiting for production %s to complete." % uuid
    while True:
        cmd = 'curl -s -X GET https://auphonic.com/api/production/%s.json -u %s:%s' % (uuid, username, password)
        (out, _) = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
        response = json.loads(out)
        status = response['data']['status']
        if status == 3:
            print ""
            print "Production %s is ready." % uuid
            return response
        else:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(15)


def download(response, options):
    username = options['auphonic.username']
    password = options['auphonic.password']

    for output_file in response['data']['output_files']:
        filename = output_file['filename']
        download_url = output_file['download_url']
        print ""
        print "Downloading %s" % filename
        print ""
        cmd = 'curl %s -o %s -u %s:%s' % (download_url, filename, username, password)
        (out, _) = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
    print ""
