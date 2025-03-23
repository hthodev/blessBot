import cloudscraper
import sys
import random
from datetime import datetime, timedelta
from colorama import Fore, Style
import asyncio
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, TimeoutError

# Constants
API_BASE_URL = "https://gateway-run.bls.dev/api/v1"
IP_SERVICE_URL = "https://icanhazip.com/"
DATE_EXPIRE = datetime(2035, 3, 17)
use_proxy = None

# Helper functions
def get_random_element(arr):
    return random.choice(arr)

def generate_random_hardware_info():
    cpu_architectures = ["x86_64", "ARM64", "x86"]
    cpu_models = [
        "Intel Core i7-10700K CPU @ 3.80GHz", "AMD Ryzen 5 5600G with Radeon Graphics",
        "Intel Core i5-10600K CPU @ 4.10GHz", "AMD Ryzen 7 5800X",
        "Intel Core i9-10900K CPU @ 3.70GHz", "AMD Ryzen 9 5900X",
        "Intel Core i3-10100 CPU @ 3.60GHz", "AMD Ryzen 3 3300X",
        "Intel Core i7-9700K CPU @ 3.60GHz", "Intel Core i5-9600K CPU @ 3.70GHz",
        "AMD Ryzen 5 3600X", "Intel Core i9-11900K CPU @ 3.50GHz", "AMD Ryzen 7 3700X",
        "Intel Xeon E5-2670 v3", "AMD Ryzen 9 3950X", "Intel Core i5-11600K CPU @ 3.90GHz",
        "AMD Ryzen 3 2200G with Radeon Vega Graphics", "Intel Core i7-9700F CPU @ 3.00GHz",
        "Intel Core i9-10850K", "AMD Ryzen 5 3400G with Radeon RX Vega 11",
        "Intel Core i5-8600K CPU @ 3.60GHz", "Intel Core i7-6800K CPU @ 3.40GHz",
        "AMD Ryzen 9 5950X", "Intel Core i5-10400F CPU @ 2.90GHz", "Intel Xeon Gold 6248",
        "AMD Ryzen Threadripper 3990X", "Intel Core i9-11980XE", "AMD Ryzen 7 5900HX",
        "Intel Core i7-11800H", "AMD Ryzen 9 5950H", "Intel Core i5-1135G7",
        "Intel Core i7-11375H", "Intel Core i9-11950H", "AMD Ryzen 5 5500U",
        "Intel Core i3-1005G1", "Intel Core i7-8565U", "AMD Ryzen 7 4800H",
        "Intel Core i5-8250U", "Intel Core i3-8109U", "Intel Core i9-10980HK",
        "AMD Ryzen 7 5800HS", "Intel Core i5-9300H", "Intel Core i7-10875H",
        "Intel Xeon Platinum 8280", "Intel Core i5-11300H", "AMD Ryzen 5 5600X",
        "Intel Xeon E3-1270 v6", "Intel Xeon E5-1650 v4", "Intel Xeon Silver 4210R",
        "AMD EPYC 7742", "Intel Core i7-11850H", "Intel Core i7-1165G7",
        "AMD Ryzen 7 5700U", "Intel Core i9-10900F", "AMD Ryzen 5 5600U",
        "Intel Core i7-11700K", "Intel Core i5-11500", "Intel Xeon Bronze 3104",
        "Intel Xeon Gold 6348", "Intel Core i7-9700KF", "AMD Ryzen 9 7950X",
        "Intel Core i5-11320H", "AMD Ryzen 9 5900HX"
    ]
    cpu_features = [
        "mmx", "sse", "sse2", "sse3", "ssse3", "sse4_1", "sse4_2", "avx", "avx2", "avx512",
        "fma", "fma4", "aes", "tsc", "hypervisor", "vme", "pdpe1gb", "rdtscp", "syscall", "smx",
        "lahf_lm", "x2apic", "clflush", "xsave", "xsaveopt", "clzero", "pge", "lm", "pat", "mmxext",
        "pse", "nx", "x86_64", "rdtscp", "tsc_adjust", "mpx", "sgx", "avx2", "avx512f", "avx512dq",
        "avx512ifma", "avx512pf", "avx512er", "avx512cd", "avx512bw", "avx512vl", "avx512vbmi",
        "avx512vpopcntdq", "avx512vbmi2", "avx512vbmib", "avx512vnni", "aes-ni", "movbe", "xstore",
        "tsc_deadline_timer", "pni", "bmi1", "bmi2", "rdrand", "rdseed", "sha_ni", "pt", "mwaitx",
        "ssbd", "mpx", "clflushopt", "clwb", "lbrv", "amd-v", "intel-vt", "amd-np", "amd64",
        "vmx", "nxbit", "f16c", "popcnt", "clzm", "tsc", "dca", "pt_write", "rdtsc_emu", "pmm",
        "spec_ctrl", "pt_tsc", "spec_emu", "mmxext", "prfchw", "debug", "hle", "sgx2", "pvemulate",
        "adx", "clm", "xsavec", "tme", "tme2", "ecx", "xfast", "pti", "pt-sc", "clwb-prefetch"
    ]
    num_processors = [4, 6, 8, 12, 16, 24, 32, 64, 128, 256, 512]
    memory_sizes = [
        8 * 1024 ** 3, 16 * 1024 ** 3, 32 * 1024 ** 3, 64 * 1024 ** 3,
        128 * 1024 ** 3, 256 * 1024 ** 3, 512 * 1024 ** 3, 1024 * 1024 ** 3,
        2048 * 1024 ** 3, 4096 * 1024 ** 3, 8192 * 1024 ** 3, 16384 * 1024 ** 3
    ]

    random_cpu_features = list(set([get_random_element(cpu_features) for _ in range(random.randint(1, len(cpu_features)))]))

    return {
        "cpuArchitecture": get_random_element(cpu_architectures),
        "cpuModel": get_random_element(cpu_models),
        "cpuFeatures": random_cpu_features,
        "numOfProcessors": get_random_element(num_processors),
        "totalMemory": get_random_element(memory_sizes),
        "extensionVersions": "0.1.8"
    }

