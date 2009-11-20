#!/usr/bin/python

"""
access to ny-times congress api:
http://developer.nytimes.com/
"""

from nytimes import API_VERS
import base

class Congress( base.NYTimesBase ):
	## customize super's vars
	_URL_EXT = "/politics/%s/us/legislative/congress" % ( API_VERS, )
	_MODULE = "congress"

	## three fundamental units
	_CONGRESS = {}
	_MEMBER = {}
	_BILL = {}
	_SUBJECTS = {}

	def __init__( self, api_key ):
		self._API_KEY = api_key

	## interface
	def getRollCallVotes( self, congress, chamber, session, roll_call ):
		pass
	def getMissedVotes( self, congress, chamber, vote_type="missed_votes" ):
		pass
	def getNominationVotes( self, congress ):
		chamber="senate"
	def getMemberInfo( self, mem_id="", member_name="" ):
		pass
	def getMemberRecentVotes( self, mem_id ):
		pass
	def getMemberRecentBills( self, mem_id, type="introduced" ):
		pass
	def getMemberRecentCosponsoring( self, mem_id ):
		pass
	def getMemberFloorAppearances( self, mem_id ):
		pass
	def getMembers( self, congress, chamber ):
		pass
	def getMembersNew( self ):
		pass
	def getMembersVoteCompare( self, mem_id_1, mem_id_2 ):
		pass
	def getCommittee( self, congress, chamber ):
		pass
	def getBillsRecent( self, congress, chamber, type="introduced" ):
		## type == introduced | updated
		pass
	def getBillInfo( self, congress, bill_id, resource="subjects" ):
		## resource == subjects | amendments | related
		pass
	def getBillCosponsors( self, congress, bill_id ):
		pass




	## general utility
	def _genSessKey( self, congress, chamber ):
		pass

