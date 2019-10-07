import numpy as np

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
nltk.download('averaged_perceptron_tagger')
from urllib.request import urlopen
from bs4 import BeautifulSoup
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

def synonymous(word1):
  synonyms = []
  
  for syn in wn.synsets(word1):
    for l in syn.lemmas():
      synonyms.append(l.name())

  synonyms = (list(synonyms))

  syn = []
  for i in synonyms:
    if i not in syn:
      syn.append(i)

  
  return syn

synonymous("hello")

url = "https://www.geeksforgeeks.org/introduction-data-science-skills-required/"
url = "https://en.wikipedia.org/wiki/Car"

def open_and_extract(url):
  html = urlopen(url)
  soup = BeautifulSoup(html, 'lxml')
  
  title = soup.title
  
  text = soup.get_text()
  
  arr = [''] * 10000000
  j=0
  for i in soup.text:
    arr[j] = arr[j] + (i)
    if i == '\n':
      j+=1
  return title, arr, soup, soup.text

title, arr, soup, soup_text = open_and_extract('https://stackoverflow.com/questions/26182980/can-anyone-give-a-real-life-example-of-supervised-learning-and-unsupervised-lear')



def linker(soup):
  all_links = soup.find_all("a")
  links = []
  linkez = []
  for link in all_links:
      links.append(link.get("href"))
  res = []
  for val in links:
      if val != None :
          res.append(val)
  for i in res:
    if i.startswith('https') :
      linkez.append(i)
  return linkez

linkz = linker(soup)
for i in linkz:
  print(i)



def final_tagger(soup_text,stop_words, W0 = 1, W1 = 0.00025, W7 = 0.1, W8 =50):
  soup_text = soup_text.replace("akproto"," ").replace("akquicv"," ").replace("documentgetelementsbytagnamescript0"," ").replace(","," ").replace("+"," ").replace("-"," ").replace("."," ").replace("@"," ").replace("'"," ").replace(":"," ").replace(";"," ").replace("!"," ").replace("#"," ").replace("%"," ").replace("^"," ").replace("&"," ").replace("*"," ").replace("("," ").replace(")"," ").replace('"'," ").replace("{"," ").replace("}"," ").replace("}"," ").replace("["," ").replace("]"," ")
  soup_text = soup_text.replace("https"," ").replace("geeksforgeeksorg"," ").replace("configpageparams"," ").replace("="," ").replace("_"," ").replace(":"," ").replace(";"," ").replace("<"," ").replace(">"," ").replace("?"," ").replace("/"," ").replace(","," ").replace("|"," ").replace('\\',' ').replace("adsbygoogle"," ").replace("windowadsbygoogle"," ").replace('www',' ').replace('com',' ')
  soup_text = soup_text.replace("gfglogopng"," ").replace("documentcreateelementscript"," ").replace('–'," ").replace('’',' ').replace("documentcreateelementscript"," ").replace("documentlocationprotocol"," ").replace("documentgetelementsbytagnamescript0"," ").replace("kgetcontextkgetcontext2dforj"," ").replace("bcreateelementcanvas"," ").replace("jlengthicsupportsji"," ")
  soup_text = soup_text.replace("gfglogopng"," ").replace("font"," ").replace("documentelement"," ").replace("stackexchange", " ")
  
  
  
  
  words = nltk.tokenize.word_tokenize(soup_text)
  
  
  
  stop_words = list(stop_words)
  stop_words.append('http')
  stop_words.append("documentelement")
  

  
  



  final_sentence = []
  for i in words:
    if i not in stop_words:
      final_sentence.append(i.lower())
  
  tagging = nltk.pos_tag(final_sentence)




  #fd = nltk.FreqDist(final_sentence)
  




  nouns = []
  for j in tagging:
    if j[1].startswith('N'):
      nouns.append(j[0])
  




  
  

  

  bigrams = list(nltk.bigrams(nouns))
  freq_dist_bi = nltk.FreqDist(bigrams)
  freq_dist_bi = list(freq_dist_bi.most_common(100))
  
  
  
  trigrams = list(nltk.trigrams(nouns))
  freq_dist_tri = nltk.FreqDist(trigrams)
  #print(list(freq_dist_tri.most_common(100)))
  freq_dist_tri = list(freq_dist_tri.most_common(100))
  

  removes = ['js','a','opensans','view','googletag','stackexchange','init','meta','f668','c8062454a840','allowretractingcommentflags','a168d277c579','fbe5e73dec7c','setcachebreakers','asteriskintrawordemphasis','clienttimingsdebouncetimeout','clienttimingsabsolutetimeout','backgroundcolor','posteditionsection','qarefreshpartone','isanonymousnetworkwide','childurl','routename','servertime','snippets','e73509971b05','stackauth','enablesocialmediainsharepopup','insertspaceafternametabcompletion','trackoutboundclicks','cmd','subscribetoquestion','showncommentcount','f4a83d','highlightcolor','stackexchange','showanswerhelp','totalcommentcount','postvalidation','dislikedtagsmaxlength','mincompletebodylength','likedtagsmaxlength','googlefonts','b','js','c','d','e','f','wbhack','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','z','y','analytics','css','values','function','window','var','addeventlistener','documentelement','classname','wgaction','wgcanonicalnamespace','wgcanonicalspecialpagename','wgnamespacenumber','client','rlconf','wgpagename','wgtitle','wgcurrevisionid','wgrelevantarticleid','wgmfdisplaywikibasedescriptions','pagevariantfallbacks','pagelanguagedir','pagelanguagecode','wgvisualeditor','wgpopupsconflictswithnavpopupgadget','wgrequestid','wgpopupsreferencepreviews','wgmediaviewerenabledbydefault','wgmediavieweronclick','wgrestrictionedit','wgcspnonce','xzjoigpamfeaackxcreaaabn','wgdefaultdateformat','wgmonthnamesshort','wgrelevantpagename',"wgmonthnames",'wgpagecontentlanguage','wgpagecontentmodel','wgcategories','wgusergroups','wgrevisionid','wgarticleid','wgisarticle','wgisredirect']
  final_tags = []
  for b in bigrams:
    for temp in b:
      
      if (temp not in final_tags) and (temp not in removes): #and (temp in words.words()):
        final_tags.append(temp)
  for t in trigrams:
    for temp in t:
      
      if temp not in final_tags and (temp not in removes): #and (temp in words.words()):
        final_tags.append(temp)
  


  
  
  points = []
  for i in range(len(final_tags)):
    points.append(float(W0 * (len(final_tags) - i)))
  
  for i in range(len(final_tags)):
    syn = synonymous(final_tags[i])
    for j in range(i+1, len(final_tags)):
      if final_tags[j] in syn:
        points[i] += W1 * (len(final_tags) - j)
  
  
  
  
  
  
  
  for k in range(len(final_tags)):
    for i in range(len(freq_dist_bi)):
      if final_tags[k] == freq_dist_bi[i][0][0] or final_tags[k] == freq_dist_bi[i][0][1]:
        points[k] += W7 * freq_dist_bi[i][1]
  
    
  for k in range(len(final_tags)):
    for i in range(len(freq_dist_tri)):
      if final_tags[k] == freq_dist_tri[i][0][0] or final_tags[k] == freq_dist_tri[i][0][1] or final_tags[k] == freq_dist_tri[i][0][2]:
        points[k] += W8 * freq_dist_tri[i][1]
  
    
    
    
  for i in range(len(points)):
    largest = i
    for j in range(i+1, len(points)):
      if points[j] > points[largest]:
        largest = j
    points[i], points[largest] = points[largest], points[i]
    final_tags[i], final_tags[largest] = final_tags[largest], final_tags[i]
  
  
  

  
  
  
  
  return final_tags, list(points), freq_dist_tri[:3], freq_dist_bi[:2]

