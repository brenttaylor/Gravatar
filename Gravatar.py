import urllib2, urllib, hashlib, os, datetime, time

class GravatarException(Exception):
	pass

class ImageTimeout(GravatarException):
	pass

class ImageNotFound(GravatarException):
	pass

class CacheIOError(GravatarException):
	pass

class DefaultImage:
	FileNotFound = "404"
	MysteryMan = "mm"
	IdentIcon = "identicon"
	MonsterID = "monsterid"
	Wavatar = "wavatar"
	Retro = "retro"
	Blank = "blank"
	NoDefault = None
	def CustomImage(self, URL):
		return urllib.quote_plus(URL)

class Rating:
	G = "g"
	PG = "pg"
	R = "r"
	X = "x"


def URL(User, Size=64, DefaultImage=None, Rating='g',
		ForceDefault=False, SSL=False):
	Options = {
			's':Size,
			'r':Rating,
		}
	if DefaultImage is not None:
		Options["d"] = DefaultImage
	if ForceDefault is True:
		Options["f"] = "y"
	return "%s://www.gravatar.com/avatar/%s?%s" % ("https" if SSL else "http",
			hashlib.md5(User.lower()).hexdigest(),
			urllib.urlencode(Options)
			)

def Image(User, Size=64, DefaultImage=None, Rating='g',
		ForceDefault=False, SSL=False):
	try:
		return urllib2.urlopen(URL(User, Size, DefaultImage, Rating, ForceDefault, SSL)).read()
	except urllib2.URLError:
		raise ImageTimeout
	except urllib2.HTTPError:
		raise ImageNotFound


class AvatarCache(object):
	def __init__(self, Directory, UpdateInterval=datetime.timedelta(days=7)): #UpdateInterval in Days
		self.__CacheDirectory = Directory
		self.__UpdateInterval = UpdateInterval.total_seconds()
		
		try:
			if not os.path.exists(Directory):
				os.makedirs(Directory)
		except IOError:
			raise CacheIOError

	def Image(self, User, Size=64, DefaultImage=None, Rating="g",
			ForceDefault=False, SSL=False):
		def UpdateCache(FileName):
			if (time.time() - os.path.getmtime(FileName)) > self.__UpdateInterval:
				return True
			return False

		FileName = os.path.join(self.__CacheDirectory,
				"%s.jpg" % (hashlib.md5(User.lower()).hexdigest(),))
		
		try:
			if not os.path.exists(FileName) or UpdateCache(FileName):
				AvatarImage = Image(User, Size, DefaultImage, Rating, ForceDefault, SSL)
				open(FileName, 'wb').write(AvatarImage)
				return AvatarImage
			else:
				return open(FileName, 'rb').read()
		except IOError:
			raise CacheIOError




