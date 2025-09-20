from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "start_time", "end_time", "location", "image", "category"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-300"
            }),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "class": "w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-300"
            }),
            "start_time": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-300"
            }),
            "end_time": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-300"
            }),
            "location": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-300"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-300"
            }),
            "category": forms.Select(attrs={
                "class": "w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-300"
            }),
        }
