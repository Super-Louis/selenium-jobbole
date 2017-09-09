from selenium import webdriver
from bs4 import BeautifulSoup, element
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
from urllib.request import urlretrieve

options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"')
driver = webdriver.Chrome(chrome_options=options)

def login():
	driver.maximize_window()
	driver.get(r'http://www.jobbole.com/login/?redirect=http%3A%2F%2Fdate.jobbole.com%2F')
	user = driver.find_element_by_id('jb_user_login')
	password = driver.find_element_by_id('jb_user_pass')
	user.send_keys('super_super')
	password.send_keys('1992liuchao4235')
	login = driver.find_element_by_id('jb_user_login_btn')
	login.click()
	time.sleep(5)
	#如果提示无法定位，可能是页面还未加载出来，建议加延时
	city = driver.find_element_by_xpath("//div[@class='col-xs-12 col-sm-4']/div/div[2]/div/ul/li/div/span[7]/a")
	city.click()
	html = driver.page_source
	final_html = switch_page(html)
	return final_html

def switch_page(html):
	soup = BeautifulSoup(html, 'lxml')
	ad = soup.find('li', class_='media sponsored')
	votes=[]
	notes=[]
	urls=[]
	for li in ad.next_siblings:
		if li != '\n' and type(li) != element.Comment: #注意换行符和注释！！
			votes.append(int(li.a.span.text))
			notes.append(li.div.h3.a.text)
			urls.append(li.div.h3.a['href'])
	_index = votes.index(max(votes))
	pre_user = driver.find_element_by_link_text(notes[(_index-1)])#为避免顶边栏挡住应点击的位置，需将串口切换至点击位置的上方
	driver.execute_script('arguments[0].scrollIntoView();', pre_user)
	user = driver.find_element_by_link_text(notes[_index])
	user.click()
	#将driver定位至跳转的新页面
	driver.switch_to_window(driver.window_handles[1])
	html = driver.page_source
	return html

def get_pics():
	html = login()
	soup = BeautifulSoup(html, 'lxml')
	imgs = soup.find('div', class_='p-entry').find_all('img')
	index = 0
	for img in imgs:
		index += 1
		img_url = img.get('src')
		path = str(index) + '.jpg'
		urlretrieve(img_url, path)
		im = Image.open(path)
		im.show()

if __name__=='__main__':
	get_pics()



