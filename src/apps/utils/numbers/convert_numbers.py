class PersianNumberConverter:
    PERSIAN_DIGITS = '۰۱۲۳۴۵۶۷۸۹'
    ENGLISH_DIGITS = '0123456789'
    TRANSLATION_TABLE = str.maketrans(ENGLISH_DIGITS, PERSIAN_DIGITS)
    REVERSE_TRANSLATION_TABLE = str.maketrans(PERSIAN_DIGITS, ENGLISH_DIGITS)

    @staticmethod
    def to_persian(value, humanize=False):
        """
            Convert English numbers to Persian numerals.
        """
        try:
            num_str = str(value)

            if humanize:
                num_str = num_str.replace(',', '').replace(' ', '')
                num_str = f'{int(num_str):,}'

            return num_str.translate(PersianNumberConverter.TRANSLATION_TABLE)
        except (ValueError, TypeError):
            return str(value)

    @staticmethod
    def to_english(value):
        """
            Convert Persian numbers to English numerals.
        """
        try:
            return str(value).translate(PersianNumberConverter.REVERSE_TRANSLATION_TABLE)
        except (ValueError, TypeError):
            return str(value)
