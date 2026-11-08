#!/bin/bash
cd ~/projects/_ds_app_site || exit 1
sed -i -E \
  -e 's#<a href="about.html"[^>]*>О проекте</a>##g' \
  -e 's#(<a href="community.html"[^>]*>Сообщество</a>)</nav>#\1<a href="about.html">О нас</a></nav>#' \
  $(ls *.html | grep -v '^about.html$')
echo "--- left 'О проекте':"; grep -n 'О проекте' *.html | cut -c1-150
echo "--- nav check:"; grep -c 'about.html">О нас' *.html | grep -v ':0'
