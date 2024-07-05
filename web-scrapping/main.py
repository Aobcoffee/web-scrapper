import requests
from bs4 import BeautifulSoup
import json
from login import login
import account


def show_results(soup, company_name: str) -> None:

    form = soup.find('form', {'id': 'cart_quantity', 'name': 'cart_quantity'})
    table = form.find('table')

    products = table.find_all("tr")[2]

    all_data=[]
    for row in products.find_all('tr')[2::]:  # skip the first two rows
        cols = row.find_all('td')
        if len(cols) > 2:
            article_number = cols[5].find('a')["name"]
            product_name = cols[6].find('a').text.strip()  # extract name from 7th column
            price = cols[7].find('div').text.strip()  # extract price from 8th column
            
            selected_data = {
                "article_number": article_number,
                "product_name": product_name,
                "price": price,
            }

            all_data.append(selected_data)


    # save json file
    with open(f'{company_name}.json', 'w') as f:
        json.dump(all_data, f, indent=4)
        print(f"Successfully saved data to {company_name}.json")
        


if __name__ == "__main__":

    
    soup = (login(account.pier7))
    show_results(soup, company_name="pier7")