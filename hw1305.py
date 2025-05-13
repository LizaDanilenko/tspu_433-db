
import sqlite3
from typing import List, Optional

DATABASE_NAME = 'quotes.db'  #  Определим имя базы данных как константу


def get_by_tags(tags: Optional[List[str]] = None) -> List[dict]:
    """
    Получение цитат по тегам.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    if not tags:
        return []  #  Возвращаем пустой список, если теги не указаны

    #  Создаем строку плейсхолдеров для SQL-запроса
    placeholders = ', '.join(['?'] * len(tags))

    #  SQL-запрос для получения цитат, связанных с указанными тегами
    query = f"""
    SELECT quotes.id, quotes.text, authors.name AS author_name
    FROM quotes
    JOIN quote_tags ON quotes.id = quote_tags.quote_id
    JOIN tags ON quote_tags.tag_id = tags.id
    JOIN authors ON quotes.author_id = authors.id
    WHERE tags.name IN ({placeholders})
    """

    cursor.execute(query, tags)
    results = cursor.fetchall()

    conn.close()

    #  Преобразуем результаты в список словарей
    quotes = []
    for row in results:
        quotes.append({
            'id': row[0],
            'text': row[1],
            'author_name': row[2]
        })
    return quotes


def get_by_authors(authors: Optional[List[str]] = None) -> List[dict]:
    """
    Получение цитат по авторам.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    if not authors:
        return []  #  Возвращаем пустой список, если авторы не указаны

    #  Создаем строку плейсхолдеров для SQL-запроса
    placeholders = ', '.join(['?'] * len(authors))

    #  SQL-запрос для получения цитат указанных авторов
    query = f"""
    SELECT quotes.id, quotes.text, authors.name AS author_name
    FROM quotes
    JOIN authors ON quotes.author_id = authors.id
    WHERE authors.name IN ({placeholders})
    """

    cursor.execute(query, authors)
    results = cursor.fetchall()

    conn.close()

    #  Преобразуем результаты в список словарей
    quotes = []
    for row in results:
        quotes.append({
            'id': row[0],
            'text': row[1],
            'author_name': row[2]
        })
    return quotes


def get_author_count_quotes(author: str = None) -> int:
    """
    Получение количества цитат автора.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    if not author:
        return 0

    #  SQL-запрос для подсчета количества цитат указанного автора
    query = """
    SELECT COUNT(*)
    FROM quotes
    JOIN authors ON quotes.author_id = authors.id
    WHERE authors.name = ?
    """

    cursor.execute(query, (author,))
    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_top_auhtors(limit: int = 5) -> List[dict]:
    """
    Отсортированный список авторов, у которых больше всего цитат в БД.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    #  SQL-запрос для получения списка авторов, отсортированных по количеству цитат
    query = """
    SELECT authors.id, authors.name, COUNT(quotes.id) AS quote_count
    FROM authors
    LEFT JOIN quotes ON authors.id = quotes.author_id
    GROUP BY authors.id
    ORDER BY quote_count DESC
    LIMIT ?
    """

    cursor.execute(query, (limit,))
    results = cursor.fetchall()

    conn.close()

    #  Преобразуем результаты в список словарей
    authors = []
    for row in results:
        authors.append({
            'id': row[0],
            'name': row[1],
            'quote_count': row[2]
        })
    return authors


def get_top_tags(limit: int = 5) -> List[dict]:
    """
    Отсортированный список тегов по количеству упоминаний.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    #  SQL-запрос для получения списка тегов, отсортированных по количеству упоминаний
    query = """
    SELECT tags.id, tags.name, COUNT(quote_tags.quote_id) AS tag_count
    FROM tags
    LEFT JOIN quote_tags ON tags.id = quote_tags.tag_id
    GROUP BY tags.id
    ORDER BY tag_count DESC
    LIMIT ?
    """

    cursor.execute(query, (limit,))
    results = cursor.fetchall()

    conn.close()

    #  Преобразуем результаты в список словарей
    tags = []
    for row in results:
        tags.append({
            'id': row[0],
            'name': row[1],
            'tag_count': row[2]
        })
    return tags


def get_author_tags(author: str = None) -> List[dict]:
    """
    Список используемых тегов автором.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    if not author:
        return []

    #  SQL-запрос для получения списка тегов, используемых автором
    query = """
    SELECT DISTINCT tags.id, tags.name
    FROM tags
    JOIN quote_tags ON tags.id = quote_tags.tag_id
    JOIN quotes ON quote_tags.quote_id = quotes.id
    JOIN authors ON quotes.author_id = authors.id
    WHERE authors.name = ?
    """

    cursor.execute(query, (author,))
    results = cursor.fetchall()

    conn.close()

    #  Преобразуем результаты в список словарей
    tags = []
    for row in results:
        tags.append({
            'id': row[0],
            'name': row[1]
        })
    return tags

#  Пример использования
if __name__ == '__main__':
    #  Примеры тегов и авторов
    example_tags = ['love', 'life']
    example_authors = ['Albert Einstein', 'Jane Austen']
    example_author = 'Albert Einstein'

    #  Вывод результатов
    print("Цитаты по тегам 'love', 'life':", get_by_tags(example_tags))
    print("Цитаты авторов 'Albert Einstein', 'Jane Austen':", get_by_authors(example_authors))
    print("Количество цитат автора 'Albert Einstein':", get_author_count_quotes(example_author))
    print("Топ 3 автора по количеству цитат:", get_top_auhtors(limit=3))
    print("Топ 3 тега по количеству упоминаний:", get_top_tags(limit=3))
    print("Теги, используемые автором 'Albert Einstein':", get_author_tags(example_author))
