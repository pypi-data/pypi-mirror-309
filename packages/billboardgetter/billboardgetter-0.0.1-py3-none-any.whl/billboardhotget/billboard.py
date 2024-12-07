import requests
from bs4 import BeautifulSoup

def scrape_hot100():
    """
    Billboard Hot 100の楽曲名をスクレイピングする。

    Returns:
        list: 楽曲名のリスト。
    """
    url = "https://billboard-japan.com/charts/detail?a=hot100"

    try:
        # ページを取得
        response = requests.get(url)
        response.raise_for_status()  # ステータスコードのチェック

        # BeautifulSoupでHTMLを解析
        soup = BeautifulSoup(response.text, 'html.parser')

        # 楽曲名を含む要素を抽出
        songs = []
        for song_tag in soup.find_all(class_='musuc_title'):
            songs.append(song_tag.text.strip())

        return songs
    except requests.exceptions.RequestException as e:
        print(f"HTTPリクエストエラー: {e}")
        return []
    except Exception as e:
        print(f"その他のエラー: {e}")
        return []

def display_songs(num_songs=None):
    """
    指定した数の楽曲リストを表示する。

    Args:
        num_songs (int, optional): 表示する楽曲の数。
    """
    songs = scrape_hot100()

    if not songs:
        print("楽曲を取得できませんでした。")
        return

    # 指定された数の楽曲を取得
    songs_to_display = songs[:num_songs] if num_songs else songs

    print(f"取得した楽曲リスト ({len(songs_to_display)}件):")
    for i, song in enumerate(songs_to_display, start=1):
        print(f"{i}. {song}")
