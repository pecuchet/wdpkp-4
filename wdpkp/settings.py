"""
Main program settings
"""
import os
import datetime

# DEV
#
DEBUG = 0
DEBUG_BASE_URL = 'http://whydopeoplekeepphotographs.net/v3_test_data/'

# INPUT
#
PHRASE = "Why do people keep photographs Why Goodness knows Why do people keep things junk trash bits and pieces They do that's all there is to it Up to a point I agree with you Some people keep things some people throw everything away as soon as they have done with it That yes it is a matter of temperament But I speak now especially of photographs Why do people keep in particular photographs"
PHRASE_PUNC = "Why do people keep photographs? Why? Goodness knows! Why do people keep things \u2014junk\u2014 trash, bits and pieces. They do \u2014that\u2019s all there is to it! Up to a point I agree with you. Some people keep things. Some people throw everything away as soon as they have done with it. That, yes, it is a matter of temperament. But I speak now especially of photographs. Why do people keep, in particular, photographs?"

# REQUEST
#
NUM_RESULTS = 40
ALLOW_RELAUNCH = 1
RELAUNCH_TIMES = 5
URL_BLACKLIST_1 = '(keepcalm-o-matic)|(i\.klip\.in)|(2\.bp\.blogspot\.com)|(1\.bp\.blogspot\.com)|(pafpc\.org)|(arghink\.com)|(animephproject\.files\.word)|(unityteens\.files\.wordpress)|(images4\.fanpop)|(poterieplurielsingulier)|(bogotobogo\.com)|(images-cdn\.moviepilot)|(i\.onionstatic)|(growingweisser\.com)|(zerohedge\.com)|(wac\.b63f\.edgecastcdn)|(orig06\.deviantart\.net)'
URL_BLACKLIST_2 = '|(ourjourneywithgod\.files\.wordpress)|(heartbeatinternational\.org)|(webneel\.com)|(catziac\.files\.wordpress)|(thechive\.files\.wordpress)|(images\.fineartamerica)|(awschrick\.files\.wordpress)|(womenshealthmag\.com)|(gronemberger\.com)|(4\.bp\.blogspot\.com)|(ichef\.bbci\.co\.uk)|(workthedream\.files\.wordpress)|(katerinamichouli\.files\.wordpress)|(rickeyorg-rickeyllc\.netdna-ssl)|(colourbox\.com)|(poker52\.fr)'
URL_BLACKLIST_3 = '|(lastoneminute\.com)|(i165\.photobucket\.com)|(media\.npr\.org)|(hdwallpapers2013\.com)|(roshnii179\.files\.wordpress\.com)|(pageone\.ng)|(3\.bp\.blogspot\.com)|(successyeti\.com)|(sarassecret\.com)|(pd4pic\.com)|(carriemunderwood\.com)|(hdwallpapers\.in)|(static\.srcdn\.com)|(comealivein365\.com)|(3upg5n1ajpdonqkkp34tcif1-wpengine\.netdna-ssl\.com)|(2static\.fjcdn\.com)|(dvanime\.narod\.ru)'
URL_BLACKLIST_4 = '|(gamba\.fm)|(adamackbeats\.com)|(contentbuket\.com)|(impawards\.com)|(img\.picturequotes\.com)|(nsullivandesign\.com)|(withersthomas\.co\.uk)|(thehilljean\.com)|(vegankicks\.com)|(lolsnaps\.com)|(image\.slidesharecdn\.com)|(kateswaffer\.files\.wordpress)'
URL_BLACKLIST_5 = '|(68\.media\.tumblr\.com)|(jpteenpics\.com)'
URL_BLACKLIST = URL_BLACKLIST_1 + URL_BLACKLIST_2 + URL_BLACKLIST_3 + URL_BLACKLIST_4 + URL_BLACKLIST_5

# VARIABLES
#
TODAY = datetime.datetime.now().isoformat().split('T')[0]
DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DIR_DATA = DIR + '/data_tmp/'
DIR_DATA_DATE = DIR_DATA + TODAY + '/'
DIR_VIDEO_DATE = DIR + '/videos/' + TODAY + '/'

# EDITING
#
FFMPEG = '/usr/local/bin/ffmpeg'
WIDTH = 1920
HEIGHT = 1080
TIME_CODES = DIR + '/assets/161024_wdpkp-timecodes.txt'
THREAD_QUEUE_SIZE = str(32)
BLACK_FRAME = DIR + '/assets/images/black.png'

# POST-PRODUCTION
#
TITLE = 'Why do people keep photographs?'
FONT_DIR = DIR + '/assets/fonts'
FONT = FONT_DIR + '/HelveticaNeue.ttf'
FONT_BOLD = FONT_DIR + '/HelveticaNeueBold.ttf'
FONT_SIZE = 40
