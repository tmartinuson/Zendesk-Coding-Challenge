import mock
from mock.mock import MagicMock
import main
import gui
import pytest
import sys

"""
Testing functional logic within the program 
because testing tkinter with mock and pytest 
proved to be quite challenging with unittests
"""

@mock.patch( 'tkinter.messagebox' )
@mock.patch( 'gui.GUI' )
@mock.patch( 'requests.get' )
def testTryLoginAndJson( mock_requests, mock_gui, mock_messagebox ):
    mock_messagebox.return_value.showerror = print("Nothing")
    mock_requests.return_value.ok = False
    mock_requests.return_value.reason = "Unauthorized"
    window = MagicMock()
    mock_gui.return_value = False
    main.tryLoginAndJson( 'user', 'pass',  window )
    mock_gui.assert_not_called
    mock_requests.return_value.reason = "Not Found"
    main.tryLoginAndJson( 'user', 'pass',  window )
    mock_gui.assert_not_called
    mock_requests.return_value.ok = True
    mock_gui.assert_called
    

@mock.patch( 'gui.requests.get' )
def testGrabJson( mock_request ):
    mock_request.return_value.json.return_value = { 'test':'clear' }
    jsonTest = gui.grabJson( 1, ( "user", "pass" ))
    assert mock_request.called
    assert jsonTest == { 'test':'clear' }

@mock.patch( 'gui.GUI.run' )
def testBuildTicket( mock_run ):
    g = gui.GUI( "Test", "Data" )
    fakeTicket = { "subject":"Testing", "id":1, "requester_id":123, "created_at":"2021-11-26T00:40:28Z"}
    resp = g.buildTicket(fakeTicket)
    assert resp == "1 Testing Opened by: 123 on 2021-11-26"

if __name__ == '__main__':
    sys.exit( pytest.main( sys.argv ) )