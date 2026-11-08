#!/usr/bin/env python3
"""Подставляет общие шапку и футер (_build/header.html, _build/footer.html)
во все *.html сайта. Запуск: python3 _build/build.py"""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, '_build')
CSS_VER = '8'

# какая ссылка меню подсвечивается на странице (по умолчанию – сама страница)
CURRENT = {'index.html': './', 'guide.html': 'docs.html', 'offer.html': 'docs.html'}


def tpl(name):
    return open(os.path.join(TPL, name), encoding='utf-8').read().strip()


def mark(name, body):
    return '<!--%s-->%s<!--/%s-->' % (name, body, name)


def header_for(page, header):
    cur = CURRENT.get(page, page)
    return header.replace('<a href="%s">' % cur, '<a href="%s" aria-current="page">' % cur, 1)


def sub(s, name, tag, body):
    marked = re.compile(r'<!--%s-->.*?<!--/%s-->' % (name, name), re.S)
    if marked.search(s):
        return marked.sub(lambda m: mark(name, body), s, 1)
    plain = re.compile(r'<%s\b.*?</%s>' % (tag, tag), re.S)
    if not plain.search(s):
        raise SystemExit('нет <%s> в странице' % tag)
    return plain.sub(lambda m: mark(name, body), s, 1)


def main():
    header, footer = tpl('header.html'), tpl('footer.html')
    for p in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        page = os.path.basename(p)
        s = open(p, encoding='utf-8').read()
        n = sub(s, 'header', 'header', header_for(page, header))
        n = sub(n, 'footer', 'footer', footer)
        n = re.sub(r'(style\.css|site\.js)(\?v=\d+)?"', r'\1?v=%s"' % CSS_VER, n)
        if n != s:
            open(p, 'w', encoding='utf-8', newline='').write(n)
        print(('обновлён ' if n != s else 'без изменений ') + page)


if __name__ == '__main__':
    main()
