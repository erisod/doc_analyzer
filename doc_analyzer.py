#!/usr/local/bin/python
# coding=utf-8

import nltk
import codecs
import ftfy
import sys
import re
import cgi

from collections import deque

reload(sys)
sys.setdefaultencoding('utf8')

display_html=True

def html(s):
  if display_html:
    print s

html("<html>")
html("<title>")
if display_html:
  print "Eric's Document Analyser"
html("</title>")
html("<body>")


file = codecs.open("/tmp/rs_final2.txt")
encode_as = 'ascii'
encode_errors = 'xmlcharrefreplace'

# Throw away some prefix chars that aren't ascii.
# file.read(20)

ignore_list=["&", "-", "of", "if", "''", "!", "'", "by", ",", "to", "and", "me", "the", "in", "or", "any", "are", "a", "i", "my", "was", "he", "that", "their", "were", "you", "they", "we", "her", "for", "it", "t", "as", "some", "what", "this", "on", "with", "an", "s", "an", "how", "is", "had", "at", "have", "her", "is", "it", "had", "from", "on", "me", "we", "at", "not", "be", "but", "she", "your", "this", "into", "are", "will", "an", "he", "our", "do", "has", '"', ".", "<", ">", '?"', '!"', ":", '."', ',"', "his", "?", "am", "lakshmi", "supriya", "hanuman", "sabrina", "grandma", "maharaja", "raynaud", "shahenn", "parvati", "copyright", "address" , "shaheen", "through", "grandfather", "captain", "vibhishana", "barrister", "giovanni", "officer", "surpanakha", "lieutenant", "grandmother", "himmler", "himself", "mother", "rama", "so", "him", "can", "ravana", "them", "rahul", "rupa", "could", "would" , "who", "such", "when", "us", "about", "there", "chapter", "more", "just", "been", "must", "too", "these", "where", "did", "mr", "than", "dr", "syed", "sita" "singh", "men", "didn", "did", "its", "go", "let", "jeff", "re", "d", "shanti", "onto", "ve", "hitler", "…", "–", "i'd", "don't", "i'm", "________________", ]

count = 0

# while True:

bigstring = file.read().decode('utf-8')
# bigstring = ftfy.fix_text(bigstring)

#if not len(bigstring):
#  break

html("<h1>")
print "Eric's Document Analyser"
html("</h1>")



html("<h2>")
print "Double Word Detection:"
html("</h2><ul>")
last = "" 
for w in bigstring.split(" "):
  if w.lower() == last.lower() and w.encode(encode_as, encode_errors):
    html("<li>")
    if display_html:
      print "Double-word: <b>%s</b>" % (w.encode(encode_as, encode_errors))
    else:
      print "   Double-word: %s" % (w)
    html("</li>")
  last = w

html("</ul><hr>")


sentences = nltk.sent_tokenize(bigstring)


master_duplist = {}

html("<title>")
print "\n\nHi!  I'll be processing %d sentences.\n\n" % len(sentences)
html("</title>")


html("<div id=summary>Summary Loading ...</div><hr>")


window = deque()
win_length = 6

last_duplist = {}

html("<h2>")
print "Duplicate words found in %d sentence groups: " % (win_length)
html("</h2>")

chapter = ""
chapter_marker = r'CHAPTER '

for sentence in sentences:
   if chapter_marker in sentence:
     chapter = re.search(r'(PART.*)?CHAPTER [0-9]+ .* [A-Z ]+', sentence, re.MULTILINE).group(0)
     html("<table width=100%><tr><td bgcolor=lightblue><h3><br><b>NEW CHAPTER : </b><font color=blue>" + chapter.encode(encode_as, encode_errors) + "</font></h3></td></tr></table>")
 
   # strip some characters that are problematic < >
 
   sentence = re.sub(r'[<>]', ' ', sentence)
   sentence = sentence.replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c",'"').replace(u"\u201d", '"')
   sentence = sentence.replace(",", '').replace('"', '')

   count = count+1

   # sentence = ftfy.fix_text(sentence) 

   # shift window
   window.append(sentence)
   if (len(window) > win_length):
     window.popleft() 

   section = " ".join(window)


   if False:
     print "=== SECTION ==="
     print section.encode(encode_as, encode_errors)
     print "==============="

   # tokens = nltk.word_tokenize(sentence)
   tokens = nltk.WhitespaceTokenizer().tokenize(sentence.lower())
   #tokens = nltk.WordPunctTokenizer().tokenize(section.lower().encode(encode_as, encode_errors))
   #tokens = nltk.WordPunctTokenizer().tokenize(section.lower())
   nomatch = True
   duplist = {}
   for token in tokens:
     token = re.sub(r'[.!?]', 'XYZ', token)

     # Remove common words
     if token.lower() in ignore_list:
       continue

     if False:
	     # Remove short words
	     if len(token) < 7:
	       continue

	     # skip words that don't in ly
	     if token[-2:] != "ly":
	       continue

     #print "Checking for duplicate of %s in %s" % (token, tokens)
     matching = filter(lambda x: token==x, tokens)
     if len(matching) > 1:

       # print "found dup token: %s" % (token) 

       if duplist.has_key(token):
	 duplist[token] = duplist[token] + 1
       else:
	 duplist[token] = 1

       if master_duplist.has_key(token):
	 master_duplist[token] = master_duplist[token] + 1
       else:
	 master_duplist[token] = 1

   # Suppress duplicates
   if duplist:
     for k in last_duplist.keys():
       if duplist.has_key(k) and duplist[k] <= last_duplist[k]:
         # print "    SUPPRESSING %s" % (k)
         duplist.pop(k, None)
       else:
         last_duplist.pop(k, None)

   else:
     last_duplist = {}

   if duplist:
     example=section.encode(encode_as, encode_errors)

     for k in duplist.keys():
       if k:
         ex = r'\b(' + re.escape(k) + r')\b'
         if display_html:
           example = re.sub(ex, r'<b>\1</b>', example, flags=re.IGNORECASE)       
         else:
           example = re.sub(ex, "__"+k.upper()+"__", example, flags=re.IGNORECASE)       

     html("<div>")
     html("<b># %d : </b>" % count)
     html("<font face=garamond>")
     print example
     html("</font><font face=arial color=555555><ul>")
     for k in duplist.keys():
       if display_html:
         # print "<li><b>%s</b> duplicated %d times.</li>" % (k, duplist[k])
         print "<li>word <b>%s</b> duplicated %d times.</li>" % ((k.encode(encode_as, encode_errors)), duplist[k])
       else:
         print "  --> %s (%d dups)" % (k.encode(encode_as, encode_errors), duplist[k])
       if not last_duplist.has_key(k):
         last_duplist[k] = duplist[k]
     print ""
     html("</ul></font>")
     html("</div><br>")


html("<div id='summary_src'>")
html("<h2>")
print "Global Duplicate Word Counts:"
html("</h2><ul>")
 
sorted_master = sorted(master_duplist, key=master_duplist.get, reverse=True)
for k in sorted_master:
  html("<li>")
  if display_html:
    # print "<b>%s</b> was found as a duplicate %d times globally." % (k, master_duplist[k])
    print "<b>%s</b> was found as a duplicate %d times globally." % ((k.encode(encode_as, encode_errors)), master_duplist[k])
  else:
    print "  --> %s (%d dups)" % (k.encode(encode_as, encode_errors), master_duplist[k])
  html("</li>")

html("</ul>")
html("</div>")

html('<script>document.getElementById("summary").innerHTML=document.getElementById("summary_src").innerHTML;')
html('document.getElementById("summary_src").innerHTML = "";</script>')


html("</body></html>")

