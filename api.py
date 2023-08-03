import requests


class Api:

    def __init__(self, token: str, user_token: str):
        self.token = token
        self.user_token = user_token

    def send(self, peer_id, text):
        return requests.get(url=f'https://api.vk.com/method/messages.send?v=5.103'
                                f'&access_token={self.token}&peer_id={peer_id}&message={text}'
                                f'&random_id=0').json()

    def edit(self, peer_id, message_id, text):
        return requests.get(url=f'https://api.vk.com/method/messages.edit?v=5.103'
                                f'&access_token={self.token}&peer_id={peer_id}&message={text}&message_id={message_id}').json()

    def reply_to(self, peer_id, message_id, photos):
        return requests.get(url=f'https://api.vk.com/method/messages.send?v=5.103'
                                f'&access_token={self.token}&peer_id={peer_id}'
                                f'&random_id=0&reply_to={message_id}&attachment={photos}').json()

    def send_user(self, user_id, text):
        return requests.get(url=f'https://api.vk.com/method/messages.send?v=5.103'
                                f'&access_token={self.token}&user_id={user_id}&message={text}'
                                f'&random_id=0')

    def send_attachment(self, peer_id, text, attachments, keyboard):
        return requests.get(url=f'https://api.vk.com/method/messages.send?v=5.103'
                                f'&access_token={self.token}&peer_id={peer_id}&message={text}&'
                                f'attachment={attachments}&random_id=0&keyboard={keyboard}').json()

    def send_keyboard(self, peer_id, keyboard, message, attachment=None):
        if attachment is None:
            return requests.get(url=f'https://api.vk.com/method/messages.send?v=5.103'
                                    f'&access_token={self.token}&message={message}&'
                                    f'peer_id={peer_id}&keyboard={keyboard}'
                                    f'&random_id=0').json()
        else:
            return requests.get(url=f'https://api.vk.com/method/messages.send?v=5.103'
                                    f'&access_token={self.token}&message={message}&'
                                    f'peer_id={peer_id}&keyboard={keyboard}'
                                    f'&random_id=0&attachment={attachment}').json()

    def block_user(self, user_id, group_id):
        requests.get(url=f'https://api.vk.com/method/groups.ban?v=5.103'
                         f'&access_token={self.user_token}&owner_id={user_id}&group_id=P{group_id}')

    def edit_message_keyboard(self, text, message_id, keyboard, peer_id):
        requests.get(url='https://api.vk.com/method/messages.edit?v=5.103'
                         f'&access_token={self.token}&peer_id={peer_id}&message_id={message_id}&message={text}&keyboard={keyboard}')
