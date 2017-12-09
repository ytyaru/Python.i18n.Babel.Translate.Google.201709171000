#import os
import pathlib
import babel.messages.extract
import babel.messages.pofile
import babel.messages.mofile
from babel._compat import BytesIO
from WebApi.Google.Translator import Translator

class Maker:
    @classmethod
    def Make(cls, srcDir='../../../src/', dstDir='../locales/', domain='hello', msgidLocale='en', locales=['en','de','ja']):
        cls.MakePot(srcDir, dstDir, domain, locales)
        cls.MakePo(srcDir, dstDir, domain, msgidLocale, locales)
        cls.MakeMo(srcDir, dstDir, domain, msgidLocale, locales)

    @classmethod
    def MakePot(cls, srcDir, dstDir, domain, locales):
        # potファイルが既存なら何もしない（将来的にはpotファイル更新する予定）
#        if cls.__GetPathPot(dstDir, domain).is_file():  print('すでにpotファイルが存在します。作成中止します。'); return;
        cls.__MakeDirs(dstDir)
        for l in locales:
#            catalog = cls.__GetCatalogFromPy(srcDir, domain, l)
            catalog, pot_path = cls.__LoadPot(srcDir, dstDir, domain, l)
            buf = BytesIO()
            babel.messages.pofile.write_po(buf, catalog)
            with pot_path.open(mode='w') as f:
                f.write(buf.getvalue().decode("utf8"))
        
    @classmethod
    def MakePo(cls, srcDir, dstDir, domain, msgidLocale, locales):
        if not cls.__GetPathPot(dstDir, domain).is_file(): raise Exception('potファイルを作成してからもう一度実行してください。')
        for msgstrLocale in locales:
            catalog, po_path = cls.__LoadPo(dstDir, domain, msgstrLocale)
            for message in catalog:
                if not message.id or message.string: continue # id無し、翻訳済み、は対象外
                message.string = Translator.Translate(message.id, msgidLocale, msgstrLocale)
            buf = BytesIO()
            babel.messages.pofile.write_po(buf, catalog)
            with po_path.open(mode='w') as po:
                po.write(buf.getvalue().decode("utf8"))
        """
        for msgstrLocale in locales:
            po_path = cls.__GetPathPo(dstDir, msgstrLocale, domain)
            # poファイルが既存なら何もしない（将来的にはpoファイル更新する予定）
            if po_path.is_file():  print('すでにpoファイルが存在します。作成中止します。'); continue;
            with cls.__GetPathPot(dstDir, domain).open() as pot:
                catalog = babel.messages.pofile.read_po(pot)
                for message in catalog:
                    if not message.id: continue
#                    message.string = '翻訳後テキスト'
                    message.string = Translator.Translate(message.id, msgidLocale, msgstrLocale)
                cls.__MakeDirs(po_path.parent)
                buf = BytesIO()
                babel.messages.pofile.write_po(buf, catalog)
                with po_path.open(mode='w') as po:
                    po.write(buf.getvalue().decode("utf8"))
        """
    @classmethod
    def MakeMo(cls, srcDir, dstDir, domain, msgidLocale, locales):
        for msgstrLocale in locales:
            po_path = cls.__GetPathPo(dstDir, msgstrLocale, domain)
            if not po_path.is_file(): raise Exception(f'poファイルを作成してからもう一度実行してください。:{str(po_path)}')
            mo_path = cls.__GetPathMo(dstDir, msgstrLocale, domain)
