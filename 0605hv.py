import requests
from bs4 import BeautifulSoup
import csv
import sqlite3

# ====================== 1. Создание структуры БД ==============================

def create_database(): # функция для создания бд 
    conn = sqlite3.connect('quotes.db') # соединяем с бдшкой
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            about_url TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quote_tags (
            quote_id INTEGER,
            tag_id INTEGER,
            PRIMARY KEY (quote_id, tag_id),
            FOREIGN KEY (quote_id) REFERENCES quotes (id),
            FOREIGN KEY (tag_id) REFERENCES tags (id)
        )
    ''')

    conn.commit()# cохр изм
    conn.close()# закрываем
    print("База данных создана.")

# =========== 2. Парсер и сохранение в CSV =============

def parse_quotes(num_quotes=1000): # функ с парамтром
    base_url = "https://quotes.toscrape.com/"
    all_quotes = []  # 2 списка
    csv_data = [] 
    page = 1 # перебор страниц сайта
    quotes_count = 0 # найденные цитаты

    while quotes_count < num_quotes:
        url = f"{base_url}page/{page}/" if page > 1 else base_url 
        response = requests.get(url) # запр
        soup = BeautifulSoup(response.content, 'html.parser')
        quotes = soup.find_all('div', class_='quote') # ищем дивы
        print(f"Парсинг страницы {page}...")
        if not quotes:
            print("Больше цитат не найдено. Завершение парсинга.")
            break

        for quote in quotes: # перебираем список 
            text = quote.find('span', class_='text').get_text() # ищем и извлекаем text
            author_name = quote.find('small', class_='author').get_text() #author
            author_about_url = base_url + quote.find('a')['href'] # a href
            tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')] #tag

            all_quotes.append({ #словарик
                'text': text,
                'author_name': author_name,
                'author_about_url': author_about_url,
                'tags': tags
            })
            csv_data.append([text, author_name, author_about_url, ','.join(tags)]) # подготовка строки для CSV

            quotes_count += 1
            if quotes_count >= num_quotes:
                break

        page += 1

    #Запись в CSV
    with open('quotes.csv', 'w', newline='', encoding='utf-8') as csvfile: #откр, созд,предотвр пустые
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['text', 'author_name', 'author_about_url', 'tags']) #Заголовок
        csvwriter.writerows(csv_data) #Запись данных
    print(f"Сохранено {quotes_count} цитат в quotes.csv")
    return all_quotes

# === 3. Загрузка из CSV в БД ===

def load_csv_to_db(csv_filename='quotes.csv'):
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()

    with open(csv_filename, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  #пропускаем заголовок

        for row in csvreader:
            text, author_name, author_about_url, tags_str = row
            tags = tags_str.split(',')

            # Находим или создаем автора
            cursor.execute("SELECT id FROM authors WHERE name = ?", (author_name,))
            author_data = cursor.fetchone()
            if author_data is None:
                cursor.execute("INSERT INTO authors (name, about_url) VALUES (?, ?)", (author_name, author_about_url))
                author_id = cursor.lastrowid
            else:
                author_id = author_data[0]

            # Создаем цитату
            cursor.execute("INSERT INTO quotes (text, author_id) VALUES (?, ?)", (text, author_id))
            quote_id = cursor.lastrowid

            # Находим или создаем теги и связываем их с цитатой
            for tag in tags:
                cursor.execute("SELECT id FROM tags WHERE name = ?", (tag,))
                tag_data = cursor.fetchone()
                if tag_data is None:
                    cursor.execute("INSERT INTO tags (name) VALUES (?)", (tag,))
                    tag_id = cursor.lastrowid
                else:
                    tag_id = tag_data[0]

                cursor.execute("INSERT INTO quote_tags (quote_id, tag_id) VALUES (?, ?)", (quote_id, tag_id))

    conn.commit()
    conn.close()
    print("Данные успешно загружены из CSV в базу данных.")


# === Main ===
if __name__ == "__main__":
    create_database()
    quotes_data = parse_quotes(num_quotes=1000)
    load_csv_to_db()
