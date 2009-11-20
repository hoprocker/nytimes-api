#!/usr/bin/python

import py,sys,os,simplejson as json
mod_path = os.path.abspath( "%s/%s/src" % ( os.path.abspath( sys.path[0] ), os.pardir ) )
if mod_path not in sys.path:
	sys.path.insert( 1, mod_path )

print "sys.path == " + str( sys.path )

from nytimes.congress import Congress

def pytest_funcarg__votes_866( request ):
	f = json.load( open( "fixtures/votes_866.json", "r+" ) )
	return f
	
def test_unittest():
	assert 1 == 1

## test base API functionality
def test_apiCall( votes_866 ):
	congress = "110"
	chamber = "house"
	session = "1"
	roll_call = "866"

	ext = "/%s/%s/sessions/%s/votes/%s" % ( congress, chamber, session, roll_call )

	cong = Congress()
	res = cong.getRollCallVote( congress, chamber, session, roll_call )

	assert res[ 'status' ] == "OK"
	assert len( res["results"]["votes"] ) > 0

def test_getRollCallVotes():
	pass
