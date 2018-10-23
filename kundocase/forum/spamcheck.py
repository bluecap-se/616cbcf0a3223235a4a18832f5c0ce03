import requests


class SpamCheck:

    def __init__(self, object):
        self.obj = object

    def has_spam(self):
        """
        Validates if object contains spam

        :param object: Django model object, of `Question` or `Answer` type
        :return: Boolean, True if object has spam
        """
        return self.long_texts_are_spam() or \
               self.long_titles_are_spam() or \
               self.all_users_from_domain_are_spam() or \
               self.some_usernames_are_spam() or \
               self.words_in_text_are_spam() or \
               self.known_spammers_are_spam()

    def long_texts_are_spam(self):
        return len(self.obj.content) > 200

    def long_titles_are_spam(self):
        return hasattr(self.obj, 'title') and len(self.obj.title) > 200

    def all_users_from_domain_are_spam(self):
        bad_domains = ["spam.com", "universitydiploma.com"]
        domain = self.obj.user_email.split("@")[1]
        return domain in bad_domains

    def some_usernames_are_spam(self):
        bad_names = ["thord", "curt", "madicken"]
        name = self.obj.user_name

        for bad_name in bad_names:
            if name in bad_name:
                return True

        return False

    def words_in_text_are_spam(self):
        bad_words = ["spam", "universitydiploma"]
        text = self.obj.content

        for word in bad_words:
            if word in text:
                return True

        return False

    def known_spammers_are_spam(self):
        email = self.obj.user_email
        url = "https://www.stopforumspam.com/api?f=json&email=" + email
        response = requests.get(url, timeout=2)
        data = response.json()

        return bool(data and data["success"] and data["email"]["appears"])
