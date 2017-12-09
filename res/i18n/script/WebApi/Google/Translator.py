#!python3.6
#coding:utf-8
import sys
import requests
import time
from Framework.ConstMeta import ConstMeta
class Translator(metaclass=ConstMeta):
    Url = "https://translate.google.com/translate_a/single"
    @classmethod
    def Translate(cls, sentence:str, fromLangCode='en', toLangCode='ja'):
        time.sleep(2)#サーバ負荷軽減対策
        if not isinstance(sentence, str): raise ValueError(f'引数sentenceは文字列型(str)にしてください。type(sentence)=type(sentence)')
        res = requests.get(
            url=cls.Url,
            headers=cls.__GetHeaders(),
            params=cls.__GetParameters(sentence, fromLangCode, toLangCode),
        )
        print('HTTP Code:', res.status_code)
        res.raise_for_status()
        result = res.json()
        print(result)
        print(result["sentences"][0]["trans"])
        return result["sentences"][0]["trans"]
    @classmethod
    def __GetHeaders(cls):
        return {
            "Host": "translate.google.com",
            "Accept": "*/*",
            "Cookie": "",
            "User-Agent": "GoogleTranslate/5.9.59004 (iPhone; iOS 10.2; ja; iPhone9,1)",
            "Accept-Language": "ja-jp",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
    @classmethod
    def __GetParameters(cls, sentence:str, fromLangCode='en', toLangCode='ja'):
        return {
            "client": "it",
            "dt": ["t", "rmt", "bd", "rms", "qca", "ss", "md", "ld", "ex"],
            "otf": "2",
            "dj": "1",
            "q": sentence,
            "hl": "ja",
            "ie": "UTF-8",
            "oe": "UTF-8",
            "sl": fromLangCode,
            "tl": toLangCode,
        }
        

if __name__ == '__main__':
    sentence = "My name is Ann. "
    print('翻訳前:', sentence)
    print('翻訳後:', Translator.translate(sentence, 'en', 'ja'))
