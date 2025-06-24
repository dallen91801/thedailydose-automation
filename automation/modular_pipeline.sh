#!/bin/bash
cd /volume1/docker/thedailydose/automation

/volume1/@appstore/Python3.9/usr/bin/python3 step1_summarize_articles.py
/volume1/@appstore/Python3.9/usr/bin/python3 step2_tag_emotions.py
/volume1/@appstore/Python3.9/usr/bin/python3 step3_generate_markdown.py
/volume1/@appstore/Python3.9/usr/bin/python3 step4_generate_html.py
/volume1/@appstore/Python3.9/usr/bin/python3 step5_cleanup_archives.py
