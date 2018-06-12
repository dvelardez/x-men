from google.appengine.ext import ndb

import human_counter
import mutant_counter


class Dna(ndb.Model):
    dna = ndb.JsonProperty()
    is_mutant = ndb.BooleanProperty(indexed=True)


@ndb.transactional(xg=True)
def add_dna(dna, is_mutant):
    new_dna = Dna(dna=dna, is_mutant=is_mutant)
    new_dna.put()
    if is_mutant:
        mutant_counter.increment()
    else:
        human_counter.increment()
