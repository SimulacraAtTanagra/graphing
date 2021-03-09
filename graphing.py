# -*- coding: utf-8 -*-
"""
Created on Mon May 11 19:45:09 2020

@author: shane
"""

from labMTsimple.storyLab import *
import re
import matplotlib.pyplot as plt
from matplotlib import animation
import PyPDF2 
import os
from numpy.polynomial import Polynomial
import nltk
from nltk import word_tokenize, sent_tokenize
from funcy import chunks

lang = 'english'
labMT,labMTvector,labMTwordList = emotionFileReader(stopval=0.0,lang=lang,returnVector=True)


def wordshifter(i):
    iValence,iFvec = emotion(i,labMT,shift=True,happsList=labMTvector)
    iStoppedVec = stopper(iFvec,labMTvector,labMTwordList,stopVal=1.0)
    return(emotionV(iStoppedVec,labMTvector))
def splitscrape(text):
    sent_corpus = [s for s in nltk.sent_tokenize(text)]
    sent_corpus= ["".join(chunk) for chunk in chunks(int(len(sent_corpus)/100),sent_corpus)]
    plotlist=[wordshifter(x) for x in sent_corpus]
    return(plotlist)
def scriptscrape(filename):
    with open(filename, 'rb') as pdfFileObj:
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    plotlist=[pdfReader.getPage(i).extractText() for i in range(pdfReader.numPages)]
    plotlist=[re.sub('\d+\s\d+\S\d+\S\d+,\d+\s\S+\s\d+\S\d+\S\d+,\d+','\n',x) for x in plotlist]
    plotlist=[re.sub('<\S+\s+\S+>','\n',x) for x in plotlist]
    plotlist=[wordshifter(x) for x in plotlist]
    return(plotlist)
def flatlist(plotlist):
    flat_list = [item for sublist in plotlist for item in sublist]
    return(flat_list)
def consolidate(fn):
    plist=[]
    x=os.getcwd()
    if x[-11:]!='transcripts':
        directory_in_str= os.path.join(x,'transcripts')
    else:
        directory_in_str = x
    directory = os.fsencode(directory_in_str)           #defines directory as indicated string
    os.chdir(directory)                                 #navigate to directory specified
    for file in os.listdir(directory):                  #iterates over all the files here
        filename = os.fsdecode(file)                    #specifies filename from file
        if fn in filename:                  #isolates epub for further action
            #print(filename)
            plist.append(scriptscrape(filename))
    try:
        plist = flatlist(plist)
    except:
        plist= plist[0]
    return(plist)
def relative(flat_list):
    flat_list = [x-(sum(flat_list)/len(flat_list)) for x in flat_list]
    return(flat_list)
def displayer(plotlist3,title):
    plotlist3 = relative(plotlist3)
    plt.figure(figsize=(12,4))
    y=plotlist3
    x=[(x/len(plotlist3))*100 for x  in range(len(plotlist3))]
    plt.plot(x, y,alpha=.5)
    plt.title(title)
    plt.ylabel("Sentiment of dialog relative to mean")
    plt.xlabel("Percent of Movie")
    p = Polynomial.fit(x, y, 30)
    plt.plot(*p.linspace())
    plt.show()
