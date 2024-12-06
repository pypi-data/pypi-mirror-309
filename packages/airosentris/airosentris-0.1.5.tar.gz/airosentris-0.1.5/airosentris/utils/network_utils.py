import json

import requests


def fetch_data(url, token):

    return mock_data()

    """Fetch data from the given URL using the provided token."""
    headers = {'Authorization': f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to load data: {response.status_code} - {response.text}")

    return response.text


def mock_data():
    data = {
        "success": True,
        "data": [
            {
                "comment_id": 17943412448833336,
                "comment_text": "Sebelum bikin gorong\"seharusnya teknisi lapangan itu survey jalan mana yg harus digali. .gak asal gali aja dipikir donk dikit\"pipa PDAM bocor alasan gak berguna sekali duakali oke lah sudah hampir 1th alasan kok podo ae",
                "comment_date": "2024-07-16 13:06:28",
                "username": "miftachul_retna",
                "user_id": 1679854023,
                "replies": [
                    {
                        "reply_id": 18051102328815550,
                        "reply_text": "@miftachul_retna bener kak gara2 ada gorong hanya bikin warga sak SBY resah aja,,, gorong2 gk berguna hanya bikin masalah saja 😢😢😢",
                        "reply_date": "2024-07-20 03:55:17",
                        "username": "yuliana_saskia",
                        "user_id": 5604089480
                    },
                    {
                        "reply_id": 18037749367974156,
                        "reply_text": "@yuliana_saskia selamat siang bu silahkan DM kami data pelanggan alamat lengkap utk segera kami tindaklanjuti pengaduannya -w",
                        "reply_date": "2024-07-20 07:37:14",
                        "username": "pdamsuryasembada",
                        "user_id": 2019411880
                    }
                ],
                "total_reply": 2,
                "label_sentiment": "positive"
            },
            {
                "comment_id": 17869819218117332,
                "comment_text": "Pak PDAM yg terhormat mau sampai kapan air diwilayah gembong sekalaj ini seperti ini ini air got lho pak,sudah dari 3 hari yg lalu warga gembong yg air ya keluar air got laporan tapi kok masih belum ada perbaikan,klu bayar telat saja sehari denda langsung tapi klu keluhan lemot sekali penanganannya",
                "comment_date": "2024-07-09 23:04:44",
                "username": "indicantik25",
                "user_id": 60555859626,
                "replies": [
                    {
                        "reply_id": 17939344316846030,
                        "reply_text": "@indicantik25 Selamat pagi bu Indi, mohon maaf atas ketidaknyamanannya. Baik, kami follow up ke petugas terkait. -w",
                        "reply_date": "2024-07-12 02:50:26",
                        "username": "pdamsuryasembada",
                        "user_id": 2019411880
                    }
                ],
                "total_reply": 1,
                "label_sentiment": "negative"
            }
        ],
        "message": "Successfully fetched 2 comments for post C9MKTnUvtRv"
    }

    return json.dumps(data)