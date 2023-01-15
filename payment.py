class payment:
    count_id = 0

    def __init__(self, first_name, last_name, card_number, cvv, expiry_date, shipping_address, voucher):
        payment.count_id += 1
        self.__user_id = payment.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__card_number = card_number
        self.__cvv = cvv
        self.__expiry_date = expiry_date
        self.__shipping_address = shipping_address
        self.__voucher = voucher

    def get_user_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_card_number(self):
        return self.__card_number

    def get_cvv(self):
        return self.__cvv

    def get_expiry_date(self):
        return self.__expiry_date

    def get_shipping_address(self):
        return self.__shipping_address

    def get_voucher(self):
        return self.__voucher

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_card_number(self, card_number):
        self.__card_number = card_number

    def set_cvv(self, cvv):
        self.__cvv = cvv

    def set_expiry_date(self, expiry_date):
        self.__expiry_date = expiry_date

    def set_shipping_address(self, shipping_address):
        self.__shipping_address = shipping_address

    def set_voucher(self, voucher):
        self.__voucher = voucher