import json
import os
from googleapiclient.discovery import build
from pathlib import Path


api_key: str = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

    @property
    def __data_info(self):
        """
        Данные о канале
        """
        data_info = self.youtube.channels().list(id=self.__channel_id, part='snippet, statistics').execute()
        return data_info

    @property
    def title(self):
        """
        Возвращает название канала
        """
        title = self.__data_info['items'][0]['snippet']['title']
        return title

    @property
    def description(self):
        description = self.__data_info['items'][0]['snippet']['description']
        return description

    @property
    def video_count(self):
        video_count = self.__data_info['items'][0]['statistics']['videoCount']
        return video_count

    @property
    def count_subscribers(self):
        count_subscribers = self.__data_info['items'][0]['statistics']['subscriberCount']
        return count_subscribers

    @property
    def view_count(self):
        view_count = self.__data_info['items'][0]['statistics']['viewCount']
        return view_count

    @property
    def url(self):
        return f'https://www.youtube.com/channel/{self.__channel_id}'

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def to_json(self, file_name):
        """
        Cохраняет в файл значения атрибутов экземпляра
        """
        path = os.path.join(Path(__file__).parent.parent, f"homework-2/{file_name}")
        structure_for_json = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'count_subscribers': self.count_subscribers,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(path, 'w', encoding='utf8') as file:
            json.dump(structure_for_json, file)

    @classmethod
    def get_service(cls):
        """
        Возвращающает объект для работы с YouTube API
        """
        return cls.youtube
