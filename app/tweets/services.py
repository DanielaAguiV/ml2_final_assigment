import emoji
import re
# Para tratamientos de texto
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import spacy
from spellchecker import SpellChecker

from tweets.models import Tweet


class TweetTransformations:
    """"Clase que lleva a cabo todas las transformaciones iniciales del tweet"""
    
    @staticmethod
    def remove_punctuation_space(df):
        PUNCTUATION = re.compile("""(\-)|(\,)|(\..)|(\...)|(\....)|(\.....)|(\......)|(\.......)""")

        return " ".join([PUNCTUATION.sub(" ", word.lower()) for word in df.split()])

    # Eliminamos signos de puntuación sin reemplazo
    @staticmethod
    def remove_punctuation(df):
        PUNCTUATION = re.compile("""(\.)|(\;)|(\:)|(\!)|(\?)|(\¡)|(\¿)| \
        (\")|(\()|(\))|(\[)|(\])|(\d+)|(\/)|(\“)|(\”)|(\')|(\-)|(\")|(\*)""")

        return " ".join([PUNCTUATION.sub("", word.lower()) for word in df.split()])

    # Corregimos abreviaciones
    @staticmethod
    def fix_abbr(x):
        if type(x) == list:
            words = x
        elif type(x) == str:
            words = x.split()
        else:
            raise TypeError('El formato no es válido, debe ser lista o str')

        abbrevs = {'d': 'de',
                   'x': 'por',
                   'xa': 'para',
                   'as': 'has',
                   'q': 'que',
                   'k': 'que',
                   'dl': 'del',
                   'xq': 'porqué',
                   'dr': 'doctor',
                   'dra': 'doctora',
                   'sr': 'señor',
                   'sra': 'señora',
                   'm': 'me'}
        return " ".join([abbrevs[word] if word in abbrevs.keys() else word for word in words])

    # Sustituimos links por {link}
    @staticmethod
    def remove_links(df):
        return " ".join(['{link}' if ('http') in word else word for word in df.split()])

    # Eliminamos vocales repetidas

    @staticmethod
    def remove_repeated_vocals(df):

        list_new_word = []

        for word in df.split(): #separamos en palabras
            new_word = []
            pos = 0

            for letra in word: #separamos cada palabra en letras
                if pos>0:
                    if letra in ('a', 'e', 'i', 'o', 'u') and letra == new_word[pos-1]:
                        None
                    else:
                        new_word.append(letra)
                        pos +=1
                else:
                    new_word.append(letra)

                    pos += 1
            else:
                list_new_word.append("".join(new_word))

        return " ".join(list_new_word)

    # Normalizamos risas 'jajaja', 'jejeje', 'jojojo'

    @staticmethod
    def normalize_laughts(df):

        list_new_words = []
        for word in df.split(): #separamos en palabras
            count = 0
            vocals_dicc = {'a': 0, 'e': 0, 'i': 0, 'o':0, 'u':0}

            for letra in word:
                if letra == 'j':
                    count+=1
                if letra in vocals_dicc.keys():
                    vocals_dicc[letra] += 1
            else:
                if count>3:
                    dicc_risa = {'a': 'jaja', 'e': 'jeje', 'i': 'jiji', 'o': 'jojo', 'u': 'juju'}
                    risa_type = max(vocals_dicc, key= lambda x: vocals_dicc[x]) #Indica si es a,e,i,o,u
                    list_new_words.append(dicc_risa[risa_type])
                else:
                    list_new_words.append(word)

        return " ".join(list_new_words)

    # Sustituimos hashtag por {hash}
    @staticmethod
    def remove_hashtags(df):
        return " ".join(['{hash}' if word.startswith('#') else word for word in df.split()])

    # Sustituimos menciones por {mencion}
    @staticmethod
    def remove_mentions(df):
        return " ".join(['{menc}' if word.startswith('“@') or word.startswith('@') else word for word in df.split()])

    # Función para identificar los 'emojis' tradicionales

    @staticmethod
    def transform_icons(df):
        word_list = []
        pos_emojis = [':)', ':D', ':))', ':)))', 'xD', 'xd', 'XD']
        neg_emojis = [':(', ":'(", '>:(', ':,(', ":(("]
        for word in df.split():
            if word in neg_emojis:
                word = '{emoji_neg}'
                word_list.append(word)
            elif word in pos_emojis:
                word = '{emoji_pos}'
                word_list.append(word)
            elif ':O' in word:
                word = '{emoji_neu}'
                word_list.append(word)
            else:
                word_list.append(word)
        return " ".join(word_list)

    # Separamos emojis que vengan juntos
    @staticmethod
    def sep_emojis(df):
        words_list = []
        for token in df.split():
            new_word = []
            for letra in token:
                if letra in emoji.UNICODE_EMOJI['es']:
                    words_list.append(letra)
                else:
                    new_word.append(letra)
            else:
                words_list.append("".join(new_word))

        return (" ".join(word for word in words_list if word != ''))
    


    @staticmethod
    def remove_stopwords(df):
        nltk.download('stopwords')
        spanish_stopwords = stopwords.words('spanish')
        non_stopwords = ['no', 'ni', 'poco', 'mucho', 'nada', 'muchos', 'muy', 'nosotros',
                         'nosotras', 'vosotros', 'vosotras', 'ellos', 'ellas', 'ella', 'él', 'tu', 'tú', 'yo',
                         'pero', 'hasta', 'contra', 'por']
        spanish_stopwords = [word for word in stopwords.words('spanish') if word not in non_stopwords]
        return " ".join([word for word in df.split() if word not in spanish_stopwords])
    
