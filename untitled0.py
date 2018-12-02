import requests
from bs4 import BeautifulSoup
from time import sleep

movie_dict = {}


def crawling_movie_data(max_page=0, recent_review_num=0):
    i = 0
    go = True
    next_recent_review_num = 0
    while go:
        i += 1
        
        if max_page != 0 and i > max_page:
            break
        
        url = "https://movie.naver.com/movie/point/af/list.nhn?&page="+str(i)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,features="lxml")
        list = soup.find("tbody").find_all("tr")
        
        #temp = list[0].find(class_="title").find("br")
        #print(temp)
        for n in range(0, len(list)) :
            temp = list[n].find_all(class_="num")
            
            if not next_recent_review_num: 
                next_recent_review_num = int(temp[0].text)
            
            if recent_review_num != 0 and int(temp[0].text) == recent_review_num :
                go = False
                break
            
            print("=================================")
            print("리뷰 번호 :\t", temp[0].text)
            title = list[n].find(class_="movie").text
            print("영화 제목 :\t", title)
            point = list[n].find(class_="point").text
            print("영화 평점 :\t", point)
            #review = list[n].find(class_="title").text
            #review = review.replace(title, '')
            #review = review.replace("신고",'')
            #review = review.strip()
            #print("영화 리뷰 :\t", review)
            #id_date = temp[1].text
            #print("아이디 :\t", id_date[:-8])
            #print("날짜 :\t", id_date[-8:])
            if title not in movie_dict:
                movie_dict[title] = {"count":1, "total_score":int(point)}
            else:
                movie_dict[title]["count"] += 1
                movie_dict[title]["total_score"] += int(point)
    
    return next_recent_review_num
    
        

recent_review_num = crawling_movie_data(10, 0)

count_set = set()
for key in movie_dict:
    count_set.add(int(movie_dict[key]["count"]))
    
count_list = list(count_set)
count_set = set(count_list[-5:])


movie_rank = {}
for i in count_set:
    movie_rank[i] = []
    
for key in movie_dict:
    if movie_dict[key]["count"] in count_set:
        movie_rank[movie_dict[key]["count"]].append(key)

print("\n\n=================================")        
for i in reversed(sorted(list(movie_rank.keys()))):
    movie_list = movie_rank[i]
    for j in movie_list:
        print(j + ' :\t' + str(i) + '\t/\t' + str(round(movie_dict[j]["total_score"]/i,1)))
    


c = 0
while c < 20:
    recent_review_num = crawling_movie_data(0, recent_review_num)
    sleep(5)
    c += 1









