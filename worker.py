# [START all]

import dna as adn
import webapp2


class InsertDnaHandler(webapp2.RequestHandler):
    def post(self):
        dna = self.request.get('dna')
        is_mutant = self.request.get('is_mutant') == 'True'

        # This task should run at most twenty times per second because of the datastore
        # transaction write throughput (1/s for each entity group)
        # and the amount of shards that the counters have (20 shards).
        adn.add_dna(dna, is_mutant)


app = webapp2.WSGIApplication([
    ('/insert_dna/', InsertDnaHandler)
], debug=True)
# [END all]
