from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from apps.thoughts.models import Thought, Topic


class ThoughtView(View):

    def post(self):
        a = 1

    def get(self, request: HttpRequest, thought_id: int) -> HttpResponse:

        thought = Thought.by_id(thought_id)
        if not thought:
            return HttpResponse('Не найдено', status=404)

        context = {
            'name': thought.title,
            'status': 'Завершено' if thought.finished else 'Не завершено',
            'created': str(thought.created),
            'last_modified': str(thought.last_modified),
            'topics': [{'id': top.id, 'name': top.title} for top in thought.topics.all()],
            'text': thought.text,
        }

        return render(request, 'thought.html', context)


class ThoughtListView(View):

    def get(self, request: HttpRequest) -> HttpResponse:

        topics = Topic.objects.order_by('paragraph__title').all()

        topics_data: List[Dict] = []

        paragraphs_dict: Dict[str, List[Thought]] = {}

        for topic in topics:
            topic_data = {'name': topic.title, 'id': topic.id}

            paragraph_name = topic.paragraph.title
            topics_list = paragraphs_dict.get(paragraph_name)

            if topics_list is None:
                paragraphs_dict[paragraph_name] = [topic_data]
            else:
                topics_list.append(topic_data)

        paragraphs_data = [{'name': k, 'topics': v}
                           for k, v in paragraphs_dict.items()]

        context = {
            'paragraphs': paragraphs_data,
        }

        return render(request, 'index.html', context)
