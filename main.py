import os
import random
import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from starlette.requests import Request

# Создаем экземпляр APIRouter
router = APIRouter()

def create_dataset(train_count, val_count, test_count):
    '''
    Функция формирования локального датасета
    '''
    dataset_path = "dataset"  # Путь к корневой папке датасета
    folders = ["volume1", "volume2", "volume3"]  # Названия подпапок внутри датасета для train, val и test
    data_types = ["train", "val", "test"]  # Типы данных: train, val и test

    dataset = {data_type: [] for data_type in data_types}  # Создание словаря для хранения путей к изображениям каждого типа данных

    # Проходим по каждой из трех папок (volume1, volume2, volume3)
    for i, folder in enumerate(folders):
        folder_path = os.path.join(dataset_path, folder)  # Получаем путь к текущей папке
        images = []  # Создаем список для хранения путей к изображениям в текущей папке

        # Проходим по каждой из двух подпапок "NORMAL" и "PNEUMONIA"
        for image_type in ["NORMAL", "PNEUMONIA"]:
            image_folder = os.path.join(folder_path, image_type)  # Получаем путь к подпапке с изображениями
            image_list = os.listdir(image_folder)  # Получаем список файлов в подпапке
            image_list = [os.path.join(image_folder, img) for img in image_list]  # Формируем полный путь к каждому изображению
            images.extend(image_list)  # Добавляем пути к изображениям в список

        if i == 0:  # Если текущая папка - train
            dataset['train'] = random.sample(images, train_count)  # Выбираем случайные изображения для train_count
        elif i == 1:  # Если текущая папка - val
            val_images = [img for img in images if "NORMAL" in img] + [img for img in images if "PNEUMONIA" in img]
            dataset['val'] = val_images[:val_count]  # Выбираем изображения для val_count в порядке чередования "NORMAL" и "PNEUMONIA"
        else:  # Если текущая папка - test
            dataset['test'] = random.sample(images, test_count)  # Выбираем случайные изображения для test_count

    return dataset['train'], dataset['val'], dataset['test']  # Возвращаем списки путей к изображениям train, val и test

def calculate_image_counts(F, r=1, ratio_train=0.7, ratio_val=0.2, ratio_test=0.1):
    """
    :param F: Размер памяти в любых единицах (предполагается в МБ).
    :param r: Средний размер изображения в МБ.
    :param ratio_train: Пропорция набора данных для обучения.
    :param ratio_val: Пропорция набора данных для валидации.
    :param ratio_test: Пропорция набора данных для тестирования.
    :return: Кортеж количеств изображений для наборов данных обучения, валидации и тестирования.
    """


    # Total number of images that can be stored
    count_images = F / r

    # Calculate counts for train, val, and test datasets
    count_train = round(count_images * ratio_train)
    count_val = round(count_images * ratio_val)
    count_test = round(count_images * ratio_test)

    return count_train, count_val, count_test


@router.get("/ping")
async def ping() -> dict:
    return {"Success": True}

@router.get("/")
async def mainpage() -> str:
    return "Ты на главной странице"


# async def create_record(request: Request) -> dict:
#     # mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["test_database"]
#     # await mongo_client.records.insert_one({"sample": "record"})
#     return {"Success": True}

# async def get_images(request: Request) -> list:
#     train_images, val_images, test_images = create_dataset(6, 3, 3)
#     return [train_images, val_images, test_images]
@router.get("/get_images/{F}/")
async def get_images(F: float) -> dict:
    count_train, count_val, count_test = calculate_image_counts(F)
    train_images, val_images, test_images = create_dataset(count_train, count_val, count_test)
    return {"train": train_images, "val": val_images, "test": test_images}



# routes = [
#     APIRoute(path="/ping", endpoint=ping, methods=["GET"]),
#     APIRoute(path="/", endpoint=mainpage, methods=["GET"]),
#     APIRoute(path="/get_images", endpoint=get_images, methods=["GET"]),
#     # APIRoute(path="/create_record", endpoint=create_record, methods=["POST"]),
# ]


app = FastAPI()
# app.include_router(APIRouter(routes=routes))
# Включаем маршруты из router в основное приложение
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)



# dataset: https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia/
# train: normal - 1341; pneumonia - 3875;
# val: normal - 8; pneumonia - 8; 
# test: normal - 234; pneumonia - 390;
# docker-compose -f docker-compose-ci.yaml up -d