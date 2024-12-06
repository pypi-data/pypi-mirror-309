from typing import TypedDict, Iterator

from ximalaya.client import XimalayaClient


class SubscriptInfo(TypedDict):
    albumSubscriptValue: int
    url: str


class AlbumInfo(TypedDict):
    albumId: int
    albumPlayCount: int
    albumTrackCount: int
    albumCoverPath: str
    albumTitle: str
    albumUserNickName: str
    anchorId: int
    anchorGrade: int
    mvpGrade: int
    isDeleted: bool
    isPaid: bool
    isFinished: int
    anchorUrl: str
    albumUrl: str
    intro: str
    vipType: int
    logoType: int
    subscriptInfo: SubscriptInfo
    albumSubscript: int


class AlbumsResponse(TypedDict):
    currentUid: int
    total: int
    pageNum: int
    pageSize: int
    albums: list[AlbumInfo]


class AlbumsResponsePagination(Iterator):
    client: XimalayaClient
    path: str
    page_num: int

    def __init__(self, client: XimalayaClient, path: str):
        self.client = client
        self.path = path
        self.page_num = 1

    def __next__(self) -> list[AlbumInfo]:
        res: AlbumsResponse = self.client.request(f'{self.path}&pageNum={self.page_num}')['data']
        albums = res['albums']

        if len(albums) == 0 or res['total'] == 0:
            raise StopIteration()

        self.page_num += 1

        return albums


def get_category_albums(client: XimalayaClient, category_id: int, page_size: int = 56, sort_by: int = 1) -> AlbumsResponsePagination:
    return AlbumsResponsePagination(client=client, path=f'/revision/category/v2/albums?pageSize={page_size}&sort={sort_by}&categoryId={category_id}')
