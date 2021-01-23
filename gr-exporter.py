import csv
import sys
from datetime import datetime
import re


def flatten_reference(match):
    _, _, title, author, *_ = match.group(0).split("|")
    return f"_{title}_ by {author}"


def write_book_info(year_file, title, author, finished_at, rating, my_review):
    year_file.write(f"\n\n## {title}\n")
    year_file.write(f"by {author}\n\n")
    year_file.write(f"Finished on {finished_at}\n")
    if rating:
        year_file.write(f"\nAndrew's Rating: {'⭐️' * int(rating)}\n")
    if my_review:
        my_review = re.sub("\[(.*)\]", flatten_reference, my_review)
        year_file.write("\n\n")
        year_file.write(my_review.replace("<br/>", "\n"))

        year_file.write("\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("grexporter <file> <dump_dir>")
        exit(-1)
    csv_file = sys.argv[1]
    location = sys.argv[2]

    current_year = None
    year_file = None

    first = True
    seen = set()
    with open(csv_file) as csv_file:
        reader = csv.reader(csv_file, quotechar='"')
        for row in reader:
            if first:
                first = False
                continue
            _, title, author, _, _, isbn, isbn13, rating, _, _, _, pages, _, _, read_on, _, _, _, _, my_review, *rest = (
                row
            )
            if read_on:
                finished_at_datetime = datetime.strptime(read_on, "%Y/%m/%d")
                if current_year != finished_at_datetime.year:
                    current_year = finished_at_datetime.year
                    if current_year <= 2013:
                        continue
                    if year_file:
                        year_file.close()
                    file_name = (
                        f"{location}/{current_year}-01-01-books-{current_year}.md"
                    )
                    year_file = open(file_name, "a" if current_year in seen else "w")
                    #                    print(f"{title} => {file_name}")
                    if current_year not in seen:
                        seen.add(current_year)
                        year_file.write(
                            f"""---
title: 'Books I Read in {current_year}'
date: {current_year}-01-01 00:00:11
featured_image: '/images/demo/demo-square.jpg' 
tags: books
---
                        """
                        )
                write_book_info(year_file, title, author, read_on, rating, my_review)
        if year_file:
            year_file.close()
