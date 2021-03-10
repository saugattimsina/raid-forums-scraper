import re


from bs4 import BeautifulSoup
import requests




def forums_browser(url):


    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    try:
        response = requests.get(url, headers=headers)
        # print(response.content.decode("utf-8"))
    except requests.exceptions.RequestException as e:
        print(e)

    return response.content


def browser_with_page_number(url,page):

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
    }

    params = (
        ('page', f'{page}'),
    )

    response = requests.get(url, headers=headers, params=params)

    return response.content


def url_generator(url_path):
    path = "https://raidforums.com/"+url_path
    return path


def forums_path_finder(base_url):

    required_urls1 = []

    home_page = forums_browser(base_url)
    soup = BeautifulSoup(home_page, 'html.parser')
    required_context = soup.find(class_="group")
    links_table = soup.find_all(class_= "forums__bit tborder")
    links_all = links_table[0].find_all('a', href=True)
    for link in links_all:
        link = link['href']
        if link.startswith("Forum"):
            required_urls1.append(link)
            
    required_urls1  = list(dict.fromkeys(required_urls1))
    required_urls1.pop(0)
    required_urls1.pop(1)
    # print(required_urls1)
    return required_urls1


def threads_title_and_url_finder(forum_content):
    
    

    forum_thread_infos_odd = forum_content.find_all(class_ = "trow1 forumdisplay_regular")
    forum_thread_infos_even = forum_content.find_all(class_ = "trow2 forumdisplay_regular")

    thread_name_and_url = []
    for i,content in enumerate(forum_thread_infos_even):
        details ={}
        if i == 0:
            pass
        elif i%2 == 1:
            thread_name = content.find(class_="forum-display__thread-name")
            thread_url = thread_name["href"]
            thread_subject = content.find(class_ = "forum-display__thread-subject").text
            details[thread_subject] = thread_url
            thread_name_and_url.append(details)


    for i,content in enumerate(forum_thread_infos_odd):
        details ={}
        if i == 0:
            pass
        elif i%2 == 1:

            thread_name = content.find(class_="forum-display__thread-name")
            thread_url = thread_name["href"]
            thread_subject = content.find(class_ = "forum-display__thread-subject").text
            details[thread_subject] = thread_url
            thread_name_and_url.append(details)

    return thread_name_and_url


def thread_title_and_url_finder_navigator(forum_name):
    all_page_collector = {}

    url = url_generator(forum_name)
    forum_info = forums_browser(url)
    forum_content = BeautifulSoup(forum_info, 'html.parser')
    content_data = threads_title_and_url_finder(forum_content)
    all_page_collector["page1"] = content_data

    number_of_pages = pages_finder_forum(forum_content)
    if not number_of_pages == "N/A":
        for page in range(2,number_of_pages+1):
            page_content = browser_with_page_number(url,page)
            forum_content = BeautifulSoup(page_content, 'html.parser')
            content_data = threads_title_and_url_finder(forum_content)
            all_page_collector["page"+str(page)] = content_data
            # print(all_page_collector)
            if page == 3:
                break
 

    return all_page_collector


def pages_finder_forum(soup):
    try:
        pages = int(soup.find(class_ = "pages").text.split("(")[1].split(")")[0])
        print(pages)
        return pages
    except Exception as e:
        return "N/A"


def thread_data_finder(soup):
    data_collector = []
    content1 = soup.find(id ="posts")
    all_post_ids = re.findall('post_[0-9]*"',str(content1))
    for post in all_post_ids:
        info_dict= {}
        post_id = post.split('"')[0]
        print(post)
        individual_post = content1.find(id = post_id)
        # date_post
        date_posted = individual_post.find(class_ = "post_date").text
        info_dict["date_time"] = date_posted
        #username
        username = individual_post.find(class_ = "post__user-profile largetext").text
        info_dict["username"]= username
        # #user title
        title = individual_post.find(class_ = "post__user-title").text.strip()
        info_dict["user_title"] = title
        print(title)
        contents = individual_post.find(class_ = "mycode_align")
        if contents:
            texts_in_the_post = contents.text.strip()
        else:
            contents = individual_post.find(class_ = "post_body scaleimages")
            texts_in_the_post = contents.text.strip()
        #contents
        info_dict["text_content"] = texts_in_the_post
        data_collector.append(info_dict)
    return data_collector


def pages_finder_thread(soup):
    try:
        pages = soup.find(id = "thread-navigation")
        pages_detail = pages.text
        total_page_number = int(re.findall("Pages..[0-9]*",pages_detail)[0].split("(")[1])
        return total_page_number
    except Exception as e:  
        return "N/A"


def thread_data_finder_navigator(thread_path,page_title):
    all_page_collector = {}
    url = url_generator(thread_path)
    page_content = forums_browser(url)
    forum_content = BeautifulSoup(page_content, 'html.parser')
    page_data = thread_data_finder(forum_content)
    all_page_collector["page_url"] = thread_path
    all_page_collector["page_title"] = page_title
    all_page_collector["page1"] = page_data

    number_of_pages = pages_finder_thread(forum_content)
    print("number of pages in thread are",number_of_pages)
    if not number_of_pages == "N/A":
        for page in range(2,number_of_pages+1):
            page_content = browser_with_page_number(url,page)
            forum_content = BeautifulSoup(page_content, 'html.parser')
            content_data = thread_data_finder(forum_content)
            all_page_collector["page"+str(page)] = content_data
            # print(all_page_collector)
            if page == 3:
                break
    
    return all_page_collector



if __name__ == "__main__":

    all_forums = forums_path_finder("https://raidforums.com/")
    titles_and_urls = thread_title_and_url_finder_navigator(all_forums[3])

    page_link = list(titles_and_urls.get("page1")[0].values())[0]
    page_title = list(titles_and_urls.get("page1")[0].keys())[0]

    print(page_link)

    posts_and_comments = thread_data_finder_navigator(page_link,page_title)
    print(posts_and_comments)
