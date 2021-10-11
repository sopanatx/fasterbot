# Requirement

- Python 3.7.x

Download python di https://www.python.org/downloads/

# Setup

Install Module `requests` and `colorama` with the following command

```sh
pip install requests colorama
```

open chrome and go to https://shopee.co.th/ then login.
press F12 then enter the network tab.

![tab network](images/tab_network.png)

refresh the webpage and find the item `/`

![forward slash](images/forward_slash.png)

click the item then right click on the "cookie" header in the "Request headers"

![copy header](images/copy_header.png)

choose `copy value`.

edit cookie.txt then paste and save!

finished / ready to login

run the script with the following command

```
python main.py
```

# Addition

for speed depending on each internet connection.
and does not guarantee 100% can
