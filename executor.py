from script import *

import database_connection



all_forums = forums_path_finder("https://raidforums.com/")
titles_and_urls = thread_title_and_url_finder_navigator(all_forums[3])

page_link = list(titles_and_urls.get("page1")[0].values())[0]
page_title = list(titles_and_urls.get("page1")[0].keys())[0]

# print(page_link)

posts_and_comments = thread_data_finder_navigator(page_link,page_title)
# print(posts_and_comments)

posts_and_comments
page_title = posts_and_comments["page_title"]
page_url = posts_and_comments["page_url"]

#0 th index for post
page_infos = posts_and_comments["page1"][0]

date_time = page_infos["date_time"]
text_content = page_infos["text_content"]
user_title = page_infos["user_title"]
username = page_infos["username"]

conn = database_connection.connection_creator()
cur = conn.cursor()

# cur.execute("INSERT INTO posts(page_url,page_title,text_content,date_time,username,user_title) VALUES(%s,%s,%s,%s,%s,%s)",(page_url,page_title,text_content,date_time,username,user_title))

# conn.commit()

cur.execute("SELECT post_id FROM posts;")
info = cur.fetchall()
post_id = info[-1][0]


keys = list(posts_and_comments.keys())
for key in range(2,len(keys)):
    if keys[key] == "page1":
        for i in range(1,len(posts_and_comments["page1"])):
            page1 = posts_and_comments["page1"]
            data = page1[i]
            date_time = data["date_time"]
            text_content = data["text_content"]
            user_title = data["user_title"]
            username = data["username"]
            cur.execute("INSERT INTO comments (text_content,date_time,username,user_title,post_id) VALUES(%s,%s,%s,%s,%s)",(text_content,date_time,username,user_title,post_id))
            conn.commit()
    else:
        print(key)
        for i in range(len(posts_and_comments["page"+str(key)])):
            page = posts_and_comments["page"+str(key)]
            data = page[i]
            date_time = data["date_time"]
            text_content = data["text_content"]
            user_title = data["user_title"]
            username = data["username"]
            cur.execute("INSERT INTO COMMENTS (text_content,date_time,username,user_title,post_id) VALUES (%s,%s,%s,%s,%s)",(text_content,date_time,username,user_title,post_id))
            conn.commit()
conn.close()