#!/bin/sh

FULL_TEST="https://sueszli.notion.site/NotionSnapshot-Test-5ab361d19688436fb22f319e84b53a07"
NOTION_TEMPLATES="https://sueszli.notion.site/NotionSnapshot-Test-full-templates-cfbba0e4a3244e84b3242b137c2f640e"
TINY_TEST="https://sueszli.notion.site/NotionSnapshot-Test-tiny-page-4dfa05657f774b45993542da4a8530c2"
PDF_TEST="https://sueszli.notion.site/NotionSnapshot-Test-pdf-ede3b5b97b104ab59d508f3645c0a513"

python3 notionsnapshot -d -c $FULL_TEST > ./log.txt
