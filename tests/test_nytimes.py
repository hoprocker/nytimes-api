#!/usr/bin/python

"""
the testing framework requires a file, config.json, in the tests/ directory with the following data:

	{ 
		"api_keys" : {
			"congress" : "<API_KEY>",
			...
			}
	}

"congress" et al correspond to the MODULE_NAME_KEY values in each of these modules.

TODO : avoid testing of modules you don't care about
"""

import sys,os,time,types
try: import simplejson as json
except: import json

mod_path = os.path.abspath( "%s/%s/src" % ( os.path.abspath( sys.path[0] ), os.pardir ) )
if mod_path not in sys.path:
	sys.path.insert( 1, mod_path )
from nytimes.congress import Congress

TEST_JSON = {}
INSTANCES = {}


def test_unittest():
	assert 1 == 1

def pytest_generate_tests( metafunc ):
	if metafunc.function.func_name == "test_genericApiGet":
		for meth_name in metafunc.cls.TEST_METHODS.keys():
			fc = metafunc.cls.MODULE_CLASS.__getattribute__( metafunc.cls.MODULE_CLASS, meth_name ).func_code
			meth_args = fc.co_varnames[1:fc.co_argcount]
			## crude stashing technique
			test_args = {}
			for a in meth_args:
				test_args[a] = metafunc.cls.FIXTURE_ARGS[a]
			metafunc.addcall( { 'method' : meth_name, 'args' : test_args }, param=metafunc.cls.TEST_METHODS[meth_name] )
def pytest_funcarg__control( request ):
	filename = "fixtures/%s/%s" % ( request.cls.MODULE_NAME_KEY, request.param, )
	if filename not in TEST_JSON.keys():
		global TEST_JSON
		TEST_JSON[filename] = json.load( open( filename, "r+" ) )
	return TEST_JSON[filename]


class NYTimesTestBase( object ):
	## OVERRIDE THESE IN SUBCLASSES
	TEST_METHODS = { 'classMethodName' : 'output_comparison.json' }
	FIXTURE_ARGS = { 'class_function_arg' : 'value_matching_output' }
	MODULE_CLASS = None  ## ref to non-instantiated class ( e.g., Congress )
	MODULE_NAME_KEY = "congress"  ## tests/fixtures/../, and name of api_key in config.json

	def pytest_funcarg__singleton( self, request ):
		return self._getSingleton()

	def test_genericApiGet( self, method, args, control, singleton ):
		"""
		check that all of the function outputs are relatively sane. tests all NYTimes modules.
		"""
		res = eval( 'singleton.%s( %s )' % ( method, ",".join( map( lambda(x): '%s="%s"' % (x,args[x].replace( '"', '\\"' )), args.keys() ) ) ) )

		assert res['status'] == "OK"

		res_items,control_items = res['results'],control['results']
		while type( res_items ) != types.DictType:
			res_items = res_items[0]
			control_items = control_items[0]
		_setCheck( res_items, control_items )
	## utility
	def _getSingleton( self ) :
		## our own singleton generator
		if self.MODULE_CLASS not in INSTANCES.keys():
			global INSTANCES
			key = json.load( open( "config.json" , "r+" ) )[ 'api_keys' ][ self.MODULE_NAME_KEY ]
			INSTANCES[ self.MODULE_CLASS ] = self.MODULE_CLASS( key )
		return INSTANCES[ self.MODULE_CLASS ]

class TestCongress( NYTimesTestBase ):
	TEST_METHODS = { 
			'getRollCallVotes' : "votes_hr1866.json",
			'getMissedVotes' : "votes_missed.json",
			'getPartyVotes' : "votes_party.json",
			'getNominationVotes' : "nominations.json",
			'getBillsRecentIntroduced' : "bills_recent_introduced.json",
			'getBillsRecentUpdated' : "bills_recent_updated.json",
			'getMemberInfo' : "member_info.json",
			'getMemberVotes' : "member_votes.json",
			'getMemberFloorAppearances' : "member_floor_appearances.json",
			'getMemberRecentBills' : "member_recent_bills.json",
			'getMemberRecentCosponsoring' : "member_bills_cosponsored.json",
			'getCommittees' : "committees.json",
			'getCommitteeMembers' : "committee_members.json",
			'getMembers' : "members_house110.json",
			'getMembersNew' : "members_new.json",
			'getMembersVoteCompare' : "vote_compare.json",
			'getBillDetails' : "bill_details.json",
			'getBillSubjects' : "bill_subjects.json",
			'getBillRelated' : "bill_related.json",
			'getBillAmendments' : "bill_amendments.json",
			'getBillCosponsors' : "bill_cosponsors.json"
			}
	FIXTURE_ARGS = {
			'congress' : "110",
			'chamber' : "house",
			'session' : "1",
			'roll_call' : "866",
			'vote_type' : "missed_votes",
			'mem_id' : "L000447",
			'mem_id_1' : "A000022",
			'mem_id_2' : "A000014",
			'bill_id' : "hres1535",
			'comm_id' : "HSAP",
		}
	MODULE_CLASS = Congress
	MODULE_NAME_KEY = "congress"


## utility
def _setCheck( d_1, d_2 ):
	d_1_keys = frozenset( d_1.keys() )
	d_2_keys = frozenset( d_2.keys() )
	assert d_1_keys <= d_2_keys
	assert d_2_keys <= d_1_keys
	"""
	TODO : value check might be a bit agressive. investigate later.
	for k in d_1.keys():
		if type( d_1[k] ) not in [ types.TupleType, types.ListType, types.DictType ]:
			assert d_1[k] == d_2[k]
	"""



##
## TODO : testing error cases
##

