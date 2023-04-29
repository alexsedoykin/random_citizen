import sqlite3
from random import randint, choice
from datetime import timedelta, datetime

con = sqlite3.connect('rnd_bd.db', check_same_thread=False)
cursor = con.cursor()


class RandomName:

    def __init__(self, gen=randint(0, 1)):
        self.gen = gen
        self.first_name = self._set_first_name(gen)
        self.middle_name = self._set_middle_name(gen)
        self.last_name = self._set_last_name(gen)
        self.date = self._set_date()
        self.email = self._set_email(self.first_name, self.last_name, self.date)
        self.address = self._set_address()
        self.telephone = self._set_telephone(self.address)
        self.card_number = self._set_card_number()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def _set_first_name(self, gen) -> str:  # выбираем имя
        if gen == 1:
            m_name = cursor.execute("SELECT name FROM male_names ORDER BY RANDOM() LIMIT 1")
            return m_name.fetchone()[0]
        else:
            f_name = cursor.execute("SELECT name FROM female_names ORDER BY RANDOM() LIMIT 1")
            return f_name.fetchone()[0]

    def _set_middle_name(self, gen) -> str:  # выбираем отчество
        if gen == 1:
            male_middle_name = cursor.execute("SELECT male_mid_name FROM middle_names ORDER BY RANDOM() LIMIT 1")
            return male_middle_name.fetchone()[0]
        else:
            female_middle_name = cursor.execute("SELECT female_mid_name FROM middle_names ORDER BY RANDOM() LIMIT 1")
            return female_middle_name.fetchone()[0]

    def _set_last_name(self, gen) -> str:  # выбираем фамилию
        if gen == 1:
            male_last_name = cursor.execute("SELECT male_surname FROM surnames ORDER BY RANDOM() LIMIT 1")
            return male_last_name.fetchone()[0]
        else:
            female_last_name = cursor.execute("SELECT female_surname FROM surnames ORDER BY RANDOM() LIMIT 1")
            return female_last_name.fetchone()[0]

    def _set_date(self) -> str:  # выбираем дату рождения
        d = randint(1, 18900)
        start_day = datetime(1954, 12, 31)
        return datetime.strftime((start_day + timedelta(days=d)), '%d.%m.%Y')

    def _set_email(self, first_name, last_name, date):  # генерируем e-mail
        domain = cursor.execute("SELECT domain FROM mail_domains ORDER BY RANDOM() LIMIT 1")  # домен
        lucky_numbers = ('555', '777', '888', '007', '43', '23', '5', '7')
        tr_name = self._translit(first_name)
        tr_surname = self._translit(last_name)
        xx_year = date[-2:]
        xxxx_year = date[-4:]
        xxxx_date = date[:5].replace('.', '')
        tpl = (
            f'{tr_name}.{tr_surname}',
            f'{tr_surname}_{tr_name}',
            f'{tr_name}{tr_surname}{xx_year}',
            f'{tr_surname}{choice(lucky_numbers)}',
            f'{tr_surname}{xx_year}',
            f'{tr_surname}{xxxx_year}',
            f'{tr_surname}{xx_year}',
            f'{tr_surname}{xxxx_year}',
            f'{tr_surname}{xxxx_date}',
        )
        return choice(tpl) + domain.fetchone()[0]

    def _set_address(self):  # генерируем адрес
        coin = randint(0, 1)  # кидаем монетку, узнаем будет ли в адресе у дома корпус
        city = cursor.execute("SELECT city FROM ru_cities ORDER BY RANDOM() LIMIT 1")
        t_city = city.fetchone()[0]
        street = cursor.execute("SELECT street FROM ru_streets ORDER BY RANDOM() LIMIT 1")
        t_street = street.fetchone()[0]
        if coin:
            return f'Россия, г.{t_city}, {t_street}, д.{randint(1, 89)}, кв.{randint(1, 320)}'
        else:
            return f'Россия, г.{t_city}, {t_street}, д.{randint(1, 89)}, к.{randint(1, 5)}, кв.{randint(1, 320)}'

    def _set_telephone(self, address):  # генирируем номер телефона
        code = cursor.execute("SELECT code FROM opsos_codes ORDER BY RANDOM() LIMIT 1")  # выбираем код оператора
        n = str(randint(1000000, 9999999))
        return f'+7 {code.fetchone()[0]} {n[:3]}-{n[3:5]}-{n[5:]}'

    def _set_card_number(self):  # генерируем номер банковской карты
        bin_codes = ('427901', '427631', '427901', '437773', '521324', '548601', '415428')  # выбираем BIN-код банка
        cardnumber = choice(bin_codes)
        for i in range(9):
            cardnumber += str(randint(0, 9))
        cardnumber += self._luhn_checksum(cardnumber)  # проверяем номер карты по алгоритму Луна и добавляем контрольную цифру
        return f'{cardnumber[:4]} {cardnumber[4:8]} {cardnumber[8:12]} {cardnumber[12:]}'

    def _luhn_checksum(self, card_number):  # проверка по алгоритму Луна
        dig = [int(i) for i in card_number]
        odd_digits = dig[-1::-2]
        even_digits = dig[-2::-2]
        checksum = sum(odd_digits)
        for digit in even_digits:
            checksum += sum([int(d) for d in str(digit * 2)])
        return str((10 - checksum % 10) % 10)

    def _translit(self, text):  # транслит для генерации e-mail
        dict = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
            'э': 'e', 'ю': 'yu', 'я': 'ya'
        }
        res = ''
        for i in text.lower():
            if i in dict:
                res += dict[i]
            else:
                res += i
        return res