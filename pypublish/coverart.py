import os
import subprocess


def generate(episode_number):
    """
    :type episode_number: int
    """
    filename = 'Euterpia_Radio_%03d.cover-art.png' % episode_number
    if os.path.exists(filename):
        os.remove(filename)
    if os.path.exists(filename):
        print "Error while deleting previous cover art %s" % filename
    subprocess.Popen('convert -background "#BB1E10" -fill white -font "Poppins-Bold" -pointsize 250 '
                     '-interline-spacing -150 label:"Euterpia\nRadio\nEpisode %s" -trim -gravity center '
                     '-extent 1800x1800 %s' % (episode_number, filename), shell=True).communicate()
    if not os.path.exists(filename):
        print "Error while generating cover art"
        exit(-1)

    return filename
