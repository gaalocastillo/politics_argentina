# coding=utf-8
import re
import unicodedata
import sys
from pymongo import *
from datetime import datetime
from TweetParser import *
#from TopicModeling import *
#from costa_pol import *
from FileWorker import FileWorker

#client = MongoClient('localhost', 27017)
#db = client['twitter_db']

def get_document



#Limpio el texto de un documeto
def clean_document(document, language='en', context_stopwords=[]):
    if language == 'es':
        stopwords = ["rt","a","actualmente","acuerdo","adelante","ademas","además","adrede","afirmó","agregó","ahi","ahora","ahí","al","algo","alguna","algunas","alguno","algunos","algún","alli","allí","alrededor","ambos","ampleamos","antano","antaño","ante","anterior","antes","apenas","aproximadamente","aquel","aquella","aquellas","aquello","aquellos","aqui","aquél","aquélla","aquéllas","aquéllos","aquí","arriba","arribaabajo","aseguró","asi","así","atras","aun","aunque","ayer","añadió","aún","b","bajo","bastante","bien","breve","buen","buena","buenas","bueno","buenos","c","cada","casi","cerca","cierta","ciertas","cierto","ciertos","cinco","claro","comentó","como","con","conmigo","conocer","conseguimos","conseguir","considera","consideró","consigo","consigue","consiguen","consigues","contigo","contra","cosas","creo","cual","cuales","cualquier","cuando","cuanta","cuantas","cuanto","cuantos","cuatro","cuenta","cuál","cuáles","cuándo","cuánta","cuántas","cuánto","cuántos","cómo","d","da","dado","dan","dar","de","debajo","debe","deben","debido","decir","dejó","del","delante","demasiado","demás","dentro","deprisa","desde","despacio","despues","después","detras","detrás","dia","dias","dice","dicen","dicho","dieron","diferente","diferentes","dijeron","dijo","dio","donde","dos","durante","día","días","dónde","e","ejemplo","el","ella","ellas","ello","ellos","embargo","empleais","emplean","emplear","empleas","empleo","en","encima","encuentra","enfrente","enseguida","entonces","entre","era","eramos","eran","eras","eres","es","esa","esas","ese","eso","esos","esta","estaba","estaban","estado","estados","estais","estamos","estan","estar","estará","estas","este","esto","estos","estoy","estuvo","está","están","ex","excepto","existe","existen","explicó","expresó","f","fin","final","fue","fuera","fueron","fui","fuimos","g","general","gran","grandes","gueno","h","ha","haber","habia","habla","hablan","habrá","había","habían","hace","haceis","hacemos","hacen","hacer","hacerlo","haces","hacia","haciendo","hago","han","hasta","hay","haya","he","hecho","hemos","hicieron","hizo","horas","hoy","hubo","i","igual","incluso","indicó","informo","informó","intenta","intentais","intentamos","intentan","intentar","intentas","intento","ir","j","junto","k","l","la","lado","largo","las","le","lejos","les","llegó","lleva","llevar","lo","los","luego","lugar","m","mal","manera","manifestó","mas","mayor","me","mediante","medio","mejor","mencionó","menos","menudo","mi","mia","mias","mientras","mio","mios","mis","misma","mismas","mismo","mismos","modo","momento","mucha","muchas","mucho","muchos","muy","más","mí","mía","mías","mío","míos","n","nada","nadie","ni","ninguna","ningunas","ninguno","ningunos","ningún","no","nos","nosotras","nosotros","nuestra","nuestras","nuestro","nuestros","nueva","nuevas","nuevo","nuevos","nunca","o","ocho","os","otra","otras","otro","otros","p","pais","para","parece","parte","partir","pasada","pasado","paìs","peor","pero","pesar","poca","pocas","poco","pocos","podeis","podemos","poder","podria","podriais","podriamos","podrian","podrias","podrá","podrán","podría","podrían","poner","por","porque","posible","primer","primera","primero","primeros","principalmente","pronto","propia","propias","propio","propios","proximo","próximo","próximos","pudo","pueda","puede","pueden","puedo","pues","q","qeu","que","quedó","queremos","quien","quienes","quiere","quiza","quizas","quizá","quizás","quién","quiénes","qué","r","raras","realizado","realizar","realizó","repente","respecto","s","sabe","sabeis","sabemos","saben","saber","sabes","salvo","se","sea","sean","segun","segunda","segundo","según","seis","ser","sera","será","serán","sería","señaló","si","sido","siempre","siendo","siete","sigue","siguiente","sin","sino","sobre","sois","sola","solamente","solas","solo","solos","somos","son","soy","soyos","su","supuesto","sus","suya","suyas","suyo","sé","sí","sólo","t","tal","tambien","también","tampoco","tan","tanto","tarde","te","temprano","tendrá","tendrán","teneis","tenemos","tener","tenga","tengo","tenido","tenía","tercera","ti","tiempo","tiene","tienen","toda","todas","todavia","todavía","todo","todos","total","trabaja","trabajais","trabajamos","trabajan","trabajar","trabajas","trabajo","tras","trata","través","tres","tu","tus","tuvo","tuya","tuyas","tuyo","tuyos","tú","u","ultimo","un","una","unas","uno","unos","usa","usais","usamos","usan","usar","usas","uso","usted","ustedes","v","va","vais","valor","vamos","van","varias","varios","vaya","veces","ver","verdad","verdadera","verdadero","vez","vosotras","vosotros","voy","vuestra","vuestras","vuestro","vuestros","w","x","y","ya","yo","z","él","ésa","ésas","ése","ésos","ésta","éstas","éste","éstos","última","últimas","último","últimos"]
    else:
        stopwords = []
    stopwords += context_stopwords
    document = unicode(document.lower())
    decoded = unicodedata.normalize('NFKD', document)
    decoded = re.sub(r"(?:\@|https?\://)\S+", "", decoded)
    sanitized = re.sub('[^a-zA-Z ]+', '', decoded)
    resultwords = [word for word in sanitized.split() if word.lower() not in stopwords]
    cleaned_document = ' '.join(resultwords)
    return cleaned_document

