#!/usr/bin/python

from nytimes import API_KEY,URLS,RESP_FORMAT

class NYTimesBase( object ):
	## overridden in subclasses
	_URL_EXT = ""
	_MODULE = ""
	_API_KEY = "" 

	def apiCall( self, tail="", params={} ):
		## TODO : can we pass an 'offset' value for any of the functions?
		## BIGGER TODO : query rate limiting

		url = "%s/%s" % ( URLS[ self._MODULE ], self._URL_EXT.strip( "/" ) )
		if len( tail ) > 0:
			url += "/%s" % ( tail.strip( "/" ), )

		params[ 'api_key' ] = self._API_KEY

		url += ".%s?%s" % ( RESP_FORMAT, urllib.urlencode( params ) )
		res = urlopen( url )

