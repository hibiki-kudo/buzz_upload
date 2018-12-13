#!/usr/bin/env python
# -*- coding: utf-8 -*-

import send_favorank
import tweet_rank

# now = datetime.now().hour
# print(now)
# while True:
#     now = datetime.now().hour
#     if 6 <= now:
#         tweet_rank.tweet_rank()
#         print("ツイート収集完了")
#
#         send_favorank.send_favorank()
#         print("ブログ投稿完了")
#
#         time.sleep(65000)

if __name__ == "__main__":
    tweet_rank.tweet_rank()
    print("ツイート収集完了")

    send_favorank.send_favorank()
    print("ブログ投稿完了")
