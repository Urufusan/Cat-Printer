
import math


def roundTraditional(val, digits):
    return round(val+10**(-len(str(val))-1), digits)

# round = roundTraditional


def receipt(*purchases: tuple, info_args: dict = {}, ):
    """Generates textual receipt that will be parsed into PIL

    Args:
        info_args (Dict): Textual parameters for the currency, name etc.
        purchases (Tuple): List of purchases

    Returns:
        str: Receipt in a form of a string
    """
    width = info_args.get("width", 35)
    currency = info_args.get("currency", ("None", ""))
    shop_name = info_args.get("shop_name", "Test shop")
    # receipt ([(name, price, count), ...])
    total = 0
    txt_elements = [
        shop_name.center(width),
        currency[0].rjust(width)
    ]
    for name, price, count in purchases:
        total += price * count

        all_price = str(roundTraditional(price * count, 2)) + currency[1]

        msg = f'{name}'.ljust(width-len(all_price), ' ')
        msg += all_price

        if type(count) is int and count >= 2:
            msg += f'\n    {count} x {price}'
        # elif type(count) is float:
        #     msg += f'\n    {count} kg x {price}'

        txt_elements.append(msg)

    total = str(roundTraditional(total, 2))+currency[1]
    txt_elements.append("\nTOTAL:".ljust(width-len(total) + 1) + total)
    return '\n'.join(txt_elements)


class ShopItem():
    def __init__(self, name: str, price: float, weight: float = None, unit: str = None, count: int = 1, currency=["EUR", "€"]):
        self.name = name
        self.price = price
        self.weight = weight
        self.unit = unit
        self.price_per_unit = self.calculate_price_per_unit()
        self.count = count
        self.currency = currency
        self.packed_info = (self.name+((f" ({self.price_per_unit} {self.currency[0]}/{self.unit})") if self.price_per_unit else ""),
                            self.price, self.count)

    def __getitem__(self, key):
        return self.packed_info[key]

    def calculate_price_per_unit(self):
        if self.weight is not None and self.weight != 0:
            return roundTraditional(self.price / self.weight, 2)
        elif self.unit is not None:
            # For items without weight but a fixed price
            return roundTraditional(self.price, 2)
        else:
            return 0  # Default case

    def display_info(self):
        print(f"Item: {self.name}")
        if self.unit:
            print(f"Price: {self.price} {self.currency[0]}")
            print(f"Weight: {self.weight} {self.unit}")
            print(
                f"Price per {self.unit}: {self.price_per_unit} {self.currency[0]}/{self.unit}")
        else:
            print(f"Price: {self.price} {self.currency[1]}")
            # print("No specific unit for this item.")


if __name__ == "__main__":
    item_with_unit = ShopItem("Apple", 2.555, 1.5, "kg")
    item_without_unit = ShopItem("Computer Mouse", 15.42, count=2)

    # item_with_unit.display_info()
    # print()
    # item_without_unit.display_info()
    # exit()
    width = 25
    currency = "EUR", "€"
    shop_name = "Fake LIDL"
    print(receipt(
        # ('bananas', 2, 1),
        # ('milk', 3, 0.5),
        item_with_unit,
        item_without_unit,
        info_args={"text_width": width,
                   "currency": currency,
                   "shop_name": shop_name
                   },
    ))
