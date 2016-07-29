from flask import request


class ListStyle(object):
    @staticmethod
    def list(select, request):
        '''Returns a styled list from the data passed. The pagination style
        is defined in the request data. The default values of `number` and
        `page` will be 10 and 1, respectively. If these parameters are passed
        as data in the request, then the values will be updated accordingly.

        Keyword arguments:
        select -- A database query of data.
        request -- A request of some type.
        '''
        number = 10
        page = 1

        for key in request.values:
            if key == 'number':
                number = int(request.values.get('number'))
            elif key == 'page':
                page = int(request.values.get('page'))

        '''Call peewee paginate method on the query.'''
        arr = []
        for i in select.paginate(page, number):
            arr.append(i.to_dict())

        '''By default, `next_page_path` and `prev_page_path` are None.'''
        next_page_path = None
        prev_page_path = None
        base_path = request.base_url + "?page="
        end_path = "&number=" + str(number)

        '''Update `next_page_path` and `prev_page_path` if there is data on
        either a next or previous page from the pagination.
        '''
        if len(arr) == number:
            next_page_path = base_path + str(page + 1) + end_path
        if page > 1:
            prev_page_path = base_path + str(page - 1) + end_path

        '''Return an array of dicts, containing the data and pagination.'''
        data = [dict(data=arr)]
        data.append(dict(paging=dict(next=next_page_path,
                                     previous=prev_page_path)))
        return data
