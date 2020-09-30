import scrapy
from scrapy.http import HtmlResponse
from les_8_scrapy.items import Les8ScrapyItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy


class IgmSpider(scrapy.Spider):
    name = 'igm'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    insta_login = ''
    insta_pwd = ''
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_users = ['it.cokr', 'molcokr_kld', 'molcokr_kzn']
    followers_of_user_hash = 'c76146de99bb02f6415203be841dd25a'
    following_of_user_hash = 'd04b0a864b4b54837c0d870b0e77e076'
    graphql_url = 'https://www.instagram.com/graphql/query/?'

    def parse(self, response:HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login,
                      'enc_password': self.insta_pwd
                      },
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:  # Проверяем ответ после авторизации
            for parse_user in self.parse_users:
                yield response.follow(
                    # Переходим на желаемую страницу пользователя. Сделать цикл для кол-ва пользователей больше 2-ух
                    f'/{parse_user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': parse_user}
                )

    def user_data_parse(self, response:HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)       #Получаем id пользователя
        # Формируем словарь для передачи даных в запрос
        variables = {
            'id': user_id,
            'first': 24
        }
        # Формируем ссылку для получения данных о подписчиках (followers)
        url_posts = f'{self.graphql_url}query_hash={self.followers_of_user_hash}&{urlencode(variables)}'
        yield response.follow(
            url_posts,
            callback=self.followers_of_user_parse,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': deepcopy(variables)
            }
        )
        # Формируем ссылку для получения данных о подписках (following)
        url_posts = f'{self.graphql_url}query_hash={self.following_of_user_hash}&{urlencode(variables)}'
        yield response.follow(
            url_posts,
            callback=self.following_of_user_parse,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': deepcopy(variables)
            }
        )

    def followers_of_user_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        # Если есть следующая страница
        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']   #Новый параметр для перехода на след. страницу
            url_followers = f'{self.graphql_url}query_hash={self.followers_of_user_hash}&{urlencode(variables)}'
            yield response.follow(
                url_followers,
                callback=self.followers_of_user_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        followers = j_data.get('data').get('user').get('edge_followed_by').get('edges')
        for follower in followers:
            item = Les8ScrapyItem(
                type='follower',
                parse_username=username,
                user_id_of_obj=follower['node']['id'],
                photo_of_obj=follower['node']['profile_pic_url'],
                username_of_obj=follower['node']['username']
            )
            yield item

    def following_of_user_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        # Если есть следующая страница
        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']   #Новый параметр для перехода на след. страницу
            url_following = f'{self.graphql_url}query_hash={self.following_of_user_hash}&{urlencode(variables)}'
            yield response.follow(
                url_following,
                callback=self.following_of_user_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        followings = j_data.get('data').get('user').get('edge_follow').get('edges')
        for following in followings:
            item = Les8ScrapyItem(
                type='following',
                parse_username=username,
                user_id_of_obj=following['node']['id'],
                photo_of_obj=following['node']['profile_pic_url'],
                username_of_obj=following['node']['username']
            )
            yield item


    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
