import hashlib
import json
import os
import random
import base64

def get_random_hardware_identifier():
    random_cpu_architecture = 'x64' if random.random() > 0.5 else 'x86'
    random_cpu_model = f'Fake CPU Model {random.randint(0, 999)}'
    random_num_of_processors = random.randint(1, 8)
    random_total_memory = random.randint(1, 16) * 1024 * 1024 * 1024

    cpu_info = {
        'cpuArchitecture': random_cpu_architecture,
        'cpuModel': random_cpu_model,
        'numOfProcessors': random_num_of_processors,
        'totalMemory': random_total_memory
    }

    return base64.b64encode(json.dumps(cpu_info).encode()).decode()

async def generate_device_identifier():
    hardware_identifier = get_random_hardware_identifier()
    device_info = json.dumps({'hardware': hardware_identifier})
    hash_object = hashlib.sha256(device_info.encode())
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
        device_identifier = await generate_device_identifier()

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
