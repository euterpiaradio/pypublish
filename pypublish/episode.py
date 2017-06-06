# coding=utf-8
import os
import re
from options import get_option, set_option

REGEX = "(.*/)?([^/]*)_([0-9]+)[_\.]raw\.flac$"


def find_source():
    here = os.path.abspath(os.path.dirname("."))
    if get_option('episode.source') is None:
        print "Looking for source file"
        sourcefiles = [f for f in os.listdir(here) if os.path.isfile(os.path.join(here, f)) and re.search(REGEX, f)]
        if len(sourcefiles) == 0:
            print "Source file not found : it should be Podcast_Name_xxx_raw.flac"
            exit(1)
        if len(sourcefiles) > 1:
            print "Too many source files : %s" % sourcefiles
            exit(1)
        set_option('episode.filename', sourcefiles[0])
        set_option('episode.source', os.path.join(here, get_option('episode.filename')))
        print "Found source file : %s" % get_option('episode.source')
    else:
        filepath = get_option('episode.source')
        print "Using source file %s" % filepath
        dirname = os.path.dirname(filepath)
        set_option('episode.filename', filepath[len(dirname):])

    return None


def update_metadata():
    """
    :param options: Options
    :type options: dict
    """
    here = os.path.abspath(os.path.dirname("."))
    match = re.search(REGEX, get_option('episode.source'))

    if match.group(1) is not None:
        here = match.group(1)
    _filename = match.group(2)
    _podcast = _filename.replace("_", " ")
    _number = match.group(3)
    _basename = "%s_%s" % (match.group(2), _number)

    if get_option('episode.podcast') is None:
        set_option('episode.podcast', _podcast)

    if options['episode.number'] is None:
        options['episode.number'] = _number

    if options['episode.title'] is None:
        options['episode.title'] = "%s %s" % (options['episode.podcast'], options['episode.number'])

    if options['episode.cover_art_file'] is None:
        options['episode.cover_art_file'] = os.path.join(here, "%s.cover.png" % _basename)

    if options['episode.artist'] is None:
        options['episode.artist'] = _podcast

    if options['episode.album'] is None:
        options['episode.album'] = _podcast

    track = number
