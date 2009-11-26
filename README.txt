=====
Intro

nytimes-api is a test-supported, lightweight Python wrapper for the NYTimes developer APIs. The main API is divided into several sections (Community, Real Estate, et al.). Currently implemented are the following APIs:

	nytimes.congress

This library requires the 'simplejson' library. With Python 2.6, this is included under the name 'json'. For versions of Python prior to 2.6, simplejson can be installed via:
	
	> sudo easy_install simplejson


<< This library is still under development, and some aspects are likely to change. >>


=====
Usage

To install the library, copy the src/nytimes/ directory to your Python packages directory, usually /usr/share/python/{version}/site-packages .

	On Linux:
	> sudo cp src/nytimes /usr/local/python/{version}/site-packages/

	On OS X:
	> sudo cp src/nytimes  /Library/Python/{version}/site-packages/
		(or, locally)
	> cp src/nytimes ~/Library/Python/{version}/site-packages/

The current form of the library basically exposes the endpoints available via the NYTimes API. To use the library, create an instance of the class you wish to use, passing your API key as an argument:

	from nytimes.congress import Congress

	cong = Congress( "yourapikeywill:be:here" )

Then call it like so:

	cong.getMemberInfo( 'L000447' )


=====
Tests

This wrapper employs a generally TDD-ish methodology. Tests are located in the tests/ directory, with fixtures in tests/fixtures/. The testing framework is based on py.test (http://codespeak.net/py/dist/test/), and in Python < 2.5, uses simplejson library. To run the tests, first download py.test:

	> sudo easy_install py.test
	> sudo easy_install simplejson

Create a file in the tests/ directory called config.json with the following format:

	{ "api_keys" : {
		"congress" : "yourapikey:here",
		...
		} }

Execute 'py.test' from the tests/ directory to run the tests.



For more information about the NYT APIs, visit http://developer.nytimes.com/
Feedback is welcome; email me at nytimes-python@hoprocker.net.
This code is free for any use, license TBD.

malcolm mcfarland 21 nov 2009
