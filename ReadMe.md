# このソフトウェアについて

PythonコードをGoogle翻訳で国際化する（pot,po,moファイル既存時は更新する）。

Babelでpyファイルからpot,po,moファイルを作成する。Google翻訳APIで翻訳したテキストを使う。

`./res/i18n/script/run.py`

msgidを原文として翻訳する。

# 前回

* [Python.i18n.Babel.201709161639](https://github.com/ytyaru/Python.i18n.Babel.201709161639)

## 実行結果

`./src/main.py`に以下の翻訳対象を追加した。
```sh
print(_('Nice to meet you.'))
```

pot, po, moを更新する。上記の文章を翻訳したファイルが作成される。2回目以降は既存なので翻訳APIは実行されない。（ただしファイルは必ず上書きされる）

```sh
$ python run.py 
{'locale': 'en', 'domain': 'hello', 'project': 'test_project', 'version': '1.0', 'copyright_holder': None, 'msgid_bugs_address': None, 'creation_date': datetime.datetime(2017, 9, 17, 10, 55, 24, 816677, tzinfo=tzlocal()), 'revision_date': datetime.datetime(2017, 9, 17, 10, 55, 24, 816677, tzinfo=tzlocal()), 'last_translator': None, 'language_team': None}
{'locale': 'de', 'domain': 'hello', 'project': 'test_project', 'version': '1.0', 'copyright_holder': None, 'msgid_bugs_address': None, 'creation_date': datetime.datetime(2017, 9, 17, 10, 55, 25, 571257, tzinfo=tzlocal()), 'revision_date': datetime.datetime(2017, 9, 17, 10, 55, 25, 571257, tzinfo=tzlocal()), 'last_translator': None, 'language_team': None}
{'locale': 'ja', 'domain': 'hello', 'project': 'test_project', 'version': '1.0', 'copyright_holder': None, 'msgid_bugs_address': None, 'creation_date': datetime.datetime(2017, 9, 17, 10, 55, 25, 587415, tzinfo=tzlocal()), 'revision_date': datetime.datetime(2017, 9, 17, 10, 55, 25, 587415, tzinfo=tzlocal()), 'last_translator': None, 'language_team': None}
HTTP Code: 200
{'sentences': [{'trans': 'Nice to meet you.', 'orig': 'Nice to meet you.', 'backend': 0}], 'src': 'en', 'confidence': 0.35836697, 'ld_result': {'srclangs': ['en'], 'srclangs_confidences': [0.35836697], 'extended_srclangs': ['en']}}
Nice to meet you.
HTTP Code: 200
{'sentences': [{'trans': 'Schön dich zu treffen.', 'orig': 'Nice to meet you.', 'backend': 1}], 'dict': [{'pos': '語句', 'terms': ['Schön, Sie kennen zu lernen.'], 'entry': [{'word': 'Schön, Sie kennen zu lernen.', 'reverse_translation': ['Nice to meet you.']}], 'base_form': 'Nice to meet you.', 'pos_enum': 10}], 'src': 'en', 'confidence': 0.35836697, 'ld_result': {'srclangs': ['en'], 'srclangs_confidences': [0.35836697], 'extended_srclangs': ['en']}}
Schön dich zu treffen.
HTTP Code: 200
{'sentences': [{'trans': 'はじめまして。', 'orig': 'Nice to meet you.', 'backend': 1}, {'translit': 'Hajimemashite.'}], 'dict': [{'pos': '感嘆詞', 'terms': ['始めまして'], 'entry': [{'word': '始めまして', 'reverse_translation': ['Nice to meet you!']}], 'base_form': 'Nice to meet you!', 'pos_enum': 9}], 'src': 'en', 'confidence': 0.35836697, 'ld_result': {'srclangs': ['en'], 'srclangs_confidences': [0.35836697], 'extended_srclangs': ['en']}}
はじめまして。
```

既存の翻訳済みテキストに関しては翻訳APIが実行されていない。

`main.py`を実行すると、翻訳されたテキストが表示される。
```
$ python main.py 
こんにちは世界 ！！
はじめまして。
...
```

# 課題

* pot, po, moファイルの更新判定を実装する（現在は新規作成のみ）
    * 更新されていない（変更、削除、追加の箇所が一つもない）
        * ファイルを上書きしない
    * 変更されている
        * ファイルを上書きする
        * リビジョンを上げる（1.0.0.567。<Major>.<Minor>.<Bug>.<Build>）
* 翻訳リクエスト回数を減らす工夫をする
    * 同一
    * 原文言語と翻訳言語が同一のときは翻訳しないようにする（原文をそのままmessage.stringに代入する）
    * 1回のリクエストに10件分(1000文字分)の文章を入力するなど
* 翻訳リクエスト部分の抽象化
* 異なる翻訳APIの実装

必要性があるか微妙な課題は以下。

* 言語コード文字列の妥当性確認
* 翻訳APIごとにおけるドメイン名の自動分割('domain_google', 'domain_microsoft'等)

## 解決済み課題

* 新規作成のとき同一msgidがあると重複回数分だけAPI発行してしまう
    * 一旦potファイルで1件にしてしまい、その後poファイルにしてから翻訳させることで1度のAPI発行にできた
* pot, po, moファイルの更新を実装する
    * 新規追加、変更、の箇所は新たに翻訳処理を行う
        * 各ファイルを上書きする

# 開発環境

* Linux Mint 17.3 MATE 32bit
* [pyenv](https://github.com/pylangstudy/201705/blob/master/27/Python%E5%AD%A6%E7%BF%92%E7%92%B0%E5%A2%83%E3%82%92%E7%94%A8%E6%84%8F%E3%81%99%E3%82%8B.md) 1.0.10
    * Python 3.6.1
        * [Babel](https://github.com/python-babel/babel) 2.5.1
* Google翻訳API
        
# ライセンス

* https://sites.google.com/site/michinobumaeda/programming/pythonconst

Library|License|Copyright
-------|-------|---------
[Babel](https://github.com/python-babel/babel)|[BSD 3-clause](https://github.com/python-babel/babel/blob/master/LICENSE)|[Copyright (C) 2013 by the Babel Team, see AUTHORS for more information.](https://github.com/python-babel/babel/blob/master/LICENSE)
