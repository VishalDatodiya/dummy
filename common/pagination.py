from rest_framework import pagination

from common import messages, constants

page_size = constants.PAGE_SIZE
MAX_PAGE_SIZE = constants.MAX_PAGE_SIZE
PAGE_QUERY_PARAM = constants.PAGE_QUERY_PARAM

class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return ({
            "message": messages.get_success_message(),
            "code": 200,
            "results": data,
          
            "pagination": {
                'next': self.get_next_page_number() if self.get_next_link() else None,
                'previous': self.get_previous_page_number() if self.get_previous_link() else None,
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "limit":page_size,
            }
        })
    def get_next_page_number(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_previous_page_number(self):
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()
