from django.db.models import QuerySet

class EmptySet(QuerySet):
    def __and__(self, __s):
        return self.__or__(__s)