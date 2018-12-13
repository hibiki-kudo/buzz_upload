#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import time

import tweepy


def tweet_rank():
    # アクセス処理
    # auth = tweepy.OAuthHandler(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"])
    # auth.set_access_token(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_SECRET"])
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    # APIインスタンスを作成
    api = tweepy.API(auth)
    # 検索キーワード入力
    q = "min_retweets:9000 min_faves:2000 lang:ja"  # since: + str(datetime.date.today())
    # 検索件数
    count = 40000
    # 検索
    search_results = api.search(q=q, count=count)
    # 結果をテキストに保存
    text = open("scr_text.txt", "w", encoding="UTF-8")

    userdata = []
    tweet_image = []

    counter = 0

    # データ取得処理
    for result in search_results:
        flag = 0
        # 検索読み込み待機時間
        if counter == 0:
            time.sleep(1)

        texts = list(result.text)

        if "https://t.co/" in result.text:
            for j in range(23):
                texts.pop()
                flag = 1

        if 'media' in result.entities:
            for i in range(len(result.extended_entities["media"])):
                if result.extended_entities["media"][0].get("video_info") != None:
                    tweet_image.append(result.extended_entities["media"][0]["video_info"]["variants"][0]["url"])
                else:
                    tweet_image.append(result.extended_entities['media'][i]['media_url'])

        if not "公式" in result.user.name and not "公式" in result.user.description and not result.user.verified and not "official" in \
                                                                                                                     result.user._json[
                                                                                                                         'screen_name'] and result.user.followers_count - result.user.friends_count <= 10000:  # and abs(result.favorite_count-result.retweet_count) <= 5000
            # if not ("名様" in result.text and  "&RT" in result.text and "応募完了" in result.text and "抽選" in result.text):
            userdata.append(
                [result.user._json['screen_name'], result.id, result.user.name, ''.join(texts), result.created_at,
                 result.favorite_count, result.user._json['profile_image_url_https'], copy.deepcopy(tweet_image),
                 result.favorite_count + (result.retweet_count * 3), result.retweet_count])
            # print(str(userdata[counter])+"\n")
            # print(result.user.description)
            counter += 1
        # データをテキストに出力
        # text.write(str(userdata[counter]) + "\n")
        tweet_image.clear()

    counter = 0

    text.write(
        '<img src="https://buzz-matome.xyz/wp-content/uploads/2018/11/今日の人気ツイート-まとめ.png" alt="" width="560" height="315" class="alignnone size-full wp-image-329" />\n')
    text.write("バズったツイートランキング！！\n")
    text.write("このランキングは1日のバズったランキングを集めた記事です(*´∀｀)\n")
    userdata.sort(key=lambda x: x[8])
    userdata.reverse()

    # データのファボランキングをし、埋め込みHTMlをテキストに保存する処理
    for result in userdata:

        if counter <= 2:
            text.write('<h2>ランキング' + str(counter + 1) + "位</h2>\n")
        else:
            text.write('<h3>ランキング' + str(counter + 1) + "位</h3>\n")

        text.write('<div style="background-color:gainsboro;"><font size="4" color="#dc143c">点数:' + str(
            userdata[counter][8]) + "点</font>\n")

        text.write('<img src="' + str(result[6]) + '"alt="アイコン"' + ' align="left"/>')
        text.write('<a href="http://twitter.com/' + str(result[0]) + '"')
        text.write(' target="_blank">@' + str(result[0]) + "</a>\n" + str(result[2]) + "<br>\n\n")
        text.write('<font size="5" color="#000000">' + str(result[3]) + "</font>\n")
        text.write('<a href="http://twitter.com/' + str(result[0]) + '/status/' + str(
            result[1]) + '" target="_blank">ツイートに移動</a>\n')
        text.write('\n')

        # print(result[7])
        if len(result[7]) != 0:
            for i in range(len(result[7])):
                print(result[7][i])
                if "video" in result[7][i]:
                    text.write('<video controls src="')
                    text.write(str(result[7][i]))
                    text.write('"alt="' + '" /></video>\n')
                else:
                    text.write('<img src="')
                    text.write(str(result[7][i]))
                    text.write('"alt="' + '" />\n')

        text.write('<a href="http://twitter.com/intent/tweet?in_reply_to=' + str(
            result[1]) + '&original_referer=https://buzz-matome.xyz/" target="_blank">リプライ</a>&ensp;')
        text.write('<a href="http://twitter.com/intent/favorite?tweet_id=' + str(
            result[1]) + '&original_referer=https://buzz-matome.xyz/" target="_blank">♡:' + str(
            result[5]) + "</a>&ensp;")
        text.write('<a href="http://twitter.com/intent/retweet?tweet_id=' + str(
            result[1]) + '&original_referer=https://buzz-matome.xyz/" target="_blank">RT:' + str(
            result[9]) + "</a>&ensp;")
        text.write("</div>\n")

        counter += 1

    print(userdata)
    text.close()
