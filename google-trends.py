import requests
from requests.structures import CaseInsensitiveDict
import json
from wordpress_xmlrpc import Client,WordPressPost
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods.posts import NewPost

def create_post(host,username,password,contents,post_id=""):
    wp = Client(host, username, password)
    post = WordPressPost()
    post.title = "Google Trends India"
    post.content = contents
    post.post_status = 'publish'
    post.terms_names = {'category': ['Trending'],
    }

    if post_id != "":
        print("updating existing post: {}".format(post_id))
        i = wp.call(posts.EditPost(3795, post))
    else:
        print("Creating New Post with name Google Trends India")
        post.id = wp.call(NewPost(post))
        print("Post id: {}".format(post.id))

def getGtrends():
    url = "https://trends.google.com/trends/api/dailytrends?hl=en-USS&tz=530&geo=IN"

    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0"
    headers["Host"] = "trends.google.com"
    headers["Accept"] = "application/json, text/plain, */*"

    resp = requests.get(url, headers=headers)

    name = resp.content.decode('utf-8')
    n1 = name[6:]

    with open('gg.json','w') as file:
        file.write(n1)

    with open('gg.json', 'r') as file:
        json_data = json.load(file)

    final_json = {}
    counter = 0
    today_data = json_data['default']['trendingSearchesDays'][0]['trendingSearches']
    for j in today_data:
        title = j['title']['query'],
        formattedTraffic = j['formattedTraffic'],
        thumbnail_url = j['image']['imageUrl'],
        related_articles_list = []
        related_articles = j['articles']
        for k in related_articles:
            related_article = {
                "r_title":  k['title'],
                "r_description": k['snippet'],
                "r_link": k['url']
            }
            related_articles_list.append(related_article)
        final_json[str(counter)] = {
                "title": title,
                "traffic_volume": formattedTraffic,
                "thumbnail_url": thumbnail_url,
                "related_articles": related_articles_list
                }
        counter += 1

    yesterday_data = json_data['default']['trendingSearchesDays'][1]['trendingSearches']
    for j in yesterday_data:
        title = j['title']['query'],
        formattedTraffic = j['formattedTraffic'],
        thumbnail_url = j['image']['imageUrl'],
        related_articles_list = []
        related_articles = j['articles']
        for k in related_articles:
            related_article = {
                "r_title":  k['title'],
                "r_description": k['snippet'],
                "r_link": k['url']
            }
            related_articles_list.append(related_article)
        final_json[str(counter)] = {
                "title": title,
                "traffic_volume": formattedTraffic,
                "thumbnail_url": thumbnail_url,
                "related_articles": related_articles_list
                }
        counter += 1
    return final_json

def createWPTable():
    style = '''<!-- wp:html --><style>
            .gt-shadow-box {
            margin-top: 10px;
            margin-right: 0px;
            text-align: left;
            border: 1px solid;
            padding: 10px;
            box-shadow: 0 10px 6px -6px #777;
            margin-left: 0px;
            width: 100%;
            }
            .gt-col-md-3 {
            float: left;
            }
            .gt-col-md-3 img {
            border-radius: 5px;
            }
            .gt-col-md-9 {
            width: 100%;
            padding-left: 160px;
            }
            .gt-badge {
            display: inline-block;
            min-width: 10px;
            padding: 3px 7px;
            font-size: 12px;
            font-weight: 700;
            line-height: 1;
            color: #fff;
            text-align: center;
            white-space: nowrap;
            vertical-align: middle;
            background-color: #777;
            border-radius: 10px;
            }
            </style>\n'''
    output = '<p>updates every 5 mins</p><div>'
    output += '<ul>'

    p1 = json.dumps(final_json)
    for s in final_json.items():
        title = s[1]['title']
        traffic = s[1]['traffic_volume']
        thumbnail_url = s[1]['thumbnail_url']
        try:
            r_article1 = s[1]['related_articles'][0]['r_title']
        except IndexError as index_e:
            r_article1 = ""
        try:
            r_article1_link = s[1]['related_articles'][0]['r_link']
        except IndexError as index_e:
            r_article1_link = ""
        try:
            r_article1_description = s[1]['related_articles'][0]['r_description']
        except IndexError as index_e:
            r_article1_description = ""
        try:
            r_article2 = s[1]['related_articles'][1]['r_title']
        except IndexError as index_e:
            r_article2 = ""
        try:    
            r_article2_link = s[1]['related_articles'][1]['r_link']
        except IndexError as index_e:
            r_article2_link = ""
        try:    
            r_article2_description = s[1]['related_articles'][1]['r_description']
        except IndexError as index_e:
            r_article2_description = ""

        output += '<div class="gt-shadow-box">'
        output += '<div class="gt-col-md-3"><img src="{}" alt="{}" width="150" height="150" /></div>'.format(''.join(thumbnail_url),''.join(title))
        output += '<div class="gt-col-md-9"><strong style="font-size:20px;">{}</strong>: <span style="font-size:16px;" class="gt-badge">{} Searches</span>'.format(''.join(title),''.join(traffic))
        output += '<p><b>Related Articles</b></p>'
        output += '<ul><li><a href="{}" target="_blank">{}</a></br>{}</li>'.format(r_article1_link,r_article1,r_article1_description)
        output += '<li><a href="{}" target="_blank">{}</a></br>{}</li>'.format(r_article2_link,r_article2,r_article2_description)
        output += '</ul></div></div>'

    output += '</ul>'
    output += '</div><!-- /wp:html -->'

    WPTable = style+output
    return WPTable


# un-comment to post to wordpress
#create_post('wp-host''wp-user','wp-pass',final_output)
#create_post('wp_host','wp_user','wp_password',createWPTable(),post_id)
#create_post('https://onlineftp.in/xmlrpc.php','python-bot','M1Vxycp!95IbVwrbdYG2Qn(!',createWPTable(),post_id)

# prints the data in json format
print(json.dumps(getGtrends()))
