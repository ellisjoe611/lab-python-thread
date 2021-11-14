from concurrent.futures import ThreadPoolExecutor


def worker(data: int):
    arr = [_ for _ in range(data * 1000000)]
    print(f'Thread number {data} is finished >> {len(arr)}')


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=10) as exe:
        future = exe.submit(worker, 2)
        print("done")
