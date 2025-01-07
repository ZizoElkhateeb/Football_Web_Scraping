import requests
from bs4 import BeautifulSoup
import csv


date = input('Enter the date in the format (mm/dd/yyyy): ')


page = requests.get(f'https://www.yallakora.com/match-center/?date={date}')
page.encoding = 'utf-8' 

def main(page):
    src = page.content 
    soup = BeautifulSoup(src, 'lxml') 
    matches_details =[]

    championships = soup.find_all('div', {'class': 'matchCard'}) 
     
    
    def get_match_info(championships):

        
        championship_tittle = championships.find('div', {'class': 'title'}).find('h2').text.strip()
        
        
        all_mathches = championships.find('div', {'class': 'ul'}).find_all('div' , {'class' :['item finish liItem' , 'item now liItem' ,'item future liItem']}) # list of all matches in the championship ex: [الاهلي - الزمالك]
        number_of_matches = len(all_mathches)

        
        
        for i in range(number_of_matches):
            

            team_a = all_mathches[i].find('div', {'class': 'teams teamA'}).find('p').text.strip()
            team_b = all_mathches[i].find('div', {'class': 'teams teamB'}).find('p').text.strip()

            

            match_score = all_mathches[i].find('div', {'class': 'MResult'}).find_all('span' , {'class' : 'score'})
            score = f"'{match_score[0].text.strip()} - {match_score[1].text.strip()}"


            

            time = all_mathches[i].find('div', {'class': 'MResult'}).find('span' , {'class' : 'time'}).text.strip()

            
            matches_details.append({
                'Championship': championship_tittle,
                'Team_a': team_a,
                'Team_b': team_b,
                'Time': time,
                'Score': score
                
            })

            '''print(f'Championship: {championship_tittle}')
            print(f'Team A: {team_a} vs Team B: {team_b} : {time} : {score}')'''
            

    
    for championship_titles in championships:
        get_match_info(championship_titles)


    
    keays = matches_details[0].keys()
    with open('G:/Random_Projects/Web_Scrapping/Match.csv','w',newline='',encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, keays)
        writer.writeheader()
        writer.writerows(matches_details)
        print('Done')

main(page)