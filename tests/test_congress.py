#!/usr/bin/python

"""
the testing framework requires a file, config.yaml, in the tests/ directory with the following data:

	api_key: "<API_KEY>"

"""

import sys,os,time,yaml,types,simplejson as json

mod_path = os.path.abspath( "%s/%s/src" % ( os.path.abspath( sys.path[0] ), os.pardir ) )
if mod_path not in sys.path:
	sys.path.insert( 1, mod_path )
from nytimes.congress import Congress

TEST_METHODS = { 
		'getRollCallVotes' : "votes_hr1866.json",
		'getMissedVotes' : "votes_missed.json",
		'getPartyVotes' : "votes_party.json",
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
TEST_JSON = {}

def pytest_funcarg__votes( request ):
	return {
			'congress' : "110",
			'chamber' : "house",
			'session' : "1",
			'roll_call' : "866",
			'json' : json.load( open( "fixtures/gen_api_test_votes.json", "r+" ) )
		}
def pytest_funcarg__control( request ):
	filename = "fixtures/%s" % ( request.param, )
	if filename not in TEST_JSON.keys():
		global TEST_JSON
		TEST_JSON[filename] = json.load( open( filename, "r+" ) )
	return TEST_JSON[filename]
def pytest_funcarg__congress( request ):
	return request.cached_setup( setup=lambda: _getCongress(), scope="session" )

def pytest_generate_tests( metafunc ):
	if metafunc.function.func_name == "test_genericApiGet":
		for meth_name in TEST_METHODS.keys():
			fc = Congress.__getattribute__( Congress, meth_name ).func_code
			meth_args = fc.co_varnames[1:fc.co_argcount]
			## crude stashing technique
			test_args = {}
			for a in meth_args:
				test_args[a] = FIXTURE_ARGS[a]
			metafunc.addcall( { 'method' : meth_name, 'args' : test_args }, param=TEST_METHODS[meth_name] )


def test_unittest():
	assert 1 == 1
def test_apiCall( votes, congress ):
	ext = "/%s/%s/sessions/%s/votes/%s" % (votes['congress'],votes['chamber'],votes['session'],votes['roll_call'] )
	res = congress.apiCall( ext )

	assert res[ 'status' ] == "OK"
	_setCheck( res['results']['votes']['vote'], votes['json']['results']['votes']['vote'] )
def test_genericApiGet( method, args, control, congress ):
	"""
	check that all of the function outputs are relatively sane.
	"""
	res = eval( 'congress.%s( %s )' % ( method, ",".join( map( lambda(x): '%s="%s"' % (x,args[x]), args.keys() ) ) ) )

	assert res['status'] == "OK"

	res_items,control_items = res['results'],control['results']
	while type( res_items ) != types.DictType:
		res_items = res_items[0]
		control_items = control_items[0]
	_setCheck( res_items, control_items )

##
## TODO : testing error cases
##


## utility
def _getCongress() :
	key = yaml.load( open( "config.yaml" , "r+" ) )[ 'api_key' ]
	return Congress( key )
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

