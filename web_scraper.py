import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import contextlib

abb = {}
url = "https://www.tabers.com/tabersonline/view/Tabers-Dictionary/767492/all/Medical_Abbreviations"
def web_scraper():
    try:
        with contextlib.closing(urlopen(url)) as page:
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, 'html.parser')
            unprocessed_p = soup.find_all("p")[6]
            patternBreakLine = "<br/>"
            patternBold = "<b>.*?</b>"
            flag = False
            prev = None
            for x in unprocessed_p:
                x = str(x).strip()
                if bool(re.search(patternBreakLine,x,re.IGNORECASE)):
                    continue
                if flag:
                    if "," in prev:
                        prevs = prev.split(", ")
                        if prevs[0] != prevs[1]:
                            abb[prevs[0]] = x
                            abb[prevs[1]] = x
                        else:
                            abb[prevs[0]] = x
                    elif ";" in prev:
                        prevs = prev.split("; ")
                        if prevs[0] != prevs[1]:
                            abb[prevs[0]] = x
                            abb[prevs[1]] = x
                        else:
                            abb[prevs[0]] = x
                    else:
                        abb[prev] = x
                    prev = None
                    flag = False
                    continue
                if bool(re.search(patternBold,x,re.IGNORECASE)):
                    prev = x.lstrip("<b>").rstrip("</b>").lower()
                    if bool(re.search("&amp;",prev,re.IGNORECASE)):
                        prev = prev.replace("&amp;", "&")
                    if bool(re.search("overline",prev,re.IGNORECASE)):
                        continue
                    if bool(re.search("<",prev,re.IGNORECASE)):
                        prev = prev.replace("<sub>", "")
                        prev = prev.replace("</sub>", "")
                        prev = prev.replace("<sup>", "")
                        prev = prev.replace("</sup>", "")
                    if "," in prev or ";" in prev:
                        continue
                    abb[prev] = None
                    flag = True
            del abb['a']
            del abb['or']
            del abb['.']
            return abb
    except Exception as e:
        print("error: ",e)
