#! /usr/bin/bash
rm locale/template.pot
xgettext -o locale/template.pot core/start_page/__init__.py lib/occ_page.py
python3 locale/generate_setting_localization_files.py setting-schema.json locale/template.pot