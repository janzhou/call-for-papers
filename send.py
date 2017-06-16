#!/usr/bin/python

import sys, re, os, requests, config

tag = "CFP"
unsubscribe_url = "%tag_unsubscribe_url%"

text_file = sys.argv[1]
html_file = text_file.replace("_posts/", "").replace(".md", ".html")
text = open(text_file,"r").read()
os.system("rm " + html_file)
os.system("wget https://janzhou.org/call-for-papers/" + html_file)
html = open(html_file,"r").read()

title_regex = re.compile('<title>(.*?)</title>', re.IGNORECASE|re.DOTALL)
title = "[" + tag + "] " + title_regex.search(html).group(1)

unsubscribe_url = '<p>Send from <a href="https://github.com/janzhou/call-for-papers">call-for-papers</a> list. To unsubscribe from this list, please click here: <a href="' + unsubscribe_url + '">' + unsubscribe_url + '</a></p>'
html = re.sub(r'</body></html>$', unsubscribe_url + "</body></html>", html)

requests.post(
		config.mailgun['api'],
		auth=("api", config.mailgun['key']),

		data={"from": config.mailgun['ls'], "to": config.mailgun['ls'], "o:tag": tag,
		"subject": title, "text": text, "html": html})

os.system("rm " + html_file)
