from .models import *
from django.db.models import Q

OPERATORS = [
    'OR',
    'NOT'
]


def process_query(query: str):
    """
    process the boolean search query from left to right where
      no operator between tags is treated as ``AND``,
      ``OR`` functions as a boolean ``OR``,
      ``NOT`` excludes the tag following the operator from results.
      Parentheses are not supported and will be treated as malformed query (return empty qset).
    """
    if '(' in query or ')' in query or 'AND' in query:
        return return_empty()

    tokens = query.split(' ')

    and_tags = Tag.objects.none()
    or_tags = []
    exclude_tags = Tag.objects.none()

    processed_tags = []
    

    for i in range(len(tokens)):
        
        if tokens[i] in processed_tags:
            continue

        if tokens[i] == 'OR':
            try:
                arg1 = tokens[i-1]
                arg2 = tokens[i+1]
            except IndexError:
                return return_empty()

            if arg1 in processed_tags or arg2 in processed_tags:
                continue
            
            if arg1 in OPERATORS or arg2 in OPERATORS:
                return return_empty()

            try:
                if tokens[i-2] == 'NOT':
                    return return_empty()
            except IndexError:
                pass

            # ...
            or_tags.append(generate_or(arg1, arg2))

            processed_tags += [arg1, arg2]


        elif tokens[i] == 'NOT':
            try:
                arg = tokens[i+1]
            except IndexError:
                return return_empty()

            if arg in OPERATORS:
                return return_empty()

            # ...
            exclude_tags |= Tag.objects.filter(name=arg)

            processed_tags.append(arg)

        else:
            try:
                if tokens[i+1] == 'OR':
                    continue
            except IndexError:
                pass

            # ...
            and_tags |= Tag.objects.filter(name=tokens[i])

            processed_tags.append(tokens[i])

    return or_tags, and_tags.order_by('name'), exclude_tags.order_by('name')
            


def return_empty():
    return [], Tag.objects.none(), Tag.objects.none()



def generate_or(arg1, arg2):
    return Tag.objects.filter(name=arg1).order_by('name'), Tag.objects.filter(name=arg2).order_by('name')

            

            
            

    

    