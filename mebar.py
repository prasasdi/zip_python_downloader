from tqdm import tqdm

# separate get bar from the main.py, about to add another method to extract those .zip
def get_bar(file_name:str, file_size:int):
    return tqdm(
                desc = file_name,
                total = file_size,
                unit = 'iB',
                unit_scale=True,
                unit_divisor=1024)