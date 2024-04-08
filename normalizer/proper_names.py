from enum import Enum


class ProperNames(Enum):
    IS_RESTYLING = "рестайлинг"

    BRANDS = {"li auto": "li",
              "raf": "раф",
              "samand / iran khodro / ikco": "iran khodro",
              "samsung": "renault samsung",
              "range rover": "land rover",
              "volkswagen [vw]": "volkswagen",
              "zx auto": "zx",
              "ваз (lada)": "лада",
              "заз (заз-daewoo)": "заз-daewoo",
              "заз": "заз-daewoo",
              "daewoo": "заз-daewoo",
              "москвич [иж, азлк]": "москвич",
              "иж": "москвич",
              "азлк": "москвич",
              }

    BRUSH_ATTACH_TYPES = {
        "крючок": "крючок",
        "узкая кнопка (push button 16 mm)": "кнопка, узкое, 16",
        "кнопка (push button)": "кнопка",
        "оригинальное Мицуба": "оригинальное",
        "Оригинальное MITSUBA": "оригинальное",
        "боковой штырь (side pin)": "штырь, боковое",
        "крючок с омывателем": "крючок, с омывателем",
        "усики (pinch tab)": "усики",
        "aeroclip (аэроклип), gwb061": "аэроклип",
        'короткий замок, "pin lock"': "замок, короткое",
        "крепление короткий замок (pin lock)": "замок, короткое",
        "специальное": "специальное",
        "спец. крепление": "специальное",
        "спецкрепление": "специальное",
        "специальная кнопка GWB072": "специальное, кнопка",
        'крепление "клешня" (claw)': "клешня",
        "специальная  кнопка (push button GWB072)": "специальное, кнопка",
        "широкий крючок": "крючок, широкое",
        "короткий боковой штырь (side pin)": "штырь, боковое, короткое",
        'крепление "верхний замок" (top lock)': "верхний замок",
        "кнопка (push button) с омывателем": "кнопка, с омывателем",
        "специальная кнопка (denso dntl11)": "специальное, кнопка",
        "специальное vatl51": "специальное",
        "Боковой штырь + крючок (америка)": "штырь, боковое, крючок",
        "кнопка (push button 19 mm)": "кнопка, 19",
        "крючок (сбоку)": "крючок, боковое",
        "специальное (dyna)": "специальное",
        "специальное (Dyna-Бразилия)": "специальное",
        "прямой штырь (bayonet)": "штырь, прямое",
        "специальная кнопка DNTL": "специльное, кнопка",
        'крючок "правый" руль': "крючок",
        "специальное gwb-071 (MG)": "специальное",
        "прямой штырь": "штырь, прямое",
        "специальное gwb071": "специальное",
        "американский штырь": "штырь, американский",
        "специальная кнопка": "кнопка, специальное",
        "крючок для систем с омывателем": "крючок, с омывателем",
        "кнопка ТОЛЬКО с омывателем": "кнопка, с омывателем",
        "кнопка с омывателем и подогревом": "кнопка, с омывателем, с подогревом",
        "крючок (9*3)": "крючок, 9*3",
        "оригинальное для Мэджик Вижн": "оригинальное",
        "правый или левый руль специальная кнопка (denso dntl11)": "кнопка, специальное",
        "оригинальное Мерседес (mbtl11)": "оригинальное",
        "специальная кнопка с омывателем": "кнопка, специальное, с омывателем",
        "специальный крючок": "крючок, специальное",
        "кнопка": "кнопка",
        "оригинальное кнопка Акваблейд": "кнопка, оригинаьное",
        "спец. широкий крючок": "крючок, широкое, специальное",
        "оригинальное Мерседес с форсунками омывытеля в щетках": "оригинальное, с форсунками",
        "крючок с интегрированными форсунками": "крючок, с форсунками",
        "оригинальное специальное Aquablade": "оригинальное, специальное",
        "оригинальное": "оригинальное",
        "с омывателем": "с омывателем",
        "специальный штырь": "штырь, специальное",
        "боковой штырь короткий (side pin)": "штырь, боковое, короткое",
        "специальное Рено": "специальное",
        "Широкий крючок (12 мм)": "крючок, широкое, 12",
        "усики (pinch tab) с омывателем": "усики, с омыывателем",
        "кнопка (специальная кнопка)": "кнопка, специальное",
        "крючок (правый руль)": "крючок",
        "0боковой штырь (side pin)": "штырь, боковое",
        "БОЛЬШОЙ крючок": "крючок, большое",
        "оригинальное Акваблейд": "оригинальное",
        "Оригинальное Мицуба": "оригинальное",
    }

    BODY_TYPES = {
        "пассажирский": "автобус",
        "микроавтобус": "автобус",
        "пассажир": "автобус",
        "автобус": "автобус",

        "автодом": "фургон",
        "цельнометаллический фургон": "фургон",
        "1994-2013 бортовой": "фургон",
        "2013-2023 connect, 2 поколение, сзади крышка, сзади 1 щетка": "фургон",
        "1997-2013 соболь": "фургон",
        "фургон": "фургон",

        "седан, гибрид": "седан",
        "родстер": "седан",
        "представительский седан": "седан",
        "электрический седан": "седан",
        "1960-1969 горбатый [965]": "седан",
        "1971-1994 мыльница [968]": "седан",
        "2021-2024 gran coupe[g26]": "седан",
        "1967-1972 ушастый [966]": "седан",
        "2008-2017 cедан [a] 1 поколение": "седан",
        "седан": "седан",

        "внедорожник": "джип",
        "джип/suv 5 дв.": "джип",
        "джип/suv 3 дв., гибрид": "джип",
        "джип/suv 5 дв., гибрид": "джип",
        "джип/suv 3 дв.": "джип",
        "кроосовер": "джип",
        "кросовер": "джип",
        "электрокроссовер": "джип",
        "кроссовер": "джип",
        "2018-2023 wrangler / rubicon, 3 двери": "джип",
        "2018-2023 wrangler / rubicon, 5 дверей": "джип",
        "1966-2001 волынь [969]": "джип",
        "2010-2019 x7": "джип",
        "1966-2001 геолог": "джип",
        "джип": "джип",

        "открытый кузов, гибрид": "купе",
        "открытый кузов": "купе",
        "купе, гибрид": "купе",
        "кабриолет": "купе",
        "спорткупе": "купе",
        "купе": "купе",

        "хэтчбек 3 дв., гибрид": "хетчбек",
        "хэтчбек 5 дв.": "хетчбек",
        "хэтчбек 5 дв., гибрид": "хетчбек",
        "хэтчбек 3 дв.": "хетчбек",
        "кроссхетчбек": "хетчбек",
        "кросс-хэтчбек": "хетчбек",
        "спортбек": "хетчбек",
        "кроссбек": "хетчбек",
        "кроссбэк": "хетчбек",
        "фастбек": "хетчбек",
        "хетчбзк": "хетчбек",
        "хетчбэк": "хетчбек",
        "хетчюек": "хетчбек",
        "хэтчбек": "хетчбек",
        "хетчбек": "хетчбек",
        "2008-2017 хетбчек": "хетчбек",

        "пикап, гибрид": "пикап",
        "пикап": "пикап",

        "универсал, гибрид": "универсал",
        "универрсал": "универсал",
        "универсал": "универсал",

        "лифтбек, гибрид": "лифтбек",
        "лифтбэк": "лифтбек",
        "мпортивный лифтбек": "лифтбек",
        "лифтбек": "лифтбек",
        "gran coupe": "лифтбек",

        "минивэн, гибрид": "минивэн",
        "минивен": "минивэн",
        "микровен": "минивэн",
        "кейкар": "минивэн",
        "кей-кар": "минивэн",
        "микровэн":  "минивэн",
        "минивек":  "минивэн",
        "2014-2022 courier": "минивэн",
        '2013-2023 connect, 2 поколение, распашные задние двери, сзади 2 щетки': "минивэн",
        "2013-2022 connect, 2 поколение, распашные задние двери, сзади 2 щетки": "минивэн",
        "2002-2013 connect, 1 поколение, крышка": "минивэн",
        "2000-2013 [fo]": "минивэн",
        "2002-2013 connect, 1 поколение, распашные задние двери, 2 щетки сзади": "минивэн",
        "2013-2022 connect, 2 поколение, сзади крышка, сзади 1 щетка": "минивэн",
        "минивэн": "минивэн",

        "седельный тягач": "грузовик",
        "бортовой грузовик": "грузовик",
        "бортовой грузовик, гибрид": "грузовик",
        "шасси, гибрид": "грузовик",
        "шасси": "грузовик",
        "груз / Пассажир": "грузовик",
        "груз/Пассажир": "грузовик",
        "грузовой": "грузовик",
        "грузовой, пассажирский": "грузовик",
        "2013-2017 бортовой [next]": "грузовик",
        "грузовик": "грузовик",
        # "электромобиль": "электромобиль",
    }

    MODELS = {"audi": {'a4 allroad': 'a4 allroad quattro',
                       'a6 allroad': 'a6 allroad quattro',
                       'rsq2': 'rs q2',
                       'rsq3': 'rs q3',
                       'rsq5': 'rs q5',
                       'rsq7': 'rs q7',
                       'rsq8': 'rs q8', },
              "avia": {"d": 'd-series'},
              "baic": {'u5': 'u5 plus'},
              'bmw': {'1': '1-series', 'm1 serie': 'm1', '1m': 'm1', '2': '2-series', 'm2 serie': 'm2',
                      '3': '3-series', 'm3 serie': 'm3', '3 gt': '3-series gran turismo', 'm4 serie': 'm4',
                      '4': '4-series', '5': '5-series', 'm5 serie': 'm5', '5 gt': '5-series gran turismo',
                      '6': '6-series', 'm6 serie': 'm6', '6 gt': '6-series gran turismo', '7 serie': '7-series',
                      'm7 serie': 'm7', '8': '8-series', 'm8 serie': 'm8'},
              'buick': {'la crosse': 'lacrosse', 'terazza': 'terraza'},
              'changan': {'cs85': 'cs85 coupe'},
              'citroen': {'c4 grand picasso': 'grand c4 picasso', 'c4 grand spacetourer': 'grand c4 spacetourer',
                          'spacetourier': 'spacetourer'},
              'daihatsu': {'bego': 'be-go', 'coure': 'cuore'},
              'delorean': {'dmc': 'dmc-12'},
              'faw': {'t77': 'bestune t77', 't99': 'bestune t99', 'b50': 'besturn b50', 'b70': 'besturn b70',
                      'x80': 'besturn x80'},
              'ferrari': {'612': '612 scaglietti'},
              'geely': {'geometry c': 'geometry c ge13'},
              'gmc': {'savanna': 'savana'},
              'infiniti': {'jx': 'jx35'},
              'jac': {'s2': 'refine s2'},
              'lamborghini': {'lm002': 'lm 002'},
              'land rover': {'velar': 'range rover velar'},
              'lexus': {'ct': 'ct200h', 'hs': 'hs250h'},
              'lotus': {'europa': 'europa s'},
              'mazda': {'2': 'mazda2', '3': 'mazda3', '3 mps': 'mazda3 mps', '5': 'mazda5', '6': 'mazda6',
                        '6 mps': 'mazda6 mps'},
              'mercedes-benz': {'eqa-class': 'eqa'},
              'mitsubishi': {'3000 gt': '3000gt', 'delica d2': 'delica d:2', 'delica d5': 'delica d:5'},
              'opel': {'crossland x': 'crossland'},
              'pontiac': {'aztec': 'aztek'},
              'renault samsung': {'sm-3': 'sm3', 'sm-5': 'sm5', 'sm-6': 'sm6', 'sm-7': 'sm7'},
              'skoda': {'105': '105/120/125'},
              'suzuki': {'cappucino': 'cappuccino'},
              'toyota': {'gt86': 'gt 86', 'prado [land cruiser prado]': 'land cruiser prado'},
              'volkswagen': {'up': 'up!'},
              'zotye': {'coupa (t600)': 't600 coupe'},
              'zx': {'grand tiger': 'grandtiger'},
              'газ': {'зим': '12 зим'},
              'заз-daewoo': {'vida': 'вида', 'rexton': 'сенс', 'forza': 'форца'},
              'зил': {'5301': '5301 бычок'},
              'лада': {'1111 oka': '1111 ока', '2113': '2113 самара', '2114': '2114 самара', '2115': '2115 самара',
                       'priora': 'приора'},
              'москвич': {'2126': '2126 ода', 'москвич 6': '6'},
              'тагаз': {'aquilla': 'aquila', 'road partner': 'роад партнер'},
              'уаз': {'462': 'буханка'}
              }
