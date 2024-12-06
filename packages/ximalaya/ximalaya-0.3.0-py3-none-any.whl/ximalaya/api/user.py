from typing import TypedDict
from ximalaya.client import XimalayaClient


class PubInfo(TypedDict):
    id: int
    title: str
    subTitle: str
    coverPath: str
    isFinished: bool
    isPaid: bool
    anchorUrl: str
    anchorNickname: str
    anchorUid: int
    playCount: int
    trackCount: int
    albumUrl: str
    description: str
    vipType: int
    albumSubscript: int


class PubPageInfo(TypedDict):
    totalCount: int
    pubInfoList: list[PubInfo]


class TrackInfo(TypedDict):
    trackId: int
    title: str
    trackUrl: str
    coverPath: str
    createTimeAsString: str
    albumId: int
    albumTitle: str
    albumUrl: str
    anchorUid: int
    anchorUrl: str
    nickname: str
    durationAsString: str
    playCount: int
    showLikeBtn: bool
    isLike: bool
    isPaid: bool
    isRelay: bool
    showDownloadBtn: bool
    showCommentBtn: bool
    showForwardBtn: bool
    isVideo: bool
    videoCover: str
    breakSecond: int
    length: int
    isAlbumShow: bool


class TrackPageInfo(TypedDict):
    totalCount: int
    trackInfoList: list[TrackInfo]


class SubscriptionPageInfo(TypedDict):
    privateSub: bool
    totalCount: int
    subscribeInfoList: list


class FollowingInfo(TypedDict):
    uid: int
    coverPath: str
    anchorNickName: str
    background: str
    description: str
    url: str
    grade: int
    mvpGrade: int
    gradeType: int
    trackCount: int
    albumCount: int
    followerCount: int
    followingCount: int
    isFollow: bool
    beFollow: bool
    isBlack: bool
    logoType: int
    ptitle: str


class FollowingPageInfo(TypedDict):
    totalCount: int
    followInfoList: list[FollowingInfo]


class FansInfo(TypedDict):
    uid: int
    coverPath: str
    anchorNickName: str
    background: str
    url: str
    grade: int
    mvpGrade: int
    gradeType: int
    trackCount: int
    albumCount: int
    followerCount: int
    followingCount: int
    isFollow: bool
    beFollow: bool
    isBlack: bool
    logoType: int


class FansPageInfo(TypedDict):
    totalCount: int
    fansInfoList: list[FansInfo]


class UserDetailedInfo(TypedDict):
    uid: int
    pubPageInfo: PubPageInfo
    trackPageInfo: TrackPageInfo
    subscriptionPageInfo: SubscriptionPageInfo
    followingPageInfo: FollowingPageInfo


class UserBasicInfo(TypedDict):
    uid: int
    nickName: str
    cover: str
    background: str
    isVip: bool
    constellationType: int
    personalSignature: str
    personalDescription: str
    fansCount: int
    gender: int
    birthMonth: int
    birthDay: int
    province: str
    city: str
    anchorGrade: int
    mvpGrade: int
    anchorGradeType: int
    isMusician: bool
    anchorUrl: str
    logoType: int
    followingCount: int
    tracksCount: int
    albumsCount: int
    albumCountReal: int
    userCompany: str
    qualificationGuideInfos: list[str]


def get_user_basic_info(client: XimalayaClient, uid: int) -> UserBasicInfo:
    return client.request(f'/revision/user/basic?uid={uid}')['data']


def get_user_detailed_info(client: XimalayaClient, uid: int):
    return client.request(f'/revision/user?uid={uid}')['data']
