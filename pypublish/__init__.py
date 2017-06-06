# coding=utf-8
import re
import glob
import dotfile
import coverart
import os
import auphonic

REGEX = "([^/]*)_([0-9]+)[_\.]raw\.flac$"


def main():
    options = dotfile.read(os.path.expanduser("~/.pypublish.yaml"))
    options.update(dotfile.read("pypublish.yaml"))
    sources = glob.glob("Euterpia_Radio_[0-9]*.raw.flac")
    for source in sources:
        process(source, options)


def process(filename, options):
    """
    :type filename: str
    :type options: dict
    """
    match = re.search(REGEX, filename)
    if match is None:
        print "Error : %s does not match regex %s" % (filename, REGEX)
        return
    episode_number = int(match.groups()[1])
    episode_cover_art = coverart.generate(episode_number)

    options['episode.coverart'] = episode_cover_art
    options['episode.number'] = episode_number
    options['episode.filename'] = filename

    if 'auphonic.skip' not in options.keys():
        uuid = auphonic.start_production(options)
        response = auphonic.wait_for_production(uuid, options)
        auphonic.download(response, options)
    else:
        print "Skipping auphonic"

    sources = glob.glob("Euterpia_Radio_%03d.*" % episode_number)
    for source in sources:
        if source != episode_cover_art and re.search(REGEX, source) is None:
            print source
