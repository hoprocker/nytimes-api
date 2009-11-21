#!/usr/bin/python

from nytimes import URLS,RESP_FORMAT,QUERY_LIMIT
import time,urllib
try: import simplejson as json
except: import json

class NYTimesBase( object ):
	## overridden in subclasses
	_URL_EXT = ""
	_MODULE = ""
	_API_KEY = "" 

	## CRUDE query rate limiter
	_LAST_CALL = -1

	def apiCall( self, tail="", params={} ):
		## TODO : can we pass an 'offset' value for any of the functions?


		## very crude query rate limiting
		interval = ( self._LAST_CALL + QUERY_LIMIT ) - time.time()
		if interval > 0:
			time.sleep( interval )

		url = "%s/%s" % ( URLS[ self._MODULE ], self._URL_EXT.strip( "/" ) )
		if len( tail ) > 0:
			url += "/%s" % ( tail.strip( "/" ), )

		params[ 'api-key' ] = self._API_KEY

		url += ".%s?%s" % ( RESP_FORMAT, urllib.urlencode( params ) )

		ret = json.load( urllib.urlopen( url ) )
		self._LAST_CALL = time.time()  ## stay on the safe side of the query limit

		return ret
