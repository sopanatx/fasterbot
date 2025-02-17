from bot import Bot
from user import User
from checkoutdata import PaymentInfo, PaymentChannel, PaymentChannelOptionInfo
from datetime import datetime
from colorama import Fore, Style, init
from time import sleep
from datetime import datetime
import os


init()
INFO = Fore.LIGHTBLUE_EX + "[*]" + Fore.BLUE
INPUT = Fore.LIGHTGREEN_EX + "[?]" + Fore.GREEN
PROMPT = Fore.LIGHTRED_EX + "[!]" + Fore.RED
if os.name.lower() == "nt":
    os.system("cls")
else:
    os.system("clear")
print(INFO, "Retrieving user information...", end='\r')
cookie = open("cookie.txt", 'r')
user = User.login(cookie.read())
cookie.close()
print(INFO, "Welcome", Fore.GREEN, user.name, ' ' * 10)
print()

print(INFO, "Enter the url of the item to be purchased")
bot = Bot(user)
item = bot.fetch_item_from_url(input(INPUT + " url: " + Fore.RESET))

print(Fore.RESET, "-" * 32)
print(Fore.LIGHTBLUE_EX, "Name:", Fore.GREEN, item.name)
print(Fore.LIGHTBLUE_EX, "Price:", Fore.GREEN, item.get_price(item.price))
print(Fore.LIGHTBLUE_EX, "Brand:", Fore.GREEN, item.brand)
print(Fore.LIGHTBLUE_EX, "Store Location:", Fore.GREEN, item.shop_location)
print(Fore.RESET, "-" * 32)
print()

selected_model = 0
if len(item.models) > 1:
    print(INFO, "เลือกประเภทสินค้า")
    print(Fore.RESET, "-" * 32)
    for index, model in enumerate(item.models):
        print(Fore.GREEN + '[' + str(index) + ']' + Fore.BLUE, model.name)
        print('\t', Fore.LIGHTBLUE_EX, "ราคา:",
              Fore.GREEN, item.get_price(model.price))
        print('\t', Fore.LIGHTBLUE_EX,
              "จำนวนสต็อกสินค้า:", Fore.GREEN, model.stock)
        print('\t', Fore.LIGHTBLUE_EX, "รหัสสินค้า:", Fore.GREEN, model.model_id)
        print(Fore.RESET, "-" * 32)
    print()
    selected_model = int(input(INPUT + " เลือกประเภทสินค้าที่ต้องการ : "))
    print()

print(INFO, "เลือกวิธีการชำระเงิน")
payment_channels = dict(enumerate(PaymentChannel))
for index, channel in payment_channels.items():
    print(Fore.GREEN + '[' + str(index) + ']' + Fore.BLUE, channel.name)
print()
selected_payment_channel = payment_channels[int(input(INPUT + " ตัวเลือก: "))]
print()

selected_option_info = PaymentChannelOptionInfo.NONE
if selected_payment_channel is PaymentChannel.TRANSFER_BANK or \
        selected_payment_channel is PaymentChannel.AKULAKU:
    options_info = dict(enumerate(list(PaymentChannelOptionInfo)[1 if selected_payment_channel is
                        PaymentChannel.TRANSFER_BANK else 7:None if selected_payment_channel is
                        PaymentChannel.AKULAKU else 7]))
    for index, option_info in options_info.items():
        print(Fore.GREEN + '[' + str(index) + ']' +
              Fore.BLUE, option_info.name)
    print()
    selected_option_info = options_info[int(input(INPUT + " ตัวเลือก: "))]

if not item.is_flash_sale:
    if item.upcoming_flash_sale is not None:
        flash_sale_start = datetime.fromtimestamp(
            item.upcoming_flash_sale.start_time)
        print(INFO, "Flash Sale Time: ", flash_sale_start.strftime("%H:%M:%S"))
        print(INFO, "Waiting.. Flash Sale", end='\r')
        sleep((datetime.fromtimestamp(
            item.upcoming_flash_sale.start_time) - datetime.now()).total_seconds())
    else:
        print(PROMPT, "Flash Sale has arrived")
        exit(1)
print(INFO, "Flash Sale Co")
start = datetime.now()
print(INFO, "Adding items to cart...")
cart_item = bot.add_to_cart(item, selected_model)
print(INFO, "Checkout item...")
bot.checkout(PaymentInfo(
    channel=selected_payment_channel,
    option_info=selected_option_info
), cart_item)
final = datetime.now() - start
print(INFO, "Item successfully purchased in time", Fore.YELLOW, final.seconds, "second", final.microseconds // 1000,
      "ms")
print(Fore.GREEN + "[*]", "Success")
