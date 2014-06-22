import client_daemon
import httpretty
import unittest
import requests
import base64
import json
import sys
import os

class ClientDaemonTest(unittest.TestCase):
	def setUp(self):
		httpretty.enable()
		httpretty.register_uri(httpretty.POST,
		'http://127.0.0.1:5000/API/v1/files/bla.txt',
		data = {"response":"ok"})

	def tearDown(self):
		httpretty.disable()
		httpretty.reset()
    
	def test_upload(self, put_file = False):
		password = "passwordSegretissima"
		username = "usernameFarlocco"
		
		file_path = '/Users/marc0/progetto/prove_deamon/bla.txt'
		mock_file_content = open(file_path, 'r')

		mock_auth_user = ":".join([username, password])
		mock_data = 'asdasd'
		client_daemon.ServerCommunicator(
			'http://127.0.0.1:5000/API/v1', 
			username, 
			password,
			"/Users/marc0/progetto/prove_deamon").upload_file(file_path, put_file)
		encoded = httpretty.last_request().headers['authorization'].split()[1]
		authorization_decoded = base64.decodestring(encoded)
		#data = httpretty.last_request().parsed_body
		path = httpretty.last_request().path
		host = httpretty.last_request().headers['host']
		method = httpretty.last_request().method
		
		#check if authorization is equals
		self.assertEqual(authorization_decoded, mock_auth_user)
		#check if data is equals
		#self.assertEqual(data, mock_data) 
		#check if url and method is equals

		self.assertEqual(path, '/API/v1/files/bla.txt')
		self.assertEqual(host,'127.0.0.1:5000')
		if put_file:
			self.assertEqual(method, 'PUT')
		else:
			self.assertEqual(method, 'POST')

	def test_download(self):
		   pass

	def test_upload_put(self):
		pass
		#self.test_upload(put_file = True)

	def test_synchronize(self):
		status_code = 200

		def fakewrite_a_file(*args):
			return 'Writing a file'

		def fakedelete_a_file(*args):
			return 'Deleting a file'

		def fakemove_a_file(*args):
			return 'Moving a file'

		def fakecopy_a_file(*args):
			return 'Coping a file'

		if status_code != 204:
			diffs = json.load(open('test_mock/sync.json', 'r'))
			for tstamp, obj in diffs.iteritems():
				self.timestamp = tstamp #update self timestamp
				print 'Timestamp op: ', tstamp
				req = obj[0]
				print 'Request: ', req
				args = obj[1]
				print 'Arguments: ', args
				{
					'req_get': fakewrite_a_file,
					'req_delete': fakedelete_a_file,
					'req_move': fakemove_a_file,
					'req_copy': fakecopy_a_file
				}.get(req)(args) 

	def test_delete(self):
		pass

	def test_on_moved(self):
		pass

	def test_on_created(self):
		pass

	def test_on_deleted(self):
		pass

	def test_on_modified(self):
		pass

	def diff_snapshot_paths(self):
		snapshot_manager = self.init_snapshot()
		#mock_equal = """[u'/Users/marc0/progetto/prove_deamon/asdas/asdasd.txt', u'/Users/marc0/progetto/prove_deamon/asdas/Nuovo documento di testo.txt', u'/Users/marc0/progetto/prove_deamon/dsa.txt', u'/Users/marc0/progetto/prove_deamon/Nuovo documento di testo (4).txt', u'/Users/marc0/progetto/prove_deamon/Nuovo documentodi testo (3).txt', u'/Users/marc0/progetto/prove_deamon/bla.txt', u'/Users/marc0/progetto/prove_deamon/asdas/sdadsda.txt', u'/Users/marc0/progetto/prove_deamon/Nuovo documento di testo (5).txt', u'/Users/marc0/progetto/prove_deamon/Nuovo documento di testo.txt', u'/Users/marc0/progetto/prove_deamon/Nuovo documento di testo (2).txt']"""
		#mock_new_client = """[u'/Users/marc0/progetto/prove_deamon/asdas/bla.txt', u'/Users/marc0/progetto/prove_deamon/asd/gbla.txt', u'/Users/marc0/progetto/prove_deamon/asdas/gbla.txt']"""
		#mock_new_server= """['path_farlocca']"""

		snap_client = snapshot_manager.local_full_snapshot
		snap_server = {'9406539a103956dc36cb7ad35547198c': [u'/Users/marc0/progetto/prove_deamon\\bla.txt'], 'a8f5f167f44f4964e6c998dee827110c': [u'/Users/marc0/progetto/prove_deamon\\asd\\gbla.txt', u'/Users/marc0/progetto/prove_deamon\\asdas\\bla.txt', u'/Users/marc0/progetto/prove_deamon\\asdas\\gbla.txt'], 'c21e1af364fa17cc80e0bbec2dd2ce5c': [u'/Users/marc0/progetto/prove_deamon\\asdas\\asdasd.txt'], 'd41d8cd98f00b204e9800998ecf8427e': [u'/Users/marc0/progetto/prove_deamon\\dsa.txt', u'/Users/marc0/progetto/prove_deamon\\Nuovo documento di testo (2).txt', u'/Users/marc0/progetto/prove_deamon\\Nuovo documento di testo (3).txt', u'/Users/marc0/progetto/prove_deamon\\Nuovo documento di testo (4).txt', u'/Users/marc0/progetto/prove_deamon\\Nuovo documento di testo (5).txt', u'/Users/marc0/progetto/prove_deamon\\Nuovo documento di testo.txt', u'/Users/marc0/progetto/prove_deamon\\asdas\\Nuovo documento di testo.txt', u'/Users/marc0/progetto/prove_deamon\\asdas\\sdadsda.txt', 
		u'path_farlocca']}
		new_client, new_server, equal = snapshot_manager.diff_snapshot_paths(snap_client, snap_server)
		
		#new_client = str(new_client).replace('\\\\','/')
		#new_server = str(new_server).replace('\\\\','/')
		#equal = str(equal).replace('\\\\','/')

		#self.assertEqual(str(new_client), mock_new_client)
		#self.assertEqual(str(equal), mock_equal)
		#self.assertEqual(str(new_server), mock_new_server)

if __name__ == '__main__':
	unittest.main()

