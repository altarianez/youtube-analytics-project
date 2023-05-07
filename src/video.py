import os

from googleapiclient.discovery import build


class Video:
    youtube = None
    """Класс для видео"""

    def __init__(self, video_id: str):
        """
        Инициализируемся м задаем необходимые параметры
        """
        Video.youtube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))
        self.data = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                id=video_id
                                                ).execute()

        self.video_id = video_id
        self.video_name = self.data['items'][0]['snippet']['title']
        self.video_url = f'https://youtu.be/{self.video_id}'
        self.video_views = self.data['items'][0]['statistics']['viewCount']
        self.video_likes = self.data['items'][0]['statistics']['likeCount']

    def __str__(self):
        """
        Возвращает информацию об экземпляре класса для пользователя
        """
        return f'{self.video_name}'


class PLVideo(Video):
    """
        Класс для видео плейлиста
        """
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_data = super().youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()

        self.video_url = f'https://www.youtube.com/watch?v={self.video_id}&list={self.playlist_id}'
        self.playlist_url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

