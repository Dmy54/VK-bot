import vk_api


class Vk:
    '''класс для упрощенной работы с vk_api и данными, которые можно получить с серверов ВК'''

    def __init__(self):
        self.token = self._get_token()
        self.destination_group_id = self._get_destination_group_id()
        self.source_group_id = self._get_source_group_id()
        self.vk_session = vk_api.VkApi(token=self.token)

    def _get_token(self):
        '''
        получение токена для подключения по vk_api
        :return возвращает строку
        '''
        f = open('./sources/vk_login', 'r')
        token = f.readline()[:-1]
        f.close()
        return token

    def _get_destination_group_id(self):
        '''
        получение id группы ВК, куда должно что-то приходить
        :return возвращает строку
        '''
        f = open('./sources/destination_group_id', 'r')
        id = f.readline()[:-1]
        f.close()
        return id

    def _get_source_group_id(self):
        '''
        получение id группы ВК, откуда брать информацию
        :return возвращает строку
        '''
        f = open('./sources/source_group_id', 'r')
        id = f.readline()[:-1]
        f.close()
        return id

    def get_posts(self, offset=0):
        '''
        получение постов из группы, id которой получено методом _get_source_group_id()
        :param offset необязательный параметр, по умолчанию = 0, принимает число.
        отвечает за смещение по стене сообщества вк
        :return возвращает структуру поста с серверов вк (см документацию https://vk.com/dev/ vk.wall.get)
        '''
        vk = self.vk_session.get_api()
        return vk.wall.get(
            owner_id=f'-{self.source_group_id}',
            offset=offset,
            count=100
        )

    def publish_post(self, post):
        '''
        публикация поста в группу, id которой получено методом _get_destination_group_id
        :param post обязательный параметр, принимает структуру, которую получаешь методом get_posts с серверов вк.
        :return: ничего
        '''
        vk = self.vk_session.get_api()
        if post.get('attachments'):
            attachments = self.get_attachments_string(post['attachments'])
        else:
            attachments = ''
        vk.wall.post(
            owner_id=f'-{self.destination_group_id}',
            message=post['text'],
            attachments=attachments
        )

    def delete_post(self, post):
        '''
        удаление поста из группы, id которой получено методом _get_source_group_id()
        :param post обязательный параметр, принимает структуру, которую получаешь методом get_posts с серверов вк.
        вместо этого можно использовать словарь {'id': 'id поста в группе'}
        :return: ничего
        '''
        vk = self.vk_session.get_api()
        vk.wall.delete(
                owner_id=f'-{self.source_group_id}',
                post_id=post['id']
            )

    def get_attachments_string(self, attachments):
        '''
        метод парсит структуру с серверов ВК и возвращает строку в формате, который нужен серверам ВК <type><owner_id>_<media_id>
        :param attachments: список, полученный с серверов вк со всей структурой постов из поля attachments
        :return: строка типа <type><owner_id>_<media_id>,<type><owner_id>_<media_id>
        '''
        result = ''
        for attachment in attachments:
            result += f"{attachment['type']}{attachment[attachment['type']]['owner_id']}_{attachment[attachment['type']]['id']},"
        return result