# File reading functions
async def read_proxies():
    with open("proxy.txt", "r") as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

async def read_node_and_hardware_ids():
    with open("id.txt", "r") as file:
        ids = [line.strip() for line in file if line.strip()]
    return [{"nodeId": id.split(":")[0], "hardwareId": id.split(":")[1], "sign_extension": id.split(":")[2]} for id in ids]

async def read_auth_token():
    with open("user.txt", "r") as file:
        auth_tokens = [line.strip() for line in file if line.strip()]
    return auth_tokens

# Cloudscraper functions
def fetch_ip_address_sync(proxy=None, scraper=None, retries=3, delay=3):
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    proxies = {"http": proxy, "https": proxy} if proxy else None

    for attempt in range(1, retries + 1):
        try:
            start_time = time.time()
            response = scraper.get(IP_SERVICE_URL, headers=headers, proxies=proxies)
            duration = time.time() - start_time

            print(f"[{datetime.now().isoformat()}] Proxy {proxy} responded in {duration:.2f} seconds")
            return response.text.strip()
        except Exception as error:
            print(f"[{datetime.now().isoformat()}] Attempt {attempt}/{retries} - Error fetching IP address: {error}")

            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)

    return None

async def fetch_ip_address(proxy=None, scraper=None, retries=3, delay=3):
    with ThreadPoolExecutor() as executor:
        try:
            future = executor.submit(fetch_ip_address_sync, proxy, scraper, retries, delay)
            return await asyncio.wait_for(asyncio.wrap_future(future), timeout=10)
        except TimeoutError:
            print(f"[{datetime.now().isoformat()}] Timeout fetching IP address")
            return None

def register_node_sync(node_id, hardware_id, ip_address, proxy, auth_token, scraper):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "origin": "chrome-extension://pljbjcehnhcnofmkdbjolghdcjnmekia",
        "x-extension-version": "0.1.8"
    }
    proxies = {"http": proxy, "https": proxy} if proxy else None

    register_url = f"{API_BASE_URL}/nodes/{node_id}"
    print(f"[{datetime.now().isoformat()}] Registering node with IP: {ip_address}, Hardware ID: {hardware_id}")

    payload = {
        "ipAddress": ip_address,
        "hardwareId": hardware_id,
        "hardwareInfo": generate_random_hardware_info(),
        "extensionVersion": "0.1.8"
    }

    try:
        response = scraper.post(register_url, headers=headers, json=payload, proxies=proxies)
        print(f"[{datetime.now().isoformat()}] Registration response: {response.json()}")
        return response.json()
    except Exception as error:
        print(f"[{datetime.now().isoformat()}] Error registering node: {error}")
        raise error

