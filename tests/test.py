import pytest
from src.main.Back import cached_checker,pnL,alert_noti
from src.fetch.scrape import currentP
from unittest.mock import patch 
#intit files is so they can be treated as packgaes.. pytest runs spearately so it does not focus on the actual cahce. it runs on different meemory
# pytest cache is diff from program cache. you need to make conftest because pytest does not stockproj is the root.
# touch to make a new file.
def test_cachedcheck():
     checker = cached_checker('AAPL')
     assert (type(checker) == int or type(checker) == float) and checker>0 
def test_pnL():
     item =['?','?','AAPL',3,300.0,'03-20-26']
     profil = (3*cached_checker('AAPL')) - (3*300.0)
     pnlcheck = pnL(item)
     assert pnlcheck[0]==profil
def test_shares(): #test functions cannot take paerameters. use pytest raises to raise an error. need to use @pytest.mark.parametersize
     item =['?','?','AAPL','3',300.0,'03-20-26']
     with pytest.raises(TypeError):
          pnL(item)
#mocking is when you create a fake version of an object. usually to test email senders like alert notti.
#patch makes a fake version of the  and inteprets it by its full path size. # the path should point to where it is used
@patch('src.main.Back.cached_checker')
@patch('src.main.Back.view_allalerts')
@patch('src.main.Back.sm.SMTP')# it is put in a stack so it is a lifo structure. like a call stack.
@patch('src.main.Back.retrieve_profile') 
def test_alerts(rp,sm,va,cc):
     fake_alerts  = [['?','?','AAPL',300.0,'activated']]
     va.return_value = fake_alerts
     rp.return_value = ['?','?','?','?','?','?','?','test123@gmail.com']
     cc.return_value = 302.0
     alert_noti()
     assert sm.called
     #mocks should never rewrite the function
#replaces the modules inside the function so that for the duration of the test it is replaces by the patchunction.



     
     



