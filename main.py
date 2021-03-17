import genanki
from bs4 import BeautifulSoup as bs
import requests
import urllib
import regex as re

target_Uri = 'http://www.messier.seds.org/m/m{0}.html' # $ 3 digits with padding

messier_catalog = []
media = []


# Objects go from M1 - M110
for _ in range(1, 111):#111):
    target = str(_).zfill(3)
    url = target_Uri.format(target)

    print("-------------------------")
    print(target)

    soup = bs(requests.get(url).text, 'html5lib')


    # Gets type
    mtype = soup.find_all('i')[0].get_text().split('M')[0].replace('\n', ' ').replace('\r',' ') # Don't ask why it works
    print(mtype) # Type of constellation


    # Gets constellation
    cons = soup.select_one("a[href*=map]").get_text()
    if cons == "Serpens (Cauda)":
      cons = "Serpens"
    print(cons)
    

    #Name (if present)
    try:

        name = soup.find_all('b')[1].get_text()
    except:
        name = ""

        
    if " " not in name:
        name = ""
    print(name)


    image  = 'http://www.messier.seds.org/JpgSm/m{0}.jpg'.format(_)
    print(image)

    urllib.request.urlretrieve(image, "{0}.jpg".format(_)) # should download image
    media.append("{0}.jpg".format(_))
    
    
    # Discovered


    description = ""
    l = -1
    while not ("discovered" in description or "Discovered" in description or "Known" in description):
        l+=1
        description = soup.find_all("p")[l].get_text().split(". ")[0].replace('\n', '').replace('\r', '')

    description = (soup.find_all("p")[l+1].get_text().split(". ")[0].replace('\n', '').replace('\r', '')+ ".").replace('..', '.') 
    print(description)

    try:
        discovered = soup.find_all(text=re.compile('Discovered*'))[0].replace('\n', '').replace('\r', '')
        
    except:
        try:
            discovered = soup.find_all(text=re.compile('Known to*'))[0].replace('\n', '').replace('\r', '')
        except:
            discovered = soup.find_all(text=re.compile('discovered by*'))
            discovered = "\n".join([x.replace('\n', '').replace('\r', '') for x in discovered])
    
    print(discovered)

    messier_object = {'mid': str(_),
                    'cons': cons,
                    'type': mtype,
                    'name': name,
                    'discoveredby': discovered,
                    'description': description,
                    'objectimage': "<img src=\"{0}.jpg\" />".format(_),
                    'consimage': "<img width =\"600\" src=\"{0}.gif\" />".format(cons)
                     }


    messier_catalog.append(messier_object)


cons_media = ["Andromeda.gif","Antlia.gif","Apus.gif","Aquarius.gif","Aquila.gif","Ara.gif","Aries.gif","Auriga.gif","Boötes.gif","Caelum.gif","Camelopardalis.gif","Cancer.gif","Canes Venatici.gif","Canis Major.gif","Canis Minor.gif","Capricornus.gif","Carina.gif","Cassiopeia.gif","Centaurus.gif","Cepheus.gif","Cetus.gif","Chamaeleon.gif","Circinus.gif","Columba.gif","Coma Berenices.gif","Corona Australis.gif","Corona Borealis.gif","Corvus.gif","Crater.gif","Crux.gif","Cygnus.gif","Delphinus.gif","Dorado.gif","Draco.gif","Equuleus.gif","ERI.gif","Fornax.gif","Gemini.gif","Grus.gif","Hercules.gif","Horologium.gif","Hydra.gif","Hydrus.gif","Indus.gif","Lacerta.gif","Leo.gif","Leo Minor.gif","Lepus.gif","Libra.gif","Lupus.gif","Lynx.gif","Lyra.gif","Mensa.gif","Microscopium.gif","Monoceros.gif","MUS.gif","Norma.gif","Octans.gif","Ophiuchus.gif","Orion.gif","Pavo.gif","Pegasus.gif","Perseus.gif","Phoenix.gif","Pictor.gif","Pisces.gif","Piscis Austrinus.gif","Puppis.gif","Pyxis.gif","Reticulum.gif","Sagitta.gif","Sagittarius.gif","Scorpius.gif","Sculptor.gif","Scutum.gif","Serpens.gif","Sextans.gif","Taurus.gif","Telescopium.gif","Triangulum Australe.gif","Triangulum.gif","Tucana.gif","Ursa Major.gif","Ursa Minor.gif","Vela.gif","Virgo.gif","Volans.gif","Vulpecula.gif"]

for c in cons_media:
  media.append(c)


messier_model = genanki.Model(
  1607392319,
  'Messier Object',
  fields=[
    {'name': 'mid'},
    {'name': 'cons'},
    {'name': 'type'},
    {'name': 'name'},
    {'name': 'discoveredby'},
    {'name': 'description'},
    {'name': 'consimage'},
    {'name': 'objectimage'}
  ],
  templates=[
    {
      'name': 'Constellation',
      'qfmt': '<div class=frontbg>Which constellation is M{{mid}} in?</div>',
      'afmt': '{{FrontSide}}<div class=backbg><hr id="answer">{{cons}}<br>{{consimage}}<br>{{discoveredby}}</div>', # Constellation with image of constellation on back
    },
    {  
      'name': 'Type',
      'qfmt': '<div class=frontbg>What type of deep sky object is M{{mid}}?</div>',
      'afmt': '{{FrontSide}}<div class=backbg><hr id="answer"><u>{{type}}</u><br><br>{{objectimage}}<br>{{description}}</div>',  
    },
    {  
      'name': 'Name',
      'qfmt': '{{#name}}<div class=frontbg>What is the common name of M{{mid}}?</div>{{/name}}',
      'afmt': '{{FrontSide}}<div class=backbg><hr id="answer">{{name}}<br>{{objectimage}}</div>',  
    }
  ],
  css='ruby rt { visibility: hidden; } ruby:hover rt { visibility: visible; } .card { font-family: Noto Sans CJK JP Regular; font-size: 25px; text-align: center; color: black; background: url("bg.jpg"); } .android .card { font-family: Noto Sans CJK JP Regular; font-size: 30px; text-align: center; color: black; background: url("bg.jpg"); } .frontbg { background-color: #313628; color: #ede7d9; border-radius: 7px; position: relative; left: 0; } .engdefbg { font-family: Raleway; font-style: italic; padding: 15px; margin-left: -5px; margin-top: -15px; color: #18adab; font-size: 15px; } .android .engdefbg { font-family: Raleway; font-style: italic; padding: 15px; margin-left: -15px; margin-top: -20px; color: #18adab; font-size: 10px; } .others { position: relative; top: 15px; border: 1px dotted #72c8e1; color: #18a111; font-size: 20x; width: auto; padding-top: 15px; padding-left: 20px; padding-bottom: 15px; padding-right: 20px; margin-bottom: 35px; } .android .others { position: relative; top: 10px; border: 1px dotted #72c111; color: #18ad34; font-size: 17px; width: auto; padding-top: 8px; padding-left: 15px; padding-bottom: 8px; padding-right: 15px; margin-bottom: 20px; } .sentence { font-size: 25px; margin-top: -20px; margin-bottom: 5px; } .android .sentence { font-size: 17px; margin-top: -15px; } .backbg { position: relative; top: -3px; background-color: #ede7d9; padding: 15px; padding-bottom: 15px; padding-left: 30px; padding-right: 30px; border-radius: 0px 0px 10px 10px; color: #313628; font-size: 22px; text-align: center; } .android .backbg { position: relative; top: -5px; background-color: #123; padding: 15px; padding-bottom: 15px; padding-left: 15px; padding-right: 15px; border-radius: 0px 0px 10px 10px; color: #fff; font-size: 20px; text-align: left; } .hira { font-size: 25px; line-height: 5px; padding-bottom: 40px; } .android .hira { font-size: 18px; line-height: 5px; padding-bottom: 25px; } hr { height: 2px; font-size: 10px; border: 0; background: #d5a021; } u { text-decoration: none; border-bottom: 1px dotted; } '
)




my_deck = genanki.Deck(2059400111, 'Messier Objects')

for M in messier_catalog:
    print(M)

    note = genanki.Note(model=messier_model, fields=[M['mid'], M['cons'], M['type'],M['name'], M['discoveredby'], M['description'], M['consimage'], M['objectimage']])
    my_deck.add_note(note)

my_package = genanki.Package(my_deck)

print(media)
media.append("bg.jpg")
my_package.media_files = media

my_package.write_to_file("output.apkg")
