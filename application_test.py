import os
import unittest
import webtest

import application
import worker

from google.appengine.ext import ndb
from google.appengine.ext import testbed as gaetestbed


class AppTest(unittest.TestCase):

    def setUp(self):
        self.test_app = webtest.TestApp(application.app)
        self.test_worker = webtest.TestApp(worker.app)
        self.testbed = gaetestbed.Testbed()
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def testDetectMutantHandler(self):
        self.testbed.init_taskqueue_stub(root_path=os.path.dirname(__file__))

        dna_mutant = {"dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]}
        dna_human = {"dna": ["TTGCCA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]}
        dna_not_human = {"dna": ["ETGCCA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]}

        response = self.test_app.post_json('/mutant/', dna_mutant)
        assert 'It is mutant.' in response.body

        with self.assertRaises(webtest.AppError) as exc:
            self.test_app.post_json('/mutant/', dna_human)
        self.assertTrue(str(exc.exception).startswith('Bad response: 403'))

        with self.assertRaises(webtest.AppError) as exc:
            self.test_app.post_json('/mutant/', dna_not_human)
        self.assertTrue(str(exc.exception).startswith('Bad response: 400'))

        tq_stub = self.testbed.get_stub(gaetestbed.TASKQUEUE_SERVICE_NAME)
        tasks = tq_stub.get_filtered_tasks()
        assert len(tasks) == 2
        assert tasks[0].name == 'task1'
        assert tasks[1].name == 'task2'

        # Run each of the tasks, checking that they succeeded.
        params = {'dna': dna_mutant, 'is_mutant': True}
        response = self.test_worker.post(tasks[0].url, params)
        assert response.status_int == 200

        params = {'dna': dna_human, 'is_mutant': False}
        response = self.test_worker.post(tasks[1].url, params)
        assert response.status_int == 200