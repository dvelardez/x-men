# [START all]

from google.appengine.ext import ndb
import webapp2
import json


class Dna(ndb.Model):
    dna = ndb.JsonProperty()
    is_mutant = ndb.BooleanProperty(indexed=True)


class InsertDnaHandler(webapp2.RequestHandler):
    def post(self):
        dna = json.loads(self.request.get('dna'))
        is_mutant = bool(self.request.get('is_mutant'))

        # This task should run at most once per second because of the datastore
        # transaction write throughput.
        @ndb.transactional
        def add_dna():
            new_dna = Dna(dna=dna, is_mutant=is_mutant)
            new_dna.put()

        add_dna()


app = webapp2.WSGIApplication([
    ('/insert_dna', InsertDnaHandler)
], debug=True)
# [END all]
