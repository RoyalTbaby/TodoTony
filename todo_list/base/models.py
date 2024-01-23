import json
import requests
from django.db import models
from django.contrib.auth.models import User
import logging


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    client_info = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    uuid_document = models.CharField(max_length=30, null=True)
    signed_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']

    def save(self, *args, **kwargs):

        if self.pk is None:
            super(Task, self).save(*args, **kwargs)


            url = "https://api.pandadoc.com/public/v1/documents"

            payload = json.dumps({
                "name": self.title,
                "template_uuid": "bPiVRZsMpe59w3Shcj6Y3D",
                "recipients": [
                    {
                        "email": self.user.email,
                        "first_name": self.user.first_name,
                        "last_name": self.user.last_name,
                        "role": "Client"
                    }
                ],
                "fields": {
                    "data_from_client": {
                        "value": "PandaDoc green"
                    }
                },
                "tokens": [
                    {
                        "name": "Description",
                        "value": self.description
                    }
                ]
            })
            headers = {
                'Authorization': 'API-Key c85ef66ec16cce8b95effffb960edfab08e0096f',
                'Content-Type': 'application/json',
                'Cookie': 'incap_ses_1463_2627658=FcM9az4s3Xccz1GXfp9NFEZXrGUAAAAAJ9Zg3eOKcqNm4I5l8Hmq2A==; nlbi_2627658=v3FTLiZSSlKwrv+Bsee3lAAAAACzEbAmFxEHmA0FPXR83+TY; visid_incap_2627658=1jfjxxqnTam9IVyQJ7X2rUpKqGUAAAAAQUIPAAAAAADN4zMpEAwEij2OblGeCKbH; AWSALB=bdPlHYUWQiZpzwUTdimoFRBYU4OAxxIBdOUxWlo6nesVXmZfrYlRSk0tZ6ysU8WOZzYo2/qhj46nbTN7wvtCK3AiuE7+Y0G16iXJzIcLjwwy2fdCx3m6VT+wA9nw; AWSALBCORS=bdPlHYUWQiZpzwUTdimoFRBYU4OAxxIBdOUxWlo6nesVXmZfrYlRSk0tZ6ysU8WOZzYo2/qhj46nbTN7wvtCK3AiuE7+Y0G16iXJzIcLjwwy2fdCx3m6VT+wA9nw'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            result = json.loads(response.text)

            self.uuid_document = result['uuid']
            super(Task, self).save(*args, **kwargs)



            url = f"https://api.pandadoc.com/public/v1/documents/[{result['uuid']}/send"

            payload = json.dumps({
                "message": "Hello! This document was sent from the PandaDoc API.",
                "silent": False
            })

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)

            logging.info(f'The task with{self.title} has been logged in')


        else:
            super(Task, self).save(*args, **kwargs)




