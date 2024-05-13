import re
import csv


def process_phonebook(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        phonebook_dict = {}

        for row in reader:
            fullname = row[:2]
            lastname, firstname, *surname = " ".join(fullname).split(" ")
            surname = " ".join(surname)
            phone = row[5]
            phone = re.sub(r'[^0-9]', '', phone)
            if len(phone) == 11:
                phone = re.sub(r'(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})', r'+7(\2)\3-\4-\5', phone)
            elif len(phone) == 10:
                phone = re.sub(r'(\d{3})(\d{3})(\d{2})(\d{2})', r'+7(\1)\2-\3-\4', phone)
            if 'доб.' in row[5]:
                main_phone, extension = row[5].split('доб.')
                main_phone = re.sub(r'[^0-9]', '', main_phone)
                if len(main_phone) == 11:
                    main_phone = re.sub(r'(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})', r'+7(\2)\3-\4-\5', main_phone)
                elif len(main_phone) == 10:
                    main_phone = re.sub(r'(\d{3})(\d{3})(\d{2})(\d{2})', r'+7(\1)\2-\3-\4', main_phone)
                phone = f"{main_phone} доб.{extension.strip()}"

            key = (lastname, firstname)
            if key in phonebook_dict:
                phonebook_dict[key][5] += ', ' + phone
                if row[6]:
                    phonebook_dict[key][6] = row[6]
            else:
                phonebook_dict[key] = [lastname, firstname, surname] + row[3:5] + [phone] + row[6:]

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["lastname", "firstname", "surname", "organization", "position", "phone", "email"])
        for value in phonebook_dict.values():
            writer.writerow(value)


process_phonebook('phonebook_raw.csv', 'phonebook_processed.csv')
