import requests
from bs4 import BeautifulSoup


def search_item():
    search = input('Search Item: ')
    search = search.replace(' ', '+')
    url = f'https://www.hificorp.co.za/catalogsearch/result/?q={search.strip()}'
    return url


def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_data(soup):
    data = soup.find_all('li', class_='item product product-item')
    return data


def parse_data(data):
    products = []
    for item in data:
        name = item.find('a', class_='product-item-link')
        image_url = item.find('img', class_='product-image-photo')
        price = item.find('span', class_='price')

        if name and image_url and price:
            name = name.text
            price = price.text
            image_url = image_url['src']

            products.append({
                'name': name,
                'price': price,
                'image': image_url
            })
    return products


url = search_item()
soup = get_soup(url)
data = get_data(soup)
products = parse_data(data)

for product in products:
    print(f"Name: {product['name']}\nPrice: {product['price']}\nImage URL: {product['image']}\n")
