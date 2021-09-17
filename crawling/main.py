from selenium import webdriver
from bs4 import BeautifulSoup

browser = webdriver.Chrome("/Users/yongcho/Downloads/chromedriver") #'./chromedriver'
# browser.maximize_window() #창 최대화
url = 'https://www.flashscore.co.kr/soccer/england/premier-league/archive/'
browser.get(url)

#지정한 위치로 스크롤 하기
browser.execute_script("window.scrollTo(0,300)") #300크기만큼 스크롤 내림

#화면 가장 아래로 스크롤 내리기
# browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
#아카이브 페이지에서 시즌 태그 중에 첫번쨰 불러오기
year1 = 2020
year2 = 2021
for i in range(0,4):
    year1 -= i
    year2 -= i
    browser.find_element_by_link_text(f"프리미어리그 {year1}/{year2}").click()

    #시즌 페이지에서 결과창 불러오기
    browser.execute_script("window.scrollTo(0,300)") #300크기만큼 스크롤 내림
    browser.find_element_by_link_text("결과").click()


    #결과 창에서 id 찾기
    browser.execute_script("window.scrollTo(0,300)") #300크기만큼 스크롤 내림
    soup = BeautifulSoup(browser.page_source,'lxml')
    arr = soup.find_all('div', attrs={'class':'event__match event__match--static event__match--twoLine'})

    #id 수정 및 id 배열 만들기
    id_arr = []
    for ar in arr:
        ar['id'] = ar['id'][4:]
        id_arr.append(ar['id'])


    #새로운 창에 대해 url 얻기
    browser2 = webdriver.Chrome("/Users/yongcho/Downloads/chromedriver") #'./chromedriver'
    url_for_statistic = f"https://www.flashscore.co.kr/match/{id_arr[0]}/#match-summary/match-statistics/0"
    browser2.get(url_for_statistic)
    soup2 = BeautifulSoup(browser2.page_source, 'lxml')


    #팀 이름 가져오기
    match = soup2.find_all("a",attrs={"class":"participantName___3lRDM1i overflow___cyQxKBr"})
    name_list = []
    for m in match:
        m_strip = str(m['href']).split('/')
        name_list.append(m_strip[2])
    home_name = name_list[0]
    away_name = name_list[1]


    #점수로 승, 무, 패 결정하기
    score = soup2.find("div",attrs={"class":"wrapper___3rU3Jah"})
    score_list = str(score).split("<span>") #두 번째 데이터 첫 번째 문자, 세 번째 데이터 첫 번째 문자가 점수
    home_score = int(score_list[1][0])
    away_score = int(score_list[2][0])
    if home_score > away_score:
        Win_Draw_Lose_HomeTeam = 2
    elif home_score == away_score:
        Win_Draw_Lose_HomeTeam = 1
    else:
        Win_Draw_Lose_HomeTeam = 0


    #통계 데이터 가져오기
    category = soup2.find_all("div",attrs={"class":"categoryName___3Keq6yi"})
    home_data = soup2.find_all("div", attrs={"class":"homeValue___Al8xBea"})
    away_data = soup2.find_all("div", attrs={"class":"awayValue___SXUUfSH"})
    home_data_score = []
    away_data_score = []
    category_name = []
    for h in home_data:
        home_data_score.append(h.get_text())
    for a in away_data:
        away_data_score.append(a.get_text())
    for c in category:
        category_name.append(c.get_text())

    for i in range(len(category_name)):
        print(f"홈팀 {category_name[i]} : {home_data_score[i]}")
        print(f"어웨이팀 {category_name[i]} : {away_data_score[i]}")