tags, point, tri, bi = final_tagger(soup_text,stop_words)
print(tags)
print(tri)

def complete_tagger(ur,weights):
  title, arr, soup, soup_text = open_and_extract(ur)
  linkz = linker(soup)
  tags, point, tri, bi = final_tagger(soup_text,stop_words,weights[0], weights[1], weights[7], weights[8])
  return title, arr, soup, soup_text, linkz, tags, point, tri, bi

complete_tagger("https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk",[3,0.0025,0.01, 0.1, 3.7, 5.6, 10.11, 0.1, 50])

def uptil_links_ranker(weights, url):
  title, arr, soup, soup_text, linkz, tags, point, tri, bi = complete_tagger(url, weights)
  
  points = []
  for j in tags:
    temp = 0
    for i in linkz:
      if j in i:
        temp += 1
    points.append(temp)
  
  points = np.array(points)
  point = np.array(point)
  point = point + weights[2] * points
  
  for i in range(len(point)):
    largest = i
    for j in range(i+1, len(point)):
      if point[j] > point[largest]:
        largest = j
    point[i], point[largest] = point[largest], point[i]
    tags[i], tags[largest] = tags[largest], tags[i]
    
  point = list(point)
  return tags, point, linkz, title, tri, bi

uptil_links_ranker([3,0.0025,0.01, 0.1, 3.7, 5.6, 10.11, 0.1, 50],url)

