import random

def luhn_algorithm(bin_code, count):
    card_numbers = []
    while len(card_numbers) < count:
        number = [int(x) for x in str(bin_code)]
        while len(number) < 15:
            number.append(random.randint(0, 9))

        checksum = 0
        for i, digit in enumerate(reversed(number)):
            if i % 2 == 0:
                digit = digit * 2
                if digit > 9:
                    digit -= 9
            checksum += digit

        number.append((10 - (checksum % 10)) % 10)
        card_number = ''.join(map(str, number))
        card_numbers.append(card_number)
    return card_numbers

def gen_cards(bin_code, month, year, count):
    months = [month if month != "random" else f"{random.randint(1, 12):02d}" for _ in range(count)]
    years = [year if year != "random" else f"{random.randint(2023, 2030)}" for _ in range(count)]
    cvvs = [f"{random.randint(100, 999)}" for _ in range(count)]
    
    card_numbers = luhn_algorithm(bin_code, count)
    generated_data = [
        f"{card}|{month}|{year}|{cvv}"
        for card, month, year, cvv in zip(card_numbers, months, years, cvvs)
    ]

    with open("cc.txt", "w") as file:
        for line in generated_data:
            file.write(f"{line}\n")