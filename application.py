from google.appengine.api import taskqueue
from google.appengine.ext import ndb
import webapp2


class Human:
    def __init__(self, dna):
        self.dna = dna

    def is_mutant(self):
        #TODO: implementar algoritmo solicitado
        return self.dna is not None


class Dna(ndb.Model):
    dna = ndb.JsonProperty()
    is_mutant = ndb.BooleanProperty(indexed=True)


class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("""            
            <form method="post" action="/mutant">
                <label>DNA</label>
                <textarea name="dna" cols="40" rows="6">{"dna":["ATGCGA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"]}</textarea>
                <button>Send</button>
            </form>
        """)


class StatsHandler(webapp2.RequestHandler):
    def get(self):
        count_mutant_dna = Dna.query(Dna.is_mutant==True).count()
        count_human_dna = Dna.query(Dna.is_mutant==False).count()
        ratio = 'undefined'
        if count_human_dna > 0:
            ratio = count_mutant_dna/count_human_dna
        result = {"count_mutant_dna": count_mutant_dna, "count_human_dna": count_human_dna, "ratio": ratio}
        self.response.write(result)


class EnqueueTaskHandler(webapp2.RequestHandler):
    def post(self):
        dna = self.request.get('dna')
        human = Human(dna)
        is_mutant = human.is_mutant()

        queue = taskqueue.Queue(name='default')
        task = taskqueue.Task(
            url='/insert_dna',
            target='worker',
            params={'dna': dna, 'is_mutant': is_mutant})

        queue.add(task)

        if is_mutant:
            self.response.write('Is mutant.')
        else:
            self.response.write("Is human.")
            self.response.status_code(403)


app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/stats', StatsHandler),
    ('/mutant', EnqueueTaskHandler)
], debug=True)
