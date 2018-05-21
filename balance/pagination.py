from rest_framework.response import Response
from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'total': self.page.paginator.count,
                'per_page': self.page.paginator.per_page,
                'current_page': self.page.number,
                'last_page': self.page.paginator.num_pages,
                'next_page_url': self.get_next_link(),
                'prev_page_url': self.get_previous_link()
            },
            'results': data
        })