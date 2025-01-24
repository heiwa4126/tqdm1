import time

from tqdm import tqdm


def main():
    for i in tqdm(range(10000)):
        time.sleep(0.0005)


if __name__ == "__main__":
    main()
