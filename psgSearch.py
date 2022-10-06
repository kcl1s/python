from bs4 import BeautifulSoup
import requests
import webbrowser
import PySimpleGUI as sg

allLinks=[]
keyText= sg.PopupGetText('Please enter serch terms',title='PSG Search')

keywords= keyText.split()
urls= ['https://www.pysimplegui.org/en/latest/',       
        'https://www.pysimplegui.org/en/latest/call%20reference/',
        'https://www.pysimplegui.org/en/latest/cookbook/',
        'https://www.pysimplegui.org/en/latest/Demos/']
for url in urls:
    links= []
    linkHTML='<h2 style="font-size:30px;">Results From '+url+'</h2><p style="font-size:20px;">'
    website= requests.get(url)
    webText= website.text
    soup= BeautifulSoup(webText)
    for link in soup.find_all('a'):
        alink= str(link.get('href')) 
        if alink.startswith('#'):
            linkText= link.text
            matches  = [x for x in keywords if x in linkText.lower()]
            links.append([alink, link.text,len(matches)])
    links= [x for x in links if x[2]>0]
    links.sort(reverse=True,key=lambda x: int(x[2]))
    for link in links:
        #print (link)
        thisHTML = '<a href="'+url+link[0]+'">'+link[1]+'</a><br>'
        #print (thisHTML)
        linkHTML += thisHTML
    linkHTML += '</p>'
    #print (len(links))
    allLinks.append(linkHTML)

searchURL = "psgSearch.html"
f = open(searchURL, 'w')
htmlOpen = '<html>\n<head>\n<title>Title</title>\n</head>\n<body>\n<center>\n<h2 style="font-size:60px";>PySimpleGUI Search</h2>\n'
htmlClose = '<center>\n</body>\n</html>'
html_template = htmlOpen + allLinks[0] + allLinks[1] + allLinks[2] + allLinks[3] + htmlClose
f.write(html_template)
f.close()
webbrowser.open(searchURL)