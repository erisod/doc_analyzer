# doc_analyzer
UTF-8 document analyzer.

I built this toy-quality app-engine tool (deployed here : https://dup-token-analyzer.appspot.com/) to help my wife, an author, evaluate accidental re-use of the same word within a few sentance distance.  It takes a Word (docx) document and using NLTK (a natural language library) scans the input text considering a configurable sliding window of words to find duplicate uses.  It also identifies a few other common document errors such as duplicate words words.

## Example
For input of:
`"He ran quickly through the forest trying to escape and came upon a ladder leaning against a tree.  Quickly he set to climbed up.  And climb he did."`, identify re-use of the word 'quickly', and 'climb'.  Note that it's able to identify a dupcate despite a different suffix or case.  A hard-coded list of ignore words avoids reporting for 'a', 'he', etc.

## Room for improvement
1. The ignore words are hard coded.  Consider doing a full document analysis of high frequency words to identify the ignores.  As it is, I have some proper nouns (character names) in the ignore list.
2. The UI is pretty messy and as a workflow tool leaves much to be desired.  It would be nice to somehow fingerprint the duplicates reported (by sentence?) so they could be ignored in subsequent document revisions if the re-use is intentional.  Having to review the same non-issues is painful.
3. Efficiency improvements.  As this was hacked together and is fast enough for it's intended purpose I've not invested here but it can surely be improved with little effort.
4. Uses hard-coded chapter break identifiers.  In order to direct the user (my wife) to the appropriate section I've included a chapter identifier scheme.  This could be generalized in some fashion.
5. Word likes to use some fancy characters (quotes, elipses, etc) which caused problems and I've just replaced those characters as I found them to be of issue.  A more general character replacement scheme could be useful.
6. Code cleanup.  This code is still in a 'hack it up to make it work for Ashley' mode and has various semi-failed-approaches  that are commented out.
7. Output formatted is mixed into the code.  Using a templating approach would be nicer.
8. This code has no tests.  Embarassing.

## Requirements
Requires nltk (www.nltk.org/).
