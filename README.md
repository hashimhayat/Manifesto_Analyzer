# Manifesto Analyzer

In this project I am looking at the manifestos published by political parties
that present their political ideology and preferences to the general public.

##Algorithm

The algorithm look at a party manifesto to calculate and analyze the political
ideology of the party on the left-right scale using key words, sentences and phrases
that left or right connotations. A similar has been used by many political scientists
and data analyzers such as the manifesto project and Wagner and Meyer (2016). A third
party sentiment analysis API has been used to judge the attitude in which each
reference key word has been used in the manifesto.

The reference key words or sentences are divided into two categories: left and right.
Left reference include words or phrases that are supported or rejected by the leftist
parities and vice versa.

Step 1: Fetching Data from the web

The First step gets and downloads the manifesto in a text format directly from the
web. Urllib, a python library to fetch the data. After the data is requested, it is
converted into string format and then all the characters in the text are converted to
lower case characters.

Step 2: Removes old and temporary Ailes

This step removes any old and temporary data Tiles from the working directory.
Step 3: Writes the data acquired form Step 1 on Aile
The manifesto text data fetched from the web is written on a Tile in this step for
backup and ofTline usage.

Step 4: Extracts data from reference Ailes

In order to analyze the manifestos, the user can include reference Tiles that includes
words, sentences or phrases that correspond to either political ideology (left or
right). For instance, if leftist parties support the implementation of taxes, the user
may include taxes into the left_ref.txt Tile.

The user may also include screen shots of words and phrases taken from published
papers or anywhere. In order to fetch the words and phrases from the images, we
use a python library that works as an OCR.

The words in the reference Tiles are read from the text Tiles or the image Tiles and
included into LEFT and RIGHT lists. Unimportant words, symbols and spaces such as
and, for, that are removed from the reference lists.

Step 5: Performs Left and Right Analysis

In the Tinal stage, the program goes through each word in the LEFT and RIGHT lists
and Tind those words in the manifesto data. For each word in the list, a function
called the word_freq counts the number of instances that word was repeated and
returns the indexes at which the word is present.

The indexes are later used to extract the sentences, one by one, in which the word
was used using the function called extract_sentence.

The sentence is then fed into the sentiment analyzer function that uses an API call to
a third part sentiment analyzer on the web to analyze whether the sentence has a
positive sentiment or negative.

##Sentiment Analysis API: http://text-processing.com/api/sentiment/
For instance, if the word is “military”, the algorithm extracts all the sentences in
which the words military has been used. Then each sentence is fed into the sentence
analyzer to Tind out if the word military is used in a positive reference or a negative
reference.

If a word is used more than once, the average ratio of sentiment is returned. The
words along with their frequency, negative and positive sentiments are written on
the two csv-Tiles: left_analyis and right_analyis in the result folder.
