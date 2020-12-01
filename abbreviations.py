import csv
from web_scraper import web_scraper

abb = web_scraper()
count = 0
with open('../mli_train_v1.csv', 'r') as file1, open('Abb/mli_train_v1.csv', 'w', newline='') as file2:
    reader = csv.reader(file1, delimiter=',')
    writer = csv.writer(file2, delimiter=',')

    for row in reader:
        for key, value in abb.items():
            if ';' not in value:
                if key in row[0].split() or key in row[3].split():
                    count += 1
                    replaced = row[0].replace(key, value)
                    row[0] = replaced
                    replaced = row[3].replace(key, value)
                    row[3] = replaced
        writer.writerow(row)

file1.close()
file2.close()
print(count)

