from google.appengine.api import taskqueue
from google.appengine.ext import ndb
import webapp2
import itertools
import json


class Human:
    @staticmethod
    def is_mutant(dna):
        rows = len(dna)
        columns = len(dna[0])
        sequences_found = []
        for i in range(rows - 4 + 1):
            for j in range(columns - 4 + 1):
                for item in Human.iterate_submatrix(dna, i, j):
                    consecutive = Human.consecutive(item)
                    if consecutive and item not in sequences_found:
                        print item
                        sequences_found.append(item)
        return len(sequences_found) > 1

    @staticmethod
    def consecutive(group):
        first, second = itertools.tee(group)
        second.next()
        for first, second in itertools.izip(first, second):
            if second != first:
                return False
        return True

    @staticmethod
    def iterate_submatrix(matrix, t, l):
        # yield the horizontals and diagonals of 4x4  subsection of matrix starting at t(op), l(eft) as 4-tuples
        submat = [row[l:l + 4] for row in matrix[t:t + 4]]
        for r in submat:
            yield tuple(r)
        for c in range(0, 4):
            yield tuple(r[c] for r in submat)
        yield tuple(submat[rc][rc] for rc in range(0, 4))
        yield tuple(submat[rc][3 - rc] for rc in range(0, 4))


class Dna(ndb.Model):
    dna = ndb.JsonProperty()
    is_mutant = ndb.BooleanProperty(indexed=True)


class StatsHandler(webapp2.RequestHandler):
    def get(self):
        count_mutant_dna = Dna.query(Dna.is_mutant==True).count()
        count_human_dna = Dna.query(Dna.is_mutant==False).count()
        ratio = 'undefined'
        if count_human_dna > 0:
            ratio = float(count_mutant_dna)/count_human_dna
        result = {"count_mutant_dna": count_mutant_dna, "count_human_dna": count_human_dna, "ratio": ratio}
        self.response.write(result)


class DetectMutantHandler(webapp2.RequestHandler):
    def post(self):
        if not self.request.body:
            self.response.write("Bad request.")
            self.response.status_int = 400
            return

        dna = json.loads(self.request.body)
        human = Human()
        is_mutant = human.is_mutant(dna.get('dna'))

        queue = taskqueue.Queue(name='default')
        task = taskqueue.Task(
            url='/insert_dna/',
            target='worker',
            params={'dna': dna, 'is_mutant': is_mutant})

        queue.add(task)

        if is_mutant:
            self.response.write('It is mutant.')
        else:
            self.response.write("Is human.")
            self.response.status_int = 403


app = webapp2.WSGIApplication([
    ('/stats/', StatsHandler),
    ('/mutant/', DetectMutantHandler)
], debug=True)
