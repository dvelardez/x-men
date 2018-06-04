import webtest

import application
import worker


def test_all(testbed, run_tasks):
    test_app = webtest.TestApp(application.app)
    test_worker = webtest.TestApp(worker.app)

    response = test_app.get('/')
    assert '0' in response.body

    test_app.post('/mutant', {"dna":["ATGCGA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"]})
    run_tasks(test_worker)

    response = test_app.get('/')
    assert 'Is mutant.' in response.body
