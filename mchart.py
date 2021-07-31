# parsing music.yandex.ru/chart
import sys
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

def p(text, *args):
	print(text, *args, sep=' / ', end='\n')

def write_json(data, filename='mchart.json'):
	with open(filename, 'w', encoding='utf8') as f:
		json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(filename='mchart.json'):
	with open(filename, 'r', encoding='utf-8') as f:
		return json.load(f)
	return {}  

def get_html(url):
	# Not Random User-Agent	
	header = {'User-Agent':'Chrome/27.0.1453.90 Safari/537.36'}
	try:
		page = requests.get(url, headers = header, timeout = 10)
		return page.text
	except Exception as e:
		print(sys.exc_info()[1])
		return False

def get_chart(html):	
	soup = BeautifulSoup(html, 'lxml')
	teg_ = soup.find('body').find('div', {'class':'lightlist__cont'})	
	# ---
	links = []
	for index, row_ in enumerate(teg_.find_all('div', class_='d-track'), 1):
		# img
		img_ = row_.find('div', class_='entity-cover').find('img').get('src')
		# chart name autor time
		track_ = row_.find('div', class_='d-track__overflowable-column')
		track_name_ = track_.find('a', class_='d-track__title').text.strip()
		track_url_ = track_.find('a', class_='d-track__title').get('href')
		track_autors_ = [{'autor':t_.text.strip(), 'url':t_.get('href')} for t_ in track_.find('div', class_='d-track__meta').find_all('a', class_='deco-link')]
		track_time_ = row_.find('div', class_='d-track__info').text.strip()
		# append
		links.append({'number':index, 'img':img_, 'name':track_name_, 'url':track_url_, 'autors':track_autors_, 'time':track_time_})	

	return links

def main():
	start = datetime.now()
	# ---- start
	url = 'https://music.yandex.ru/chart'
	music_ = get_chart(get_html(url))
	write_json(data = music_, filename = 'mchart.json')
	for track_ in music_:		
		p(track_['number'], track_['name'], ", ".join([t_['autor'] for t_ in track_['autors']]), track_['time'])
	# ---- end
	end = datetime.now()
	print(str(end-start))


if __name__ == '__main__':
	main()