# Función para stemizar
    @staticmethod
    def stem(df):
        stemmer = SnowballStemmer('spanish')
        return " ".join([stemmer.stem(word) for word in df.split()])
    
    # Función para lematizar



    # Definimos función
    @staticmethod
    def lemmatizer(df):
        # Creamos el objeto
        spacy.prefer_gpu() # or spacy.require_gpu()
        nlp = spacy.load("es_core_news_md")
        word_list = []
        doc = nlp(df)
        for tok in doc:
            if str(tok) == 'menc':
                  word_list.append('{menc}')
            elif str(tok) == 'hash':
                  word_list.append('{hash}')
            elif str(tok) == 'link':
                  word_list.append('{link}')
            elif str(tok) == 'emoji_pos':
                  word_list.append('{emoji_pos}')
            elif str(tok) == 'emoji_neu':
                  word_list.append('{emoji_neu}')
            elif str(tok) == 'emoji_neg':
                  word_list.append('{emoji_neg}')
            elif str(tok) == 'eur':
                  word_list.append('{eur}')
            else:
                word_list.append(tok.lemma_.lower())

        return " ".join([word for word in word_list if (word != '{') and (word!='}')])  


    @staticmethod
    def correcting_words(df):
        spell = SpellChecker(language='es', distance=1)
        misspelled = spell.unknown(df.split())
        return " ".join(filter(None,[spell.correction(word) if word in misspelled else word for word in df.split()]))
    
    @staticmethod
    def remove_eur(df):
        wlist = ['{eur}' if ('€' in word) | ('euro' in word) | ('$' in word) else word for word in df.split()]
        return " ".join(wlist)
    
    @staticmethod
    def transform_tweets(tweet: Tweet, mode='lemma') -> Tweet:
        
        df = tweet.value
        df = TweetTransformations.remove_links(df)
        df = TweetTransformations.remove_punctuation_space(df)
        df = TweetTransformations.remove_mentions(df)    
        df = TweetTransformations.remove_hashtags(df)
        df = TweetTransformations.remove_eur(df)
        df = TweetTransformations.transform_icons(df)
        df = TweetTransformations.sep_emojis(df)
   #     df = transform_emoji(df)
        df = TweetTransformations.normalize_laughts(df)
        df = TweetTransformations.remove_punctuation(df)
        df = TweetTransformations.remove_repeated_vocals(df)
        df = TweetTransformations.correcting_words(df)
        df = TweetTransformations.fix_abbr(df)
        df = TweetTransformations.remove_stopwords(df)
        if mode=='lemma':
            df = TweetTransformations.lemmatizer(df)
        elif mode=='stem':
            df = TweetTransformations.stem(df)
        else:
            raise TypeError('Invalid mode. Must be "lemma" or "stem"') 
        
        lemma_tweet = Tweet(df)
        return lemma_tweet