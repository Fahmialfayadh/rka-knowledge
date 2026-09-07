#write csv file
import csv
header = ['Negara', 'Benua']
data = [
    ['Indonesia', 'Asia'],
    ['Brazil', 'South America'],
    ['Germany', 'Europe']
]
    
with open('countries.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header)  # write header
    writer.writerows(data)   # write data rows
    