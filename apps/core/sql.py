from typing import List, Dict, Any
from dataclasses import dataclass

from django.db import connection


@dataclass
class Query:
    text: str = ''

    def execute(self, params: List[Any]) -> List[Dict]:
        with connection.cursor() as cursor:
            cursor.execute(self.text, params)

            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
