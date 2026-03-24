class Product():
    def __init__(self, name, price):
        self.name = str(name)
        self.price = float(price)

    def __str__(self):
        return self.name + " : " + str(self.price)

    def get_information(self):
        return "Product: " + self.name + " | " + "Price: " + str(self.price)

class Client():
    def __init__(self, name, email):
        self.name = str(name)
        self.email = str(email)
        self.scart = []

    def add_to_cart(self, product):
        self.scart.append(product)

    def compute_total(self):
        total = 0
        for i in self.scart:
            total += i.price
        return total

class VIPclient(Client):
    def __init__(self, name, email, discount):
        super().__init__(name, email)
        self.discount = float(discount)

    def calculate_discount(self):
        total = super().compute_total()
        percentage = 1 - (self.discount / 100)
        return total * percentage


tv = Product("Television", "500")
console = Product("Console", "700")
pc = Product("Computer", "1000")

alice = VIPclient("Alice", "aliceterron10@gmail.com", "30")
marcos = Client("Marcos", "mruiz@gmail.com")

alice_prod = [tv, console]
for i in alice_prod:
    alice.add_to_cart(i)

marcos_prod = [tv, pc]
for i in marcos_prod:
    marcos.add_to_cart(i)

print("Customer: Alice(VIP)")
print("Total to pay:", alice.calculate_discount())
print("Customer: Marcos")
print("Total to pay:", marcos.compute_total())