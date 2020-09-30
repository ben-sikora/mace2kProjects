
#USER GUIDE

#First Draft Coding Assignment by Ben Sikora for Mace2k Project

#Requires Python3 (Necessary for stanza and can change if need to)

#Please enter the PMC ID either as an argument or input in console 
# (Additional customization for entities and bioconcepts can be added)

#The program will output each sentence of the article and
#print the annotations as a list of dictionaries. 
# Each dictionary represents the contents of one annotation



#Used to open up the website of the API
import urllib

#Used to Navigate the XML format of the website
import xml.etree.ElementTree as ET

#Stanza is a python implementation of Standford NLP 
#Was used to split the sentences of each passage
import stanza

#For Args
import sys



#Generating the the URL for the user Given PMCID 
#For example PMC6982432
if len(sys.argv) > 1:
    url= str(sys.argv[1])
else:
    url= input("Please enter a PMC ID: ")

url="https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmcids=" + url


#The format for generating the URL. Identifiers and Bioconcepts could be specified by the user 
#https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/[Format]?[Type]=[Identifiers]&concepts=[Bioconcepts]



#The default URL used for testing 
locu_api= 'https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmcids=PMC6207735'


#Opening the URL and storing the contents into a string 
obj= urllib.request.urlopen(url).read()

#Storing the XML file into root 
root= ET.fromstring(obj)


#Implentation for Stanza
#If first time running will have to download the enlgish model
stanza.download('en')
#Using the default pipeline for english Model (Further customization available)
nlp= stanza.Pipeline('en')
#Important for annotation placement 
sum_char=0



#Will cycle through each passage of the article i.e Abstract, Introduction, and then print the setences and associated passages 
for passage in root.iter('passage'):

    print() #For Formatting 
    print()

    #The actual text of the passage 
    text= passage.find('text').text

    #Storing text into document object. Document object splits the text into 
    #setences and stores them into list doc.sentences
    doc=nlp(text)

    #Storing Sentence lengths into list
    sent_list= []

    #Annotations are given in reference to total length of article.
    #So need to find amount of chars before each passage
    #so can add to setence length 
    sum_char= int(passage.find('offset').text)

    #Creating list of when sentences occur in reference to total
    #length of the article 
    for sentence in doc.sentences: 
        sentence_size= len(sentence.text)+ sum_char
        sum_char= sentence_size
        sent_list.append(sentence_size)



    #Stores all the parts for each annotation
    entDict= {}

    #Stores the location of the annotation and the assocaited EntDict
    annotDict= {}

    #Goes through each annotation and fills annotDict and 
    #entDict for the entire passage
    for annotation in passage.iter('annotation'):
        entity= annotation.find('text').text #name of the entity
        entDict['ED']= entity
        for infon in annotation.iter('infon'):
            attrib= infon.get('key') #Type of Identifier
            entDict[attrib]=infon.text #Text of intenfier 
        location= annotation.find('location') 
        locationINT= int(location.get('offset'))
        annotDict[locationINT]= entDict
        entDict= dict()


    #Simple int iterator
    j= 0

    #Will create a list of all the annotations for a single sentence
    entList= []

    #Will store the setence number as a key and the value a Entlist for that sentence
    sentenceDict= {}



    #Will go through each annotDict and find the sentence 
    # associated with that location. 
    #After findinng the sentence will add the annotation to sentenceDict along
    #with the sentence location 
    for key in sorted (annotDict.keys()):
        for i in sent_list:
            if key<= i:
                if sentenceDict.get(j) == None: 
                    entList.append(annotDict[key]) #Swapping keys
                    sentenceDict[j]= entList
                else: 
                    (sentenceDict.get(j)).append(annotDict[key])
                break #Can come back to later 
            j= j+1
        entList= list()
        j=0
    

    #Printing sentences and annotations 
    for key in sentenceDict:
        print(doc.sentences[key].text)
        print(sentenceDict[key])
