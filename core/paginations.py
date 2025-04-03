from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': (self.page.paginator.count // self.page.paginator.per_page) + (
                1 if self.page.paginator.count % self.page.paginator.per_page else 0
            ),
            'current_page': self.page.number,
            'page_size': self.page.paginator.per_page,  # The current limit set
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })