from src.channel import Channel


class Video:

    def __init__(self, video_id):
        self.id_vidio = video_id
        self.youtube = Channel.get_service()
        self.video_id = video_id
        try:
            video_response = self.youtube.videos().list(
                part='snippet,statistics,contentDetails,topicDetails',
                id=video_id
            ).execute()['items'][0]
        except IndexError:
            self.title = None
            self.count = None
            self.like_count = None
            self.comment_count = None
        else:
            self.title = str(video_response['snippet']['title'])
            self.count = str(video_response['statistics']['viewCount'])
            self.like_count = int(video_response['statistics']['likeCount'])
            self.comment_count = int(video_response['statistics']['commentCount'])

    def __repr__(self):
        return f'{self.title}'


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __repr__(self):
        return f'{self.title}'