async def register_node(node_id, hardware_id, ip_address, proxy, auth_token, scraper):
    with ThreadPoolExecutor() as executor:
        try:
            future = executor.submit(register_node_sync, node_id, hardware_id, ip_address, proxy, auth_token, scraper)
            return await asyncio.wait_for(asyncio.wrap_future(future), timeout=10)
        except TimeoutError:
            print(f"[{datetime.now().isoformat()}] Timeout registering node")
            return None

def start_session_sync(node_id, proxy, auth_token, scraper):
    headers = {
        "Accept": "*/*",
        "Authorization": f"Bearer {auth_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "origin": "chrome-extension://pljbjcehnhcnofmkdbjolghdcjnmekia",
        "x-extension-version": "0.1.8"
    }
    proxies = {"http": proxy, "https": proxy} if proxy else None

    start_session_url = f"{API_BASE_URL}/nodes/{node_id}/start-session"
    print(f"[{datetime.now().isoformat()}] Starting session for node {node_id}, it might take a while...")

    try:
        response = scraper.post(start_session_url, headers=headers, proxies=proxies)
        print(f"[{datetime.now().isoformat()}] Start session response: {response.json()}")
        return response.json()
    except Exception as error:
        print(f"[{datetime.now().isoformat()}] Error starting session: {error}")
        raise error

async def start_session(node_id, proxy, auth_token, scraper):
    with ThreadPoolExecutor() as executor:
        try:
            future = executor.submit(start_session_sync, node_id, proxy, auth_token, scraper)
            return await asyncio.wait_for(asyncio.wrap_future(future), timeout=10)
        except TimeoutError:
            print(f"[{datetime.now().isoformat()}] Timeout starting session")
            return None

def ping_node_sync(node_id, proxy, ip_address, is_b7s_connected, auth_token, scraper, sign_extension):
    headers = {
        "Accept": "*/*",
        "Authorization": f"Bearer {auth_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "origin": "chrome-extension://pljbjcehnhcnofmkdbjolghdcjnmekia",
        "x-extension-version": "0.1.8",
        "Content-Type": "application/json",
        "X-Extension-Signature": sign_extension
    }
    proxies = {"http": proxy, "https": proxy} if proxy else None

    ping_url = f"{API_BASE_URL}/nodes/{node_id}/ping"
    print(f"[{datetime.now().isoformat()}] Pinging node {node_id} using proxy {proxy}")

    payload = {"isB7SConnected": is_b7s_connected}

    try:
        response = scraper.post(ping_url, headers=headers, json=payload, proxies=proxies)
        data = response.json()
        log_message = f"[{datetime.now().isoformat()}] Ping response, NodeID: {Fore.GREEN}{node_id}{Style.RESET_ALL}, Status: {Fore.YELLOW}{response.text}{Style.RESET_ALL}, Proxy: {proxy}, IP: {ip_address}"
        print(log_message)
        return data
    except Exception as error:
        print(f"[{datetime.now().isoformat()}] Error pinging node: {error}")
        raise error

async def ping_node(node_id, proxy, ip_address, is_b7s_connected, auth_token, scraper, sign_extension):
    with ThreadPoolExecutor() as executor:
        try:
            future = executor.submit(ping_node_sync, node_id, proxy, ip_address, is_b7s_connected, auth_token, scraper, sign_extension)
            return await asyncio.wait_for(asyncio.wrap_future(future), timeout=10)
        except TimeoutError:
            print(f"[{datetime.now().isoformat()}] Timeout pinging node")
            return None

def check_node_sync(node_id, proxy, auth_token, scraper):
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "origin": "chrome-extension://pljbjcehnhcnofmkdbjolghdcjnmekia",
        "x-extension-version": "0.1.8"
    }
    proxies = {"http": proxy, "https": proxy} if proxy else None

    check_node_url = f"{API_BASE_URL}/nodes/{node_id}"
    print(f"[{datetime.now().isoformat()}] Checking node {node_id} using proxy {proxy}")

    try:
        response = scraper.get(check_node_url, headers=headers, proxies=proxies)
        data = response.json()
        today_reward = data.get("todayReward", 0)
        is_connected = data.get("isConnected", False)
        log_message = f"[{datetime.now().isoformat()}] node Check response, NodeID: {Fore.GREEN}{node_id}{Style.RESET_ALL}, Today Rewards: {Fore.YELLOW}{today_reward}{Style.RESET_ALL}, is Connected: {is_connected}"
        print(log_message)
        return is_connected
    except Exception as error:
        print(f"[{datetime.now().isoformat()}] Error checking node: {error}")
        raise error

