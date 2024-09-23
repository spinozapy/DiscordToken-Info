import requests
import json
import sys
import colorama
import os

from datetime import datetime
from colorama import Fore, init

clear_command = 'cls' if os.name == 'nt' else 'clear'

cc_digits = {
    'american express': '3',
    'visa': '4',
    'mastercard': '5'
}

def get_user_info(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }

    res = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
    user_info = {}

    if res.status_code == 200:
        res_json = res.json()
        user_info['username'] = f'{res_json["username"]}#{res_json["discriminator"]}'
        user_info['user_id'] = res_json['id']
        user_info['avatar_id'] = res_json['avatar']
        user_info['avatar_url'] = f'https://cdn.discordapp.com/avatars/{user_info["user_id"]}/{user_info["avatar_id"]}.png'  # .png uzantısı
        user_info['phone_number'] = res_json.get('phone', 'N/A')  # 'N/A' döndürüyoruz
        user_info['email'] = res_json.get('email', 'N/A')
        user_info['creation_date'] = datetime.utcfromtimestamp(((int(user_info["user_id"]) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')
    return user_info

def get_billing_info(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }

    billing_info = []
    billing_sources = requests.get('https://discord.com/api/v10/users/@me/billing/payment-sources', headers=headers).json()
    
    for x in billing_sources:
        y = x.get('billing_address', {})
        name = y.get('name', 'N/A')
        address_1 = y.get('line_1', 'N/A')
        address_2 = y.get('line_2', '')
        city = y.get('city', 'N/A')
        postal_code = y.get('postal_code', 'N/A')
        state = y.get('state', 'N/A')
        country = y.get('country', 'N/A')

        if x['type'] == 1:
            cc_brand = x['brand']
            cc_first = cc_digits.get(cc_brand)
            cc_last = x['last_4']
            cc_month = str(x['expires_month'])
            cc_year = str(x['expires_year'])
            
            data = {
                'Payment Type': 'Credit Card',
                'Valid': not x['invalid'],
                'CC Holder Name': name,
                'CC Brand': cc_brand.title(),
                'CC Number': ''.join(z if (i + 1) % 2 else z + ' ' for i, z in enumerate((cc_first if cc_first else '*') + ('*' * 11) + cc_last)),
                'CC Exp. Date': ('0' + cc_month if len(cc_month) < 2 else cc_month) + '/' + cc_year[2:4],
                'Address 1': address_1,
                'Address 2': address_2 if address_2 else '',
                'City': city,
                'Postal Code': postal_code,
                'State': state if state else '',
                'Country': country,
                'Default Payment Method': x['default']
            }

            billing_info.append(data)

    return billing_info

def print_user_info(user_info):
    os.system(clear_command)
    print(' ')
    print(f' {Fore.GREEN}Username      : {Fore.RESET}{user_info["username"]}')
    print(f' {Fore.GREEN}User ID       : {Fore.RESET}{user_info["user_id"]}')
    print(f' {Fore.GREEN}Creation Date : {Fore.RESET}{user_info["creation_date"]}')
    print(f' {Fore.GREEN}Avatar URL    : {Fore.RESET}{user_info["avatar_url"] if user_info["avatar_id"] else ""}')
    print(f' {Fore.GREEN}Phone Number  : {Fore.RESET}{user_info["phone_number"] if user_info["phone_number"] else ""}')
    print(f' {Fore.GREEN}Email         : {Fore.RESET}{user_info["email"] if user_info["email"] else ""}')
    print(f' {Fore.RESET}\n')

def print_billing_info(billing_info):
    os.system(clear_command)
    for payment in billing_info:
        print(f' {Fore.GREEN}Payment Type    : {Fore.RESET}{payment["Payment Type"]}')
        print(f' {Fore.GREEN}Valid           : {Fore.RESET}{payment["Valid"]}')
        print(f' {Fore.GREEN}CC Holder Name  : {Fore.RESET}{payment["CC Holder Name"]}')
        print(f' {Fore.GREEN}CC Brand        : {Fore.RESET}{payment["CC Brand"]}')
        print(f' {Fore.GREEN}CC Number       : {Fore.RESET}{payment["CC Number"]}')
        print(f' {Fore.GREEN}CC Exp. Date    : {Fore.RESET}{payment["CC Exp. Date"]}')
        print(f' {Fore.GREEN}Address 1       : {Fore.RESET}{payment["Address 1"]}')
        print(f' {Fore.GREEN}Address 2       : {Fore.RESET}{payment["Address 2"]}')
        print(f' {Fore.GREEN}City            : {Fore.RESET}{payment["City"]}')
        print(f' {Fore.GREEN}Postal Code     : {Fore.RESET}{payment["Postal Code"]}')
        print(f' {Fore.GREEN}State           : {Fore.RESET}{payment["State"]}')
        print(f' {Fore.GREEN}Country         : {Fore.RESET}{payment["Country"]}')
        print(f' {Fore.GREEN}Default Method  : {Fore.RESET}{payment["Default Payment Method"]}')
        print(f' {Fore.RESET}\n')

def get_token_input():
    os.system(clear_command)
    try:
        print(f"{Fore.GREEN}[TokenInfo]: {Fore.LIGHTYELLOW_EX}Enter token (or 'exit' to quit)")
        token = input(f"{Fore.MAGENTA}root@you:~$ " + colorama.Fore.WHITE + "")
        return token
    except KeyboardInterrupt:
        os.system(clear_command)
        return get_token_input()

def main():
    init(convert=True)

    while True:
        token = get_token_input()
        if token.lower() == 'exit':
            break
        
        while True:
            try:
                user_info = get_user_info(token)
                if not user_info:
                    os.system(clear_command)
                    print(f"{Fore.GREEN}[TokenInfo]: {Fore.LIGHTYELLOW_EX}Enter token (or 'exit' to quit)")
                    token = input(f"{Fore.MAGENTA}root@you:~$ " + colorama.Fore.WHITE + "")
                    if token.lower() == 'exit':
                        break
                    continue
                else:
                    break
            except UnicodeEncodeError:
                os.system(clear_command)
                print(f"{Fore.GREEN}[TokenInfo]: {Fore.LIGHTYELLOW_EX}Enter token (or 'exit' to quit)")
                token = input(f"{Fore.MAGENTA}root@you:~$ " + colorama.Fore.WHITE + "")
                continue

        if token.lower() == 'exit':
            break

        print_user_info(user_info)

        billing_info = get_billing_info(token)
        print(f"{Fore.GREEN}[TokenInfo]: " + colorama.Fore.LIGHTYELLOW_EX + "Do you want to see credit card information? (Y/N) ")
        choice = input(f"{Fore.MAGENTA}root@you:~$ " + colorama.Fore.WHITE + "")
        if choice.lower() == 'y':
            print_billing_info(billing_info)
            input("Press Enter to continue...")
            os.system(clear_command)
        elif choice.lower() == 'n':
            print(f"{Fore.GREEN}[TokenInfo]: " + colorama.Fore.LIGHTYELLOW_EX + "Do you want to clear previous information? (Y/N) ")
            clear_choice = input(f"{Fore.MAGENTA}root@you:~$ " + colorama.Fore.WHITE + "")
            if clear_choice.lower() == 'y':
                os.system(clear_command)
            elif clear_choice.lower() == 'n':
                continue

if __name__ == '__main__':
    main()
