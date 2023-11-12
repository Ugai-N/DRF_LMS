import re

from rest_framework import serializers


class OnlyYoutubeValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):  # value приходит в виде словаря
        pattern = r"(?:https?:\/\/|ftps?:\/\/|www\.)(?:(?![.,?!;:()]*(?:\s|$))[^\s]){2,}"
        youtube_pattern = \
            r"(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
        field_value = dict(value).get(self.field)
        if field_value:
            urls_in_field = re.findall(pattern, field_value)
            for url in urls_in_field:
                if not bool(re.match(youtube_pattern, url)):
                    raise serializers.ValidationError('Недопустимо указание ссылок на любые источники, кроме Youtube')
            # for url in urls_in_field:
            #     if "youtube" in url:
            #         continue
            #     else:
            #         raise serializers.ValidationError('Недопустимо указание ссылок на любые источники, кроме Youtube')
