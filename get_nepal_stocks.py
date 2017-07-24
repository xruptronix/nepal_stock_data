from bs4 import BeautifulSoup
import requests
import csv

url = "http://www.nepalstock.com/main/todays_price/index/{}/stock-name/asc/"

def get_page_info():
    url = "http://www.nepalstock.com/main/todays_price"
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    number_of_page = int(soup.find("div",{"class":"pager"}).find_all("a")[-1].text.strip())
    date = soup.find(id="date")
    file_name = date.text.strip().encode('utf-8')
    return number_of_page,file_name

def main():
    page_info = get_page_info()
    number_pages = page_info[0]
    with open("{}.csv".format(page_info[1]),"w+") as f:
        writer = csv.writer(f)
        writer.writerow(["Traded Company","No. of Transactions","Max Price","Min Price","Closing Price","Traded Shares","Amount","Previous Closing","Difference Rs."])
        for url_index in range(1,number_pages+1):
            new_url = url.format(url_index)
            r = requests.get(new_url)
            soup = BeautifulSoup(r.text,"html.parser")
            table_rows = soup.find("table",{"class":"table"}).find_all("tr")[2:-4]
            for row in table_rows:
                tds = row.find_all("td")
                traded_company = tds[1].text.strip().encode('utf-8')
                no_of_transaction = tds[2].text.strip().encode('utf-8')
                max_price = tds[3].text.strip().encode('utf-8')
                min_price = tds[4].text.strip().encode('utf-8')
                closing_price = tds[5].text.strip().encode('utf-8')
                traded_shares = tds[6].text.strip().encode('utf-8')
                amount = tds[7].text.strip().encode('utf-8')
                previous_closing = tds[8].text.strip().encode('utf-8')
                difference = tds[9].text.strip().encode('utf-8')
                writer.writerow([traded_company,no_of_transaction,max_price,min_price,closing_price,traded_shares,amount,previous_closing,difference])


if __name__ == "__main__":
    main()
