import time
import requests
import os
from bs4 import BeautifulSoup

start_time = time.time()


def check_inputs(isOK=False):
    if not isOK:
        if year not in range(1934, 1967 + 1):
            print("Неправильный год")
            return False
        if month not in range(1, 12 + 1):
            print("Неправильный месяц")
            return False
        return True
    else:
        return True


def create_directory(path):
    try:
        os.makedirs(path)
        print(f'Директория {path} успешно создана.')
    except FileExistsError:
        pass
        # print(f'Директория {output_path} уже существует.')
    except Exception as e:
        print(f'Ошибка при создании директории {path}: {str(e)}')


def download_ph(u, path_n_name):
    response = requests.get(u)
    if response.status_code == 200:
        with open(path_n_name, 'wb') as file:
            file.write(response.content)
        # print('Фотография успешно скачана.')
    else:
        print('Не удалось скачать фотографию.')


# year = 1948
# month = №5

url_ = "https://electro.nekrasovka.ru"
url_list_clean = []
books = []

if __name__ == "__main__":

    if check_inputs(True):

        for year in range(1960, 1949 + 1, -1):  # 1967 + 1

            for month in range(1, 12 + 1):

                for site_page in range(1, 6):

                    url = url_ + f"/editions/1/{year}/{month}?page={site_page}"  # month page
                    html_text = requests.get(url).text
                    soup = BeautifulSoup(html_text, 'lxml')
                    a_tags = soup.find_all('a', attrs={'href': lambda href: href and '/books/' in href})
                    books = []

                    for url in a_tags:
                        books.append(url['href'])

                    p_tags_all = soup.find_all('p')
                    p_tags = []
                    dates = []

                    for p_tag in p_tags_all:
                        if p_tag.text.startswith("Вечерняя"):
                            p_tags.append(p_tag.text)

                    if len(p_tags) == 0:
                        continue  # Пропускаем итерацию, если страницы не существует

                    p_tags.pop(0)

                    for text in p_tags:
                        dates.append(text.split(",")[-1][1:])  # Добавление дат журналов

                    for i, book_number in enumerate(books):
                        book_num = book_number[7:]
                        name_of_directory = f"/Volumes/WDElements5Tb/web/Вечерняя Москва/{year}/{month}/{dates[i]}"
                        create_directory(name_of_directory)

                        for book_page in range(1, 4 + 1):
                            url_to_download = f"https://api.{url_[8:]}/api{book_number}/pages/{book_page}/img/original"
                            name_and_path = f"{name_of_directory}/{p_tags[i]}-{book_page}.jpeg"
                            download_ph(url_to_download, name_and_path)
                            print(url_to_download)
                        print("Book done.")

                    print("Переход на следующую страницу.")

    else:
        print("Wrong input")

end_time = time.time()
total_time = end_time - start_time
if total_time < 1:
    print("Execution time: < 1 second")
else:
    print(f"Execution time: {total_time} seconds")
