import enum


class Discount:
    def __init__(self, group_name, cost, unit, users):
        self.group_name = group_name
        self.cost = cost
        self.unit = unit
        self.users = users


class Person:
    def __init__(self, name, last_name, userID):
        self.name = name
        self.last_name = last_name
        self.userID = userID

    def __eq__(self, other):
        return self.userID == other.userID


def calculate_m(point1, point2):
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]
    return (y1 - y2) / (x1 - x2)


class Type_Product(enum.Enum):
    shirt = 'shirt'
    pants = 'pants'
    hat = 'hat'
    shoes = 'shoes'


class MarkUp:
    def __init__(self, lower_cost, upper_cost, unit, product_type, lower_count):
        self.lower_cost = lower_cost
        self.upper_cost = upper_cost
        self.unit = unit
        self.product_type = product_type
        self.lower_count = lower_count


class Product:
    def __init__(self, type, name, price, unit, commission_group):
        self.type = type
        self.name = name
        self.price = price
        self.unit = unit
        self.commission_group = commission_group


class Company:
    persons = []
    products = []
    markUp = []
    discounts = []

    def __init__(self, name):
        self.name = name

    @staticmethod
    def add_markUp(cls, markUp):
        Company.markUp.append(markUp)

    @staticmethod
    def add_person(cls, person):
        Company.persons.append(person)

    @staticmethod
    def add_product(cls, product):
        Company.products.append(product)

    @staticmethod
    def add_discount(cls, discount):
        Company.discounts.append(discount)

    def calculate_percent(self, product, count):
        MainMarkUp = next(filter(lambda markup: markup.product_type == product.type, Company.markUp))
        percent = 0
        if count == 1:
            percent = MainMarkUp.upper_cost
        elif count >= MainMarkUp.lower_count:
            percent = MainMarkUp.lower_cost
        elif count > 1:
            m = calculate_m((1, MainMarkUp.upper_cost),
                            (MainMarkUp.lower_count, MainMarkUp.lower_cost + 1))
            percent = MainMarkUp.upper_cost + (float(m) * float(count))
        return percent

    def calculate_product_price(self, productType, count, userID):
        MainPerson = next(filter(lambda person: person.userID == userID, Company.persons))
        result = {}
        first, family = MainPerson.name, MainPerson.last_name
        if len(first) != 0 and len(family) != 0:
            result['username'] = {'first_name': first, 'last_name': family}
        else:
            result['username'] = ''
        MainProduct = next(filter(lambda product: product.type == productType, Company.products))
        total_price = MainProduct.price * count
        result['product_name'] = MainProduct.name
        total_price = total_price + total_price * self.calculate_percent(productType, count) / 100
        result['total_price'] = total_price
        groups = []
        maxDiscount = []
        for item in Company.products:
            if productType == item.type:
                groups.extend(item.commission_group)
        for item in Company.discounts:
            if item.group_name in groups and userID in item.users:
                cost = item.cost
                unit = item.unit
                if unit == 'percent':
                    discount = total_price * count / 100
                else:
                    discount = total_price - cost
                maxDiscount.append(discount)
        result['discount'] = max(maxDiscount)
        result['total_with_commission'] = total_price - result['discount']
        print(result)
