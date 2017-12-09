import babel.messages.extract

# pyファイルから翻訳対象箇所を取得する
res = babel.messages.extract.extract_from_dir(dirname='../../src/')
print(res)
for a in res:
    print(a)
print()
"""
#(filename, lineno, message, comments, context)
('main.py', 9, 'MSG000', [], None)
('sub.py', 1, 'MSG000', [], None)
('mypackage/mymodule.py', 1, 'Good Luck !', [], None)
"""

#翻訳データ(Catalog)を作成する
import babel.messages.catalog
catalog = babel.messages.catalog.Catalog(locale='ja', domain='hello')
c_list = list(babel.messages.extract.extract_from_dir(dirname='../../src/'))
for c_tpl in c_list:
    catalog.add(c_tpl[2], string='翻訳後テキスト', locations=[(c_t[0], c_t[1]) for c_t in c_list if c_tpl[2]==c_t[2]])

#poファイル書き出し
from babel._compat import BytesIO
buf = BytesIO()
import babel.messages.pofile
babel.messages.pofile.write_po(buf, catalog)
#babel.messages.pofile.write_po(buf, catalog, omit_header=True)
print(buf.getvalue().decode("utf8"))

"""
#: main.py:9 sub.py:1
msgid "MSG000"
msgstr "翻訳後テキスト"

#: mypackage/mymodule.py:1
msgid "Good Luck !"
msgstr "翻訳後テキスト"
"""
