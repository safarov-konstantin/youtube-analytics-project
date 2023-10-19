import isodate
import datetime
from src.channel import Channel


class PlayList:
    def __init__(self, playlist_id):
        self.__youtube = Channel.get_service()
        self.__playlist_id = playlist_id
        self.title = self.__get_title_playlist()
        self.url = self.__get_url_playlist()

    @property
    def youtube(self):
        return self.__youtube

    @property
    def playlist_id(self):
        return self.__playlist_id

    @property
    def total_duration(self):
        """
        возвращает объект класса datetime.timedelta с суммарной длительность плейлиста
        """
        video_ids = self.__get_video_ids()
        video_response = self.__youtube.videos().list(part='contentDetails,statistics',
                                                      id=','.join(video_ids)
                                                      ).execute()
        total_duration = datetime.timedelta()
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def __get_title_playlist(self):
        """
        Получить название плейлиста
        """
        playlist_response = self.__youtube.playlists().list(part='snippet',
                                                            id=self.__playlist_id
                                                            ).execute()
        title = playlist_response['items'][0]['snippet']['title']
        return title

    def __get_url_playlist(self):
        """
        Получить url плейлиста
        """
        return f"https://www.youtube.com/playlist?list={self.__playlist_id}"

    def __get_video_ids(self):
        """
        Получить все id видеороликов из плейлиста
        """
        playlist_videos = self.__youtube.playlistItems().list(playlistId=self.playlist_id,
                                                              part='contentDetails',
                                                              maxResults=50,
                                                              ).execute()
        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        return video_ids

    def show_best_video(self):
        """
        возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        video_ids = self.__get_video_ids()
        statistics_videos = self.__get_statistics_videos(video_ids)
        vidio_id_max_like_count = max(statistics_videos, key=statistics_videos.get)
        return f'https://youtu.be/{vidio_id_max_like_count}'

    def __get_statistics_videos(self, video_ids):
        """
        Получить статистику по всем видео в плейлисте
        """
        video_response = self.__youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                      id=','.join(video_ids)
                                                      ).execute()
        videos_items = video_response['items']
        statistics_videos = {video['id']: video['statistics']['likeCount'] for video in videos_items}
        return statistics_videos