async def check_node(node_id, proxy, auth_token, scraper):
    with ThreadPoolExecutor() as executor:
        try:
            future = executor.submit(check_node_sync, node_id, proxy, auth_token, scraper)
            return await asyncio.wait_for(asyncio.wrap_future(future), timeout=10)
        except TimeoutError:
            print(f"[{datetime.now().isoformat()}] Timeout checking node")
            return False

# Main logic
async def process_reg_node(node_id, hardware_id, proxy, ip_address, auth_token, scraper):
    try:
        print(f"[{datetime.now().isoformat()}] Processing nodeId: {node_id}, hardwareId: {hardware_id}, IP: {ip_address}")
        is_connected = await check_node(node_id, proxy, auth_token, scraper)
        print(f"[{datetime.now().isoformat()}] Node nodeId: {node_id} is connected? {is_connected}.")
        if not is_connected:
            try:
                print(f"[{datetime.now().isoformat()}] Starting session for nodeId: {node_id}")
                await register_node(node_id, hardware_id, ip_address, proxy, auth_token, scraper)
                await start_session(node_id, proxy, auth_token, scraper)
            except Exception as error:
                print(f"[{datetime.now().isoformat()}] Error Starting session for nodeId: {node_id}. Error: {error}")
    except Exception as error:
        print(f"[{datetime.now().isoformat()}] An error occurred: {error}")

async def process_node(node_id, hardware_id, proxy, ip_address, auth_token, scraper, sign_extension):
    try:
        print(f"[{datetime.now().isoformat()}] Processing nodeId: {node_id}, hardwareId: {hardware_id}, IP: {ip_address}")
        is_connected = await check_node(node_id, proxy, auth_token, scraper)
        print(f"[{datetime.now().isoformat()}] Sending initial ping for nodeId: {node_id}")
        await ping_node(node_id, proxy, ip_address, is_connected, auth_token, scraper, sign_extension)
    except Exception as error:
        print(f"[{datetime.now().isoformat()}] Error occurred for nodeId: {node_id}, restarting process: {error}")

async def run_all(initial_run=True):
    try:
        ids = await read_node_and_hardware_ids()
        proxies = await read_proxies()
        auth_tokens = await read_auth_token()

        if len(proxies) < len(ids):
            raise Exception(f"Number of proxies ({len(proxies)}) does not match number of nodeId:hardwareId pairs ({len(ids)})")

        current_account = ''
        scraper = cloudscraper.create_scraper()
        ip_addresses = [None] * len(auth_tokens)

        while True:
            start_time = time.time()
            stt_account = 0

            for i in range(len(auth_tokens)):
                try:
                    if current_account != auth_tokens[i]:
                        current_account = auth_tokens[i]
                        stt_account += 1
                    print(f"[{datetime.now().isoformat()}]: Start with account {stt_account}")
                    print(f"[{datetime.now().isoformat()}]: Start with stt id {i + 1}")
                    
                    node_id = ids[i]["nodeId"]
                    hardware_id = ids[i]["hardwareId"]
                    sign_extension = ids[i]["sign_extension"]
                    proxy = proxies[i]
                    ip_address = None
                    if not ip_addresses[i]:
                        ip_address = await fetch_ip_address(proxy, scraper)
                        ip_addresses[i] = ip_address
                    else:
                        ip_address = ip_addresses[i]
                    print(f"[{datetime.now().isoformat()}]: Start with ipAddress {ip_address}")

                    auth_token = auth_tokens[i]
                    await process_reg_node(node_id, hardware_id, proxy, ip_address, auth_token, scraper)
                    await process_node(node_id, hardware_id, proxy, ip_address, auth_token, scraper, sign_extension)
                
                except Exception as error:
                    print(f"[{datetime.now().isoformat()}] An error occurred: {error}")

            # Tính thời gian đã chạy
            elapsed_time = time.time() - start_time  
            remaining_time = (15 * 60) - elapsed_time 

            if remaining_time > 0:  
                await asyncio.sleep(remaining_time)
            
    except Exception as error:
        print(f"[{datetime.now().isoformat()}] An error occurred: {error}")

# Run the script
if __name__ == "__main__":
    asyncio.run(run_all())
