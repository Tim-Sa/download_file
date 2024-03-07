import time
import asyncio

import re
import tqdm
import aiohttp


def runtime(func): 
  
    def wrapper(*args, **kwargs): 
        st = time.time() 
        print('\033[92m' + f'{func.__name__} started... \033[0m')
        result = func(*args, **kwargs) 
        print('\033[92m' + f'{func.__name__} work time: ' + str(round(time.time() - st, 2)) + 's. \033[0m')
        return result
    
    return wrapper


@runtime
def get_filename_from_url(url: str) -> str:
    filename_pattern = r'\/([\w.][\w.-]*)(?<!\/\.)(?<!\/\.\.)(?:\?.*)?$'
    _target_file_path = re.findall(filename_pattern, url)

    if len(_target_file_path) == 0:
        raise ValueError("Can't read filename from specified link.")
    
    target_file_path = _target_file_path[0]

    return target_file_path


@runtime
def download_by_url(url: str, target_path: str = '', chunk_size: int = 1024) -> None:

    if target_path:
        target_file_path = target_path
    else:
        target_file_path = get_filename_from_url(url)

    try:
        asyncio.run(a_download_by_url(url, target_file_path, chunk_size))

    except Exception as e:
        # TODO: log
        print('\033[91m' + f"Can't download file:\n\t{str(e)}" + '\033[0m')
        print('\n', str(e), '\n')


async def a_download_by_url(url: str, target_file_path: str, chunk_size: int = 1024) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(target_file_path, "wb") as handle:
                async for data in response.content.iter_chunked(chunk_size):
                    handle.write(data)
                    
                    # Update tqdm progress bar
                    tqdm.tqdm.write('\033[96m' + f"Downloaded {round(handle.tell() / 1024, 2)} KB" + '\033[0m', end='\r')


def main():
    test_url = 'https://archive.org/download/dr_where-to-go-what-to-see-in-portland-oregon-the-city-of-roses-drawn-by-m-10917001/10917001.jpg'
    download_by_url(test_url)


if __name__ == '__main__':
    main()