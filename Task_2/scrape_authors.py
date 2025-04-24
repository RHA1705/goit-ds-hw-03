import requests
import json
from bs4 import BeautifulSoup


def delete_duplicates(data):
    new_data = set(data)
    return new_data


def find_authors_links(page_url):
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to retrieve page: {page_url}")
        return [], None

    soup = BeautifulSoup(response.text, 'lxml')
    author_links = []

    quotes = soup.find_all('div', class_='quote')
    for quote in quotes:
        author_link = quote.find('small', class_='author').find_next_sibling('a')['href']
        author_links.append(author_link)

    author_links_not_repeat = set(author_links)

    # Перевірка чи є кнопка
    base_url = "http://quotes.toscrape.com"
    next_button = soup.find('li', class_='next')
    next_page_url = None
    if next_button:
        next_relative_url = next_button.find('a')['href']
        next_page_url = f"{base_url}{next_relative_url}"  # Збираємо урлу для перехода
    return author_links_not_repeat, next_page_url


def scrap_authors(authors_links):
    authors_data = []
    base_url = "http://quotes.toscrape.com"
    for author_l in authors_links:
        new_url = f'{base_url}{author_l}'  # Збираємо  повний URL автора
        new_response = requests.get(new_url)
        if new_response.status_code != 200:
            print(f"Failed to retrieve author page: {new_url}")
            continue
        new_soup = BeautifulSoup(new_response.text, 'lxml')
        author_details = new_soup.find('div', class_='author-details')
        if author_details:
            name = author_details.find('h3', class_='author-title').get_text(strip=True)
            born_date = author_details.find('span', class_='author-born-date').get_text(strip=True)
            born_location = author_details.find('span', class_='author-born-location').get_text(strip=True)
            description = author_details.find('div', class_='author-description').get_text(strip=True)
            authors_data.append({
                'fullname': name,
                'born_date': born_date,
                'born_location': born_location,
                'description': description
            })
    return authors_data


def main():
    base_url = "http://quotes.toscrape.com"
    current_url = base_url
    all_authors = []

    while current_url:
        print(f"Scraping {current_url}...")
        authors, next_page_url = find_authors_links(current_url)
        all_authors.extend(authors)
        current_url = next_page_url  # Переходимо на наступну сторінку

    all_authors = list(set(all_authors))

    print(f"Total authors collected: {len(all_authors)}")

    authors_data = scrap_authors(all_authors)

    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(authors_data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
