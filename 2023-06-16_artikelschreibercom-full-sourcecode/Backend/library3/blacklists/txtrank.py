#!/usr/bin/env python
# encoding: utf-8

import logging
#import pytextrank
import spacy
import sys
import pytextrank as pyt
from pytextrank import TextRank

text=""" 
Der Milliardär stieg spät in den Wahlkampf ein, jetzt zählt er zu den Favoriten. Michael Bloomberg pumpt Hunderte Millionen in seine Kampagne. Kann das funktionieren?
Von Klaus Brinkbäumer
17. Februar 2020, 5:56 Uhr54 Kommentare
Michael Bloomberg: Bei keiner TV-Debatte war Michael Bloomberg dabei, in den ersten vier Staaten steht er nicht mal zur Wahl. Doch der Einsatz seines Milliardenvermögens schiebt New Yorks ehemaligen Bürgermeister zunehmend ins Rampenlicht.
Michael Bloomberg – dank ihm beginnt der US-Präsidentschaftswahlkampf in diesen Tagen noch einmal neu und von vorn. © Brett Carlsen/​Getty Images
InhaltAuf einer Seite lesen
INHALT
Er ist niemals da, wo die anderen sind, explizit nicht, darum geht es. Sind sie in Iowa, dann reist er durch Florida oder South Carolina, sind sie in New Hampshire, dann fährt er durch Texas, und kommen die anderen in wenigen Tagen nach South Carolina, war er schon da; wo er dann sein wird, verrät er heute natürlich noch nicht.

Offen ist, wer hier Hase und wer Igel ist und wer dieses seltsame Rennen gewinnen und damit ganz am Ende recht gehabt haben wird. Sicher hingegen ist: Michael Bloomberg, 78, nervt die anderen, denn seine Strategie wirkt.

Bernie Sanders spricht inzwischen in jeder seiner Reden von diesem Bloomberg und sagt, der Kerl wolle "die Wahl kaufen". Die USA dürften sich "nicht länger vom Geld dominieren lassen, das Washington viel zu lange dominiert hat", das sagt Elizabeth Warren. Es sind ohnmächtige Worte, da Bloomberg zwar tatsächlich einen Geldwahlkampf führt, aber es ist sein eigenes Geld und er braucht keine Spenden. "Ich bin unabhängiger als all meine Gegner", sagt er und im finanziellen Sinne stimmt das.

Darum beginnt der amerikanische Präsidentschaftswahlkampf in diesen Tagen noch einmal neu und von vorn. 
Bloomberg pumpt Hunderte Millionen in seine Kandidatur
Im vergangenen Sommer erklärten 27 Bewerberinnen und Bewerber ihre Kandidatur, dann formten sie ihre Kampagnen, ihr Netzwerk, legten los. Und nach und nach stiegen jene, die sich nicht für die Fernsehdebatten qualifizierten, weil ihre Umfragewerte zu niedrig waren, wieder aus. Es war aufreibend und nur teilweise aufregend, und Bloomberg sah zu und fand das Geschehen "schwach", wie er heute sagt. Die moderaten Kandidaten, selbst die führenden, Joe Biden, Pete Buttigieg und Amy Klobuchar, überzeugten ihn nicht: "Donald Trump wird wiedergewählt", sagte Bloomberg im Oktober auf einer New Yorker Party. Und die progressiven, in Amerika als linksextrem oder auch sozialistisch geltenden Kandidaten, Bernie Sanders und Elizabeth Warren, erschreckten Bloomberg. "Washington, D. C. ist nicht Moskau", auch das ist ein Bloomberg-Satz.

Im November griff er ein und erklärte seine Kandidatur, und das kam sehr, sehr spät. Auf die ersten acht Fernsehdebatten verzichtete er also und, vor allem, auf die ersten vier Vorwahlen: Iowa, New Hampshire, Nevada (19.2.) und South Carolina (29.2.). Erst zu den vierzehn Vorwahlen des Super Tuesday am 3. März steigt Bloomberg ein.

Solch eine Kandidatur gab es in den USA noch nie, doch heißt das, dass man so nicht siegen kann? Und heißt das, dass es unmoralisch ist? Dass man auf Bloombergs Weise nicht siegen darf?

60 Milliarden Dollar besitzt der Mann, er ist der achtreichste Mensch der Welt. Der auf Wirtschaft spezialisierte Medienkonzern Bloomberg L.P. und die Tochter Bloomberg Television sind seine Schöpfungen. 188 Millionen Dollar hat Bloomberg in nur drei Monaten ausgegeben, vor allem für TV-Spots und Anzeigen in den sozialen Medien. Er überschwemmt den Wahlkampf. Er ist omnipräsent. Und er kontert Präsident Trump – dort, wo Trump die Vereinigten Staaten beherrscht und unbesiegbar erschien.
"""

######################################################################
## sample usage
######################################################################

# load a spaCy model, depending on language, scale, etc.

nlp = spacy.load("en_core_web_sm")

# logging is optional: to debug, set the `logger` parameter
# when initializing the TextRank object

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger("PyTR")

# add PyTextRank into the spaCy pipeline

tr = pyt.TextRank(logger=None)
nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)
tr.load_stopwords(path="/home/unaique/library/blacklists/stopwords_all.txt")

# parse the document

#with open("dat/mih.txt", "r") as f:
#    text = f.read()

doc = nlp(text)

print("pipeline", nlp.pipe_names)
print("elapsed time: {} ms".format(tr.elapsed_time))

# examine the top-ranked phrases in the document

for phrase in doc._.phrases:
    print("{:.4f} {:5d}  {}".format(phrase.rank, phrase.count, phrase.text))
    #print(phrase.chunks)
    print(phrase)
    
for phrase in doc._.phrases[:20]:
    print(phrase)
    
  