def isValid(tweet):
    for url in tweet["entities"]["urls"]:
        #print url["display_url"]
        if url["display_url"] == "fllwrs.com":
            return False 
    return True

def isRetweet(tweet):
    texto = tweet['text']
    if 'retweeted_status' in tweet or (len(texto) > 4 and texto[:4] == 'RT @'):
        return True
    return False

def generate_clasified_lists(filename, leanings):
    f = open(filename, 'r')
    f.readline()
    classified_users = {}
    for leaning in leanings:
        classified_users[leaning] = []
    for line in f:
        fields = line.strip().split(',')
        user = fields[1]
        if user == 'JorgeTaiana' or user == 'MicaFerrarom':
            continue
        leaning = fields[2]
        classified_users[leaning].append(user)
    f.close()
    return classified_users


def add_to_db(classified_users):
    collection = ''
    for leaning in classified_users:
        users = classified_users[leaning]
        if leaning == 'oficialismo':
            collection = db.lideres_oficialismo
        elif leaning == 'justicialista':
            collection = db.lideres_justicialista
        elif leaning == 'frente_renovador':
            collection = db.lideres_renovador
        else:
            collection = db.lideres_izquierda
        for username in users:
            tweets = get_user_timeline(username)
            for tweet in tweets:
                if not isValid(tweet):
                    continue
                cleaned_text = clean_document(tweet['text'], 'es')
                tweet['text'] = cleaned_text
                collection.insert(tweet)

def get_user_timeline(username):
    worker = FileWorker()
    data = worker.readJSON('../../data/timelines/' + username + '.json')
    return data['tweets']

#leanings = ['oficialismo', 'justicialista', 'frente_renovador', 'frente_izquierda']
#classified_users = generate_clasified_lists('../../data/seed_users.csv', leanings)
#add_to_db(classified_users)