# [0, 0.0025, 0.01, 0, 0, 0, 0, 0.1, 50, 1, 1, 10, 1]
# [3, 0.0025, 0.01, 0.1, 3.7, 5.6, 10.11, 0.1, 50, 1, 1, 10, 0]
def spider(url, weights = [1, 0.0025, 0.01, 0, 0, 0, 0, 0.1, 50, 1, 1, 10, 1]):
  n0 = int(weights[4])
  n1 = int(weights[5])
  n2 = int(weights[6])
  tags, points, links, title, tri, bi = uptil_links_ranker(weights, url)
  connections = []
  linkz = []
  titlez = []
  for i in tags[:n0]:
    for j in links:
      if i in j:
        linkz.append(j)
  
  for i in linkz[:n1]:
        try:
          tags_temp, points_temp, links_temp, titles_temp, tri_temp, bi_temp = uptil_links_ranker(weights, i)
          connections.append(tags_temp[:n2])
          titlez.append(str(titles_temp))
          
        except:
          continue
  
  title_col = []
  for i in titlez:
    
    try:
      i = i.replace("<title>"," ").replace("</title>"," ")
    except:
      continue
    title_col.append(i)
  
  connections_new = []
  for i in connections:
    for j in i:
      if j not in connections_new:
        connections_new.append(j)
  
  for i in connections:
    for j in i:
      if j in tags:
        points[tags.index(j)] += weights[3]*(len(connections_new)-connections_new.index(j))
      
  title = str(title)
  title = title.replace("<title>"," ").replace("</title>"," ")
  
  for i in range(len(tags)):
    if tags[i] in title:
      points[i] += weights[9] * (len(title)-(title.index(tags[i])))
    
  for i in range(len(tags)):
    for j in title_col:
      if tags[i] in j:
        points[i] += weights[10] * (len(j)-(j.index(tags[i])))
  
  
  
  
  #tri_new = []
  for i in tri:
    for j in i[0]:
      if j in tags:
        points[tags.index(j)] += weights[11] * (i[1])
        
  
        
  for i in bi:
    for j in i[0]:
      if j in tags:
        points[tags.index(j)] += weights[12] * (i[1])
  
  
  
  
  
  
  for i in range(len(points)):
    largest = i
    for j in range(i+1, len(points)):
      if points[j] > points[largest]:
        largest = j
    points[i], points[largest] = points[largest], points[i]
    tags[i], tags[largest] = tags[largest], tags[i]
    
  points = list(points)
  
  tags = tags[:5]
  for i in tri:
    if (i[0][0] + ' ' + i[0][1]) not in tags:
      tags.append(i[0][0] + ' ' + i[0][1])
    if (i[0][1] + ' ' + i[0][2]) not in tags:
      tags.append(i[0][1] + ' ' + i[0][2])

  
  for i in bi:
    if (i[0][0] + ' ' + i[0][1]) not in tags:
      tags.append(i[0][0] + ' ' + i[0][1])

  return tags

wot = [1, 0.0025, 0.01, 0, 0, 0, 0, 0.1, 50, 1, 1, 10, 1]
a = spider('https://stackoverflow.com/questions/26182980/can-anyone-give-a-real-life-example-of-supervised-learning-and-unsupervised-lear', wot)
print(a)

def machine_learning_function():
  #           0    1      2    3  4  5  6   7   8   9  10  11  12
  #weights = [1, 0.0025, 0.01, 0, 0, 0, 0, 0.1, 50, 1,  1, 10, 1]
  '''
  WEIGHTS EXPLANATION:
  W[0]  * FREQUANCY DISTRIBUTION POSITION
  W[1]  * SUM OF FREQUENCY DISTRIBUTION OF THEIR SYNONYMS
  W[2]  * NUMBER OF TIMES THE WORD/TAG IS REPEATED IN ALL LINKS, HREF, ETC.
  W[3]  * NUMBER OF TIMES THE WORD/TAG IS REPEATED IN ALL OUTGOING LINKS
  W[4]  = NUMBER OF TAGS TO BE ANALYSED USING SPIDER
  W[5]  = NUMBER OF LINKS TO BE ANALYSED USING SPIDER AFTER CATEGORISATION FROM W[4]
  W[6]  = NUMBER OF TAGS TO BE COUNTED FOR FROM EACH LINK
  W[7]  * FREQUENCY DISTRIBUTION OF TAG/WORD IN BIGRAMS
  W[8]  * FREQUENCY DISTRIBUTION OF TAG/WORD IN TRIGRAMS
  W[9]  * POSITION IN TITLE OF CURRENT PAGE
  W[10] * POSITION IN TITLES OF ALL LINKS ANALYSED IN SPIDER
  W[11] * FREQUENCY DISTRIBUTION OF TRIGRAM IN WHICH THE TAG/WORD APPEARS
  W[12] * FREQUENCY DISTRIBUTION OF BIGRAM IN WHICH THE TAG/WORD APPEARS
  '''
  weights = [1, 0.0025, 0.01, 0, 0, 0, 0, 0.1, 50, 1,  1, 10, 1]

machine_learning_function()
