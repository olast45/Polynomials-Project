# Wielomiany na bazie list powiązanych pojedynczo i posortowanych.
# Jeden węzeł listy reprezentuje jeden wyraz wielomianu i przechowuje atrybuty 'degree' oraz 'coefficient'.
# Węzły są sortowane względem atrybutu 'degree'


# Klasa reprezentująca pojedynczy wyraz wielomianu
class Node:
    def __init__(self, coefficient, degree):  # KONSTRUKTOR WEZLA
        self.coefficient = coefficient
        self.degree = degree
        self.next = None

    def __eq__(self, other):  # POROWNYWANIE WEZLOW
        if isinstance(other, Node):
            if other.coefficient == self.coefficient and other.degree == self.degree:
                return True
        return False


# Klasa reprezentujaca wielomian
class Polynomial:

    def __init__(self):  # KONSTRUKTOR
        self.head = None

    def __str__(self):  # WYSWIETLANIE
        if self.is_empty():
            return "0"
        nodes = []
        current_node = self.head
        while current_node is not None:
            if current_node.coefficient < 0:
                if current_node.degree == 0:
                    node = f"({current_node.coefficient})"
                else:
                    node = f"({current_node.coefficient}x^{current_node.degree})"
            elif current_node.coefficient > 0:
                if current_node.degree == 0:
                    node = f"{current_node.coefficient}"
                else:
                    node = f"{current_node.coefficient}x^{current_node.degree}"

            nodes.append(node)
            current_node = current_node.next
        return " + ".join(nodes)

    def size(self):  # ILOSC WYRAZOW WIELOMIANU
        if self.is_empty():
            return 0
        result = 0
        current_node = self.head
        while current_node is not None:
            result += 1
            current_node = current_node.next
        return result

    def __eq__(self, other):  # POROWNYWANIE WIELOMIANOW
        if isinstance(other, Polynomial):
            if self.size() != other.size():
                return False
            self_node = self.head
            other_node = other.head
            while self_node is not None and other_node is not None:
                if (self_node.degree != other_node.degree) or (self_node.coefficient != other_node.coefficient):
                    return False
                self_node = self_node.next
                other_node = other_node.next
        return True

    def __ne__(self, other):
        return not self == other

    def is_empty(self):
        return self.head is None

    def delete_node(self, node):  # USUWANIE KONKRETNEGO WEZLA
        if self.is_empty():
            raise ValueError("Polynomial doesn't have any terms!")

        current_node = self.head
        # Wezel do usuniecia jest na poczatku
        if node == current_node:
            self.head = current_node.next

        while current_node.next is not None:
            if current_node.next == node:
                # Jezeli wezel do usuniecia nie jest na koncu
                if current_node.next.next is not None:
                    current_node.next = current_node.next.next
                else:
                    current_node.next = None
            current_node = current_node.next

    def insert_node(self, node):  # WSTAWIANIE KONKRETNEGO WEZLA WIELOMIANU
        if node.coefficient == 0:  # Nie dodajemy 0
            return

        if self.is_empty():  # Przypadek dla pustego wielomianu
            self.head = node

        else:
            current_node = self.head
            if current_node.degree < node.degree:  # Ustawiamy nowa "glowe", bo na poczatku wielomianu trzymamy najwieksza wartosc
                node.next = current_node
                self.head = node
            else:
                while current_node.next is not None and current_node.next.degree > node.degree:
                    current_node = current_node.next
                if current_node.degree == node.degree:
                    current_node.coefficient += node.coefficient
                elif current_node.next is not None and current_node.next.degree == node.degree:
                    current_node.next.coefficient += node.coefficient
                else:
                    if current_node.next is not None:
                        node.next = current_node.next
                        current_node.next = node
                    if current_node.next is None:
                        current_node.next = node

    @staticmethod
    def from_list(_list):
        result = Polynomial()
        for pair in _list:
            coefficient, degree = pair
            result.insert_node(Node(coefficient, degree))
        return result

    def check_if_zero(self):
        current_node = self.head
        while current_node is not None:
            if current_node.coefficient == 0:
                self.delete_node(current_node)
            current_node = current_node.next

    def polynomial_degree(self):  # STOPIEN WIELOMIANU
        return self.head.degree

    def horner(self, x_value):  # ALGORYTM OBLICZANIA WARTOSCI WIELOMIANU W DANYM PUNKCIE
        if self.is_empty():
            return 0
        current_node = self.head
        max_degree = current_node.degree

        current_node = self.head
        result = current_node.coefficient
        for i in reversed(range(0, max_degree)):
            if current_node.next is not None and current_node.next.degree == i:
                result = (result * x_value) + current_node.next.coefficient
                current_node = current_node.next
            else:
                result = (result * x_value)
        return result

    def __add__(self, other):  # DODAWANIE WIELOMIANOW
        result = Polynomial()
        current_node = self.head
        while current_node is not None:
            result.insert_node(Node(current_node.coefficient, current_node.degree))
            current_node = current_node.next
        current_node = other.head
        while current_node is not None:
            result.insert_node(Node(current_node.coefficient, current_node.degree))
            current_node = current_node.next
        result.check_if_zero()
        return result

    def __sub__(self, other):  # ODEJMOWANIE WIELOMIANOW
        result = Polynomial()
        current_node = self.head
        while current_node is not None:
            result.insert_node(Node(current_node.coefficient, current_node.degree))
            current_node = current_node.next
        current_node = other.head
        while current_node is not None:
            result.insert_node(Node(-current_node.coefficient, current_node.degree))
            current_node = current_node.next
        result.check_if_zero()
        return result

    def __mul__(self, other):  # MNOZENIE WIELOMIANOW
        result = Polynomial()
        current_node = self.head
        while current_node is not None:
            other_node = other.head  # ustawiamy w tym miejscu, zeby kazdy z wyrazow pierwszego wielomianu byl mnozony
            while other_node is not None:
                coefficient = current_node.coefficient * other_node.coefficient
                degree = current_node.degree + other_node.degree
                result.insert_node(Node(coefficient, degree))
                other_node = other_node.next
            current_node = current_node.next

        result.check_if_zero()
        return result

    def __divmod__(self, divisor):  # DZIELENIE WIELOMIANOW Z RESZTA
        quotient = Polynomial()
        dividend = self

        if divisor.is_empty():
            raise ValueError("Division by zero!")

        if divisor.polynomial_degree() > dividend.polynomial_degree():
            raise ValueError("The degree of the dividend is less than the degree of the divisor!")

        else:
            while dividend.head.degree >= divisor.head.degree:
                # nie musimy sprawdzac czy divisor.head.coefficient jest = 0, bo 0 nie dodajemy
                coefficient = dividend.head.coefficient / divisor.head.coefficient
                degree = dividend.head.degree - divisor.head.degree
                quotient.insert_node(Node(coefficient, degree))

                term = Polynomial()
                term.insert_node(Node(coefficient, degree))
                term = (term * divisor)

                dividend = (dividend - term)

            remainder = dividend

            quotient.check_if_zero()
            remainder.check_if_zero()
            return quotient, remainder


