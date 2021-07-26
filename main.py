import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

search = ''
page = 2
data = []


def search_item():
    global search
    search = input('Search Item: ')
    search = search.replace(' ', '+')
    url = f'https://www.hificorp.co.za/catalogsearch/result/?q={search.strip()}'
    return url


def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_data(soup):
    global data
    global page
    flag = False
    data.append(soup.find_all('li', class_='item product product-item'))
    pagination_data = soup.find('a', class_='action next')
    not_pagination_data = soup.find('a', class_='action disabled next')

    if pagination_data:
        flag = True
        if not_pagination_data:
            flag = False
    while flag:
        print(f'fetching page {page} data...')
        url = f'https://www.hificorp.co.za/catalogsearch/result/index/?p={page}&q={search.strip()}'
        soup = get_soup(url)
        data.append(soup.find_all('li', class_='item product product-item'))
        # pagination_data = soup.find('a', class_='action  next')
        not_pagination_data = soup.find('a', class_='action disabled next')
        if not_pagination_data:
            flag = False
        page += 1
    return data


def parse_data(items):
    products = []
    for item_list in items:
        for item in item_list:
            name = item.find('a', class_='product-item-link').text
            image_url = item.find('img', class_='product-image-photo')['src']
            price = item.find('span', class_='price').text
            product_url = item.find('a', class_='product-item-link')['href']

            products.append({
                'name': name.strip(),
                'price': price,
                'image': image_url.strip(),
                'product_url': product_url
            })
    return products


def main():
    global search
    url = search_item()
    excel = Workbook()
    sheet = excel.active
    sheet.title = f"HiFi Corp {search.replace('+', ' ')} list"
    sheet.append(['Product Name', 'Price', 'Image URL', 'Product URL'])

    soup = get_soup(url)
    items = get_data(soup)
    products = parse_data(items)

    for product in products:
        # print(f"Name: {product['name']}"
        #       f"\nPrice: {product['price']}"
        #       f"\nImage URL: {product['image']}"
        #       f"\nProduct URL: {product['product_url']}\n")
        sheet.append([product['name'], product['price'], product['image'], product['product_url']])

    print(f'{sheet.title} saved.')
    excel.save(f'{sheet.title}.xlsx')


if __name__ == '__main__':
    main()
