import os, pymupdf
from time import perf_counter

start_time = perf_counter()


def create_directory(path, enable_logs):
    try:
        os.makedirs(path)
        if enable_logs:
            print(f'Директория {path} успешно создана.')
    except FileExistsError:
        if enable_logs:
            print(f'Директория {path} уже существует.')
    except Exception as e:
        print(f'Ошибка при создании директории {path}: {str(e)}')


def sort_dates(dates):
    days = []
    for item in dates:
        try:
            day_str = item.split()[0]
            day_int = int(day_str)
            days.append((day_int, item))
        except ValueError:  # occurs if encountering non integer values
            continue

    return [item[1] for item in sorted(days)]


def merge_PDFs(path, year, month):
    output_PDF = pymupdf.open()
    PDFs_to_merge = [f for f in os.listdir(path) if f.endswith('.pdf')]

    for pdf in sort_dates(PDFs_to_merge):
        pdf_path = os.path.join(path, pdf)
        page_count = len(pymupdf.open(pdf_path))
        # Append all pages of the current PDF to the new document
        output_PDF.insert_pdf(pymupdf.open(pdf_path), from_page=0, to_page=page_count - 1)

    output_PDF.save(f"{os.path.join(path, f'{year}-{month}-all')}.pdf")


# years_folder_path = r'/Users/ivan/Desktop/PROGRAMMING/Python/projects/magazines/convert_to_pdf/test_years'  # Вечерняя Москва
# output_folder_path = r'/Users/ivan/Desktop/PROGRAMMING/Python/projects/magazines/convert_to_pdf/output_folder'  # Вечерняя Москва PDF

output_folder_path = r'/Volumes/WD_new_5Tb/газеты/web/Вечерняя Москва PDF'
years_folder_path = r'/Volumes/WD_new_5Tb/газеты/web/Вечерняя Москва'

enable_creation_logs = True

start_year = 1957
end_year = 1967  # 1967
# [start_year, end_year]

needed_years = [i for i in range(start_year, end_year + 1)]
print(needed_years)

years = os.listdir(years_folder_path)
years.remove('.DS_Store')
years = sorted(map(int, years))
for year in years:
    if year in needed_years:
        output_year_path = os.path.join(output_folder_path, str(year))
        create_directory(output_year_path, enable_creation_logs)

        months_path = os.path.join(years_folder_path, str(year))

        months = os.listdir(months_path)
        months.remove('.DS_Store')
        months = sorted(map(int, months))
        for month in months:
            output_month_path = os.path.join(output_year_path, str(month))
            create_directory(output_month_path, enable_creation_logs)

            dates_path = os.path.join(months_path, str(month))

            for date in sort_dates(os.listdir(dates_path)):
                doc_PDF = pymupdf.open()  # output PDF
                sheets_path = os.path.join(dates_path, date)  # where my files are
                sheets_list = os.listdir(sheets_path)  # list of them

                if sheets_list:

                    for i, f in enumerate(sorted(sheets_list)):
                        if f != '.DS_Store':
                            img = pymupdf.open(os.path.join(sheets_path, f))  # open pic as document
                            rect = img[0].rect  # pic dimension
                            pdfbytes = img.convert_to_pdf()  # make a PDF stream
                            img.close()
                            imgPDF = pymupdf.open("pdf", pdfbytes)  # open stream as PDF
                            page = doc_PDF.new_page(width=rect.width,
                                                    height=rect.height)  # new page with ... pic dimension
                            page.show_pdf_page(rect, imgPDF, 0)  # image fills the page

                    output_path = os.path.join(output_month_path, date)  # ! does not include .pdf

                    doc_PDF.save(f"{output_path}.pdf")

                else:
                    print(f'{sheets_path} EMPTY')

            merge_PDFs(output_month_path, year, month)

    print()
    year_end_time = perf_counter()
    total_time = round(year_end_time - start_time, 3)
    print(f'YEAR {year} DONE; total time taken {total_time} s')
    print()

print()
end_time = perf_counter()
total_time = end_time - start_time
if total_time < 1:
    print("Execution time: < 1 second")
else:
    print(f"Execution time: {total_time} seconds")
