#!/usr/bin/python

"""
Access to NYTimes congress API (http://developer.nytimes.com/docs/congress_api).

Instantiating the Congress and call its instance methods:

	from nytimes.congress import Congress
	c = Congress( "<api-key>" )
	c.getMemberInfo( "L000447" )
"""

from nytimes import API_VERS
import base

class Congress( base.NYTimesBase ):
	## customize super's vars
	_URL_EXT = "/politics/%s/us/legislative/congress" % ( API_VERS, )
	_MODULE = "congress"

	def __init__( self, api_key ):
		self._API_KEY = api_key

	def getRollCallVotes( self, congress, chamber, session, roll_call ):
		rest = "%s/%s/sessions/%s/votes/%s" % ( congress, chamber, session, roll_call )
		return self.apiCall( rest )
	def getMissedVotes( self, congress, chamber ):
		rest = "%s/%s/missed_votes" % ( congress, chamber )
		return self.apiCall( rest )
	def getPartyVotes( self, congress, chamber ):
		rest = "%s/%s/party_votes" % ( congress, chamber )
		return self.apiCall( rest )
	def getNominationVotes( self, congress ):
		rest = "%s/nominations" % ( congress, )
		return self.apiCall( rest )
	def getMemberInfo( self, mem_id ):
		# TODO : get-by-name
		rest = "members/%s" % ( mem_id, )
		return self.apiCall( rest )
	def getMemberVotes( self, mem_id ):
		rest = "members/%s/votes" % ( mem_id, )
		return self.apiCall( rest )
	def getMemberRecentBills( self, mem_id ):
		rest = "members/%s/bills/introduced" % ( mem_id, )
		return self.apiCall( rest )
	def getMemberRecentCosponsoring( self, mem_id ):
		rest = "members/%s/bills/cosponsored" % ( mem_id, )
		return self.apiCall( rest )
	def getMemberFloorAppearances( self, mem_id ):
		## Trent Lott, L000447, missing (how many others?)
		rest = "members/%s/floor_appearances" % (mem_id,)
		return self.apiCall( rest )
	def getMembers( self, congress, chamber ):
		## TODO : implement state, district params
		rest = "%s/%s/members" % ( congress, chamber )
		return self.apiCall( rest )
	def getMembersNew( self ):
		rest = "members/new_members"
		return self.apiCall( rest )
	def getMembersVoteCompare( self, congress, chamber, mem_id_1, mem_id_2 ):
		rest = "members/%s/compare/%s/%s/%s" % ( mem_id_1, mem_id_2, congress, chamber )
		return self.apiCall( rest )
	def getCommittees( self, congress, chamber ):
		rest ="%s/%s/committees" % ( congress, chamber )
		return self.apiCall( rest )
	def getCommitteeMembers( self, congress, chamber, comm_id ):
		rest ="%s/%s/committees/%s" % ( congress, chamber, comm_id )
		return self.apiCall( rest )
	def getBillsRecentIntroduced( self, congress, chamber ):
		rest = "/%s/%s/bills/introduced" % ( congress, chamber )
		return self.apiCall( rest )
	def getBillsRecentUpdated( self, congress, chamber ):
		rest = "/%s/%s/bills/updated" % ( congress, chamber )
		return self.apiCall( rest )
	def getBillDetails( self, congress, bill_id ):
		rest = "%s/bills/%s" % ( congress, bill_id )
		return self.apiCall( rest )
	def getBillSubjects( self, congress, bill_id ):
		rest = "%s/bills/%s/subjects" % ( congress, bill_id )
		return self.apiCall( rest )
	def getBillAmendments( self, congress, bill_id ):
		rest = "%s/bills/%s/amendments" % ( congress, bill_id )
		return self.apiCall( rest )
	def getBillRelated( self, congress, bill_id ):
		rest = "%s/bills/%s/related" % ( congress, bill_id )
		return self.apiCall( rest )
	def getBillCosponsors( self, congress, bill_id ):
		rest = "%s/bills/%s/cosponsors" % ( congress, bill_id )
		return self.apiCall( rest )
