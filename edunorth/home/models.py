# from django.db import models

# class SearchHistory(models.Model):
#     prompt = models.CharField(max_length=255)  # The search query entered by the user
#     created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of search

#     def __str__(self):
#         return self.prompt

# class VideoResult(models.Model):
#     search_history = models.ForeignKey(SearchHistory, on_delete=models.CASCADE, related_name="videos")
#     title = models.CharField(max_length=255)  # Video title
#     link = models.URLField()  # Video URL

#     def __str__(self):
#         return self.title
from django.db import models
from django.contrib.auth.models import User

class UserSearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ✅ Link search to user
    prompt = models.TextField()  # ✅ Store search query
    created_at = models.DateTimeField(auto_now_add=True) # ✅ Timestamp

    def __str__(self):
        return f"{self.user.username} - {self.prompt} ({self.created_at})"

class Subtopic(models.Model):
    search = models.ForeignKey(UserSearchHistory, on_delete=models.CASCADE, related_name="subtopics")  # ✅ Link to search history
    name = models.CharField(max_length=255)  # ✅ Subtopic name

    def __str__(self):
        return self.name

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('youtube', 'YouTube Video'),
        ('blog', 'Blog Article'),
    ]

    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, related_name="resources")  # ✅ Link to a subtopic
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)  # ✅ Type: YouTube or Blog
    title = models.CharField(max_length=255)  # ✅ Title of resource
    url = models.URLField()  # ✅ URL of resource

    def __str__(self):
        return f"{self.resource_type}: {self.title} (Subtopic: {self.subtopic.name})"
from django.db import models
from django.contrib.auth.models import User

class UserSearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ✅ Link search to user
    prompt = models.TextField()  # ✅ Store search query
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ Timestamp

    def __str__(self):
        return f"{self.user.username} - {self.prompt} ({self.created_at})"

class Subtopic(models.Model):
    search = models.ForeignKey(UserSearchHistory, on_delete=models.CASCADE, related_name="subtopics")  # ✅ Link to search history
    name = models.CharField(max_length=255)  # ✅ Subtopic name
    quiz_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('youtube', 'YouTube Video'),
        ('blog', 'Blog Article'),
    ]

    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, related_name="resources")  # ✅ Link to a subtopic
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)  # ✅ Type: YouTube or Blog
    title = models.CharField(max_length=255)  # ✅ Title of resource
    url = models.URLField()  # ✅ URL of resource

    def __str__(self):
        return f"{self.resource_type}: {self.title} (Subtopic: {self.subtopic.name})"
    
    
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # ✅ Links profile to user
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.URLField()
    college = models.CharField(max_length=255)
    grad_year = models.IntegerField(blank=True, null=True)
    skills = models.TextField(help_text="Enter skills separated by commas")  # ✅ Stores skills as text
    experience = models.TextField(blank=True, null=True)  # ✅ Experience is optional
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ Stores profile creation date

    def __str__(self):
        return self.name