#            # moファイルが既存なら何もしない（将来的にはmoファイル更新する予定）
#            if mo_path.is_file(): print('すでにmoファイルが存在します。作成中止します。'); return;
            with po_path.open() as po:
                catalog = babel.messages.pofile.read_po(po)
                cls.__MakeDirs(mo_path.parent)
                buf = BytesIO()
                babel.messages.mofile.write_mo(buf, catalog)
                with mo_path.open(mode='wb') as mo:
                    mo.write(buf.getvalue())

    @classmethod
    def __GetPathPot(cls, dstDir, domain):
        return pathlib.Path(dstDir).resolve() / pathlib.Path(f'{domain}.pot')
    @classmethod
    def __GetPathPo(cls, dstDir, locale, domain):
        return pathlib.Path(dstDir).resolve() / pathlib.Path(f'{locale}/LC_MESSAGES/{domain}.po')
    @classmethod
    def __GetPathMo(cls, dstDir, locale, domain):
        return pathlib.Path(dstDir).resolve() / pathlib.Path(f'{locale}/LC_MESSAGES/{domain}.mo')

    @classmethod
    def __LoadPo(cls, dstDir, domain, locale):
        if not cls.__GetPathPot(dstDir, domain).is_file(): raise Exception('potファイルを作成してからもう一度実行してください。')
        # poファイルがあればロードする
        po_path = cls.__GetPathPo(dstDir, locale, domain)
        cls.__MakeDirs(po_path.parent)
        if po_path.is_file():
            with po_path.open() as po:
                catalog = babel.messages.pofile.read_po(po)
        else: catalog = babel.messages.catalog.Catalog()
        # poにpotをマージする
        with cls.__GetPathPot(dstDir, domain).open() as pot:
            pot_catalog = babel.messages.pofile.read_po(pot)
            catalog.update(pot_catalog)
        return catalog, po_path
        """
        for message in catalog:
            if not message.id or message.string: continue # id無し、翻訳済み、は対象外
            message.string = Translator.Translate(message.id, msgidLocale, msgstrLocale)
        cls.__MakeDirs(po_path.parent)
        buf = BytesIO()
        babel.messages.pofile.write_po(buf, catalog)
        with po_path.open(mode='w') as po:
            po.write(buf.getvalue().decode("utf8"))

    
    
    
    
    
        pot_path = cls.__GetPathPot(dstDir, domain)
        if pot_path.is_file():
            with pot_path.open() as po:
                catalog = babel.messages.pofile.read_po(po)
        else: catalog = babel.messages.catalog.Catalog()
        catalog.update(cls.__GetCatalogFromPy(srcDir, domain, locale))
        return catalog
        """
    
    @classmethod
    def __LoadPot(cls, srcDir, dstDir, domain, locale):
        pot_path = cls.__GetPathPot(dstDir, domain)
        if pot_path.is_file():
            with pot_path.open() as pot:
                catalog = babel.messages.pofile.read_po(pot)
        else: catalog = babel.messages.catalog.Catalog()
        catalog.update(cls.__GetCatalogFromPy(srcDir, domain, locale))
        return catalog, pot_path
        
    @classmethod
    def __GetCatalogFromPy(cls, srcDir, domain, locale):
        prm = cls.__GetCatalogParameters(domain, locale)
        print(prm)
        catalog = babel.messages.catalog.Catalog(**prm)
        c_list = list(babel.messages.extract.extract_from_dir(dirname=srcDir))
        for c_tpl in c_list:
            catalog.add(c_tpl[2], string='', locations=[(c_t[0], c_t[1]) for c_t in c_list if c_tpl[2]==c_t[2]])
        return catalog

    @classmethod
    def __GetCatalogParameters(cls, domain, locale):
        #ファイル更新を実装したとき、creation_dateとrevision_dateを別にする
        import datetime
        import dateutil.tz
        now = datetime.datetime.now(dateutil.tz.tzlocal())
        return {'locale':locale, 'domain':domain, 'project':'test_project', 'version':'1.0', 'copyright_holder':None, 'msgid_bugs_address':None, 'creation_date':now, 'revision_date':now, 'last_translator':None, 'language_team':None}

    @classmethod
    def __MakeDirs(cls, dirpath):
        while True:
            if not pathlib.Path(dirpath).resolve().is_dir():
                pathlib.Path(dirpath).resolve().mkdir(parents=True, exist_ok=True)
                continue
            break

if __name__ == '__main__':
    Maker.Make()

