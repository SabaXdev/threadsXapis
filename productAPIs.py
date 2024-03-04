import requests
import threading
import json
import time

API_URLS = [
    "https://dummyjson.com/products/{}".format(i) for i in range(1, 101)
]


class DataLoaderThread(threading.Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.result = None

    def run(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.result = response.json()
        else:
            print(f"Error occurred, failed to fetch data from {self.url}")


def main():
    start_time = time.perf_counter()

    all_threads = []
    for url in API_URLS:
        thread = DataLoaderThread(url)
        all_threads.append(thread)
        thread.start()

    products = []
    for thread in all_threads:
        thread.join()                       # Pause main thread, until current thread performs its operation
        if thread.result:                   # If request is successful, then thread result will be added to products
            # list
            products.append(thread.result)

    # Write products to file names "products.json"
    with open("products.json", "w") as file:
        json.dump(products, file, indent=4)

    end_time = time.perf_counter()
    print(f"Program runtime is: {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
