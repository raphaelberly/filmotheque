import mailjet_rest


class Mailer(object):

    def __init__(self, api_key, secret_key):
        self.client = mailjet_rest.Client(auth=(api_key, secret_key), version='v3.1')

    def send(self, data):
        return self.client.send.create(data=data)
