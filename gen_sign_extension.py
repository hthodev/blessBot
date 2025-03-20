import hashlib
import json
import os
import random
import base64

def generate_hash():
    random_data = os.urandom(32)
    hash_object = hashlib.sha512(random_data)
    return hash_object.hexdigest()


async def main():
    with open('id.txt', 'r') as file:
        id_str = file.read()

    print('\033[91m\033[1mThis is only for testing purposes, I do not recommend using it\033[0m')

    results = []
    ids = id_str.splitlines()

    total = int(input('\033[96mHow many identifiers do you want to generate? \033[0m'))
    output = ''

    for i in range(total):
        device_identifier = generate_hash()

        log_entry = f'Device Identifier {i + 1}: \033[92m{device_identifier}\033[0m\n'
        formatted_entry = f'{ids[i]}:{device_identifier}\n'
        output += formatted_entry
        print(log_entry)

    with open('id.txt', 'w') as file:
        file.write(output)

    print('\033[93mData saved to id.txt\033[0m')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
