import wikipedia
from bs4 import BeautifulSoup


def get_html(title):
    return wikipedia.page(title).html()

def hasAttribute(obj,attr):
    try:
        whatevs = obj[attr]
        return True
    except:
        return False

def isOk(a):
    return not isLangLink(a) and hasAttribute(a,'title') and 'wikt:' not in a['title'] and '#cite_note' not in a['href'] and 'Help:' not in a['href'] and '.ogg' not in a['href'] and 'wikipedia/commons' not in a['href'] and 'Wikipedia:' not in a['href']

def isInfoBox(ele):
    try:
        res = 'vcard' in ele['class']
    except:
        res = False

    return res

def isLangLink(a):
    return "_language" in a['href']

def get_title_of_first_link_of_page(page_title):
    html = get_html(page_title)
    soup = BeautifulSoup(html,'html.parser')

    yes = False
    for table in soup.findAll('table'):
        if isInfoBox(table):
            yes = True
        #    print(table)
            break

  #  print(yes)

    if yes:
        candidates = soup.find_all()
        res = None
        passedInfoBox = False
        count = 0
        while res==None or not passedInfoBox and count<len(candidates):

            if not passedInfoBox:
                if isInfoBox(candidates[count]):
                    passedInfoBox=True
                count=count+1
                continue

            stri = str(candidates[count])
            if stri[0]=='<' and stri[1]=='p' and stri[2]=='>':
            #    print(candidates[count])
                for a in candidates[count].find_all('a'):
                    if isOk(a):
                        #print("selected ",a['href'])
                        res = a['title']
                        break

            count=count+1
        return res
    else:

        candidates = soup.find_all('p')
        res = None
        count = 0
        while res==None and count < len(candidates):
            summary = candidates[count]
            print(summary[0:100])
            count=count+1
            for a in summary.find_all('a'):
                if isOk(a):
              #      print("selected ",a['href'])
                    res = a['title']
                    break
        return res

title = "Bob Dylan"
while True:
    print(title)
    title = get_title_of_first_link_of_page(title)