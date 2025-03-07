from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from .models import UserSearchHistory, Subtopic, Resource
# from .AIMOD import get_subtopics, get_top_youtube_video, get_blog_link
from .AIMOD import get_ai_response
from .models import StudentProfile
from .tester import get_quiz, create_google_form
# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,'home.html')

def loginUser(request):
    
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        print(username,password)
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login( request, user)
            return render(request,'home.html')
        else:
            return render(request,"updateProfile.html")

  
    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return render(request,'login.html')

def about(request):
    return render(request,'about.html')

def profile(request):
    user_profile = StudentProfile.objects.filter(user=request.user).first()
    return render(request, "profile.html", {"user_profile": user_profile})


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Validate passwords match
        if password1 != password2:
            return render(request, "register.html", {"error": "Passwords do not match!"})

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists!"})

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email is already registered!"})
        
        # Create user and hash password
        user = User.objects.create(username=username, email=email, password=make_password(password1))
        StudentProfile.objects.create(user=user, name=username)
        login(request, user)  # Auto-login after registration
        return render(request,'updateProfile.html')  # Redirect to home page

    return render(request, "register.html")

def personalised(request):
    return render(request, "hometest.html")

def joblisting(request):
    return render(request, "joblisting.html")


# def search(request):
#     if request.method == "POST":
#         query = request.POST.get("query")
#         if query:
#             # Create a new search entry or get existing one
#             search_entry, created = SearchHistory.objects.get_or_create(prompt=query)

#             # Fetch related video results
#             videos = list(search_entry.videos.values("title", "link"))  # Use related_name "videos"

#             return JsonResponse({"videos": videos})

#     # Render template with all past search history
#     return render(request, "search.html", {"history": SearchHistory.objects.all()})


# def search(request):
#     videos = []  # Default empty list for videos

#     if request.method == "POST":
#         query = request.POST.get("query")
#         if query:
#             # Create or fetch the search entry
#             search_entry, created = SearchHistory.objects.get_or_create(prompt=query)

#             # Fetch related videos
#             videos = search_entry.videos.all()

#     # Render the template with history and video results
#     return render(request, "search.html", {"history": SearchHistory.objects.all(), "videos": videos})

  # ✅ Import AI functions


# # def process_prompt(request):
#     ai_response = None

#     if request.method == "POST":
#         prompt = request.POST.get("prompt")

#         if prompt:
#             # ✅ Get subtopics from AI
#             subtopics_dict = get_subtopics(prompt)

#             # ✅ Store in database
#             search_entry = UserSearchHistory.objects.create(user=request.user, prompt=prompt)

#             for subtopic in subtopics_dict["subtopics"]:
#                 subtopic_entry = Subtopic.objects.create(search=search_entry, name=subtopic)

#                 # ✅ Get YouTube video & blog for this subtopic
#                 video_info = get_top_youtube_video(subtopic, subtopics_dict["topic"])
#                 blog_info = get_blog_link(subtopic, subtopics_dict["topic"])

#                 if video_info:
#                     Resource.objects.create(
#                         subtopic=subtopic_entry, 
#                         resource_type="youtube",
#                         title=video_info["title"],
#                         url=video_info["url"]
#                     )

#                 if blog_info:
#                     Resource.objects.create(
#                         subtopic=subtopic_entry, 
#                         resource_type="blog",
#                         title=blog_info["title"],
#                         url=blog_info["url"]
#                     )

#     return render(request, "search_test.html", {"ai_response": ai_response})

def history_display(request):
    ai_response = None

    # ✅ Always fetch last 7 searches of the logged-in user
    history = UserSearchHistory.objects.filter(user=request.user).order_by("-created_at")[:20]  

    if request.method == "POST":
        prompt = request.POST.get("search")

        if prompt:
            print(f"\n🔹 User Searched for: {prompt}")

            # ✅ Store in database
            search_entry = UserSearchHistory.objects.create(user=request.user, prompt=prompt)

            # ✅ Refresh history after new search
            history = UserSearchHistory.objects.filter(user=request.user).order_by("-created_at")[:20]  

    return render(request, "hometest.html", {"ai_response": ai_response, "history": history})  # ✅ Always pass history



def search(request):
    if request.method=="POST":
        print(1)
    ai_response = None

    if request.method == "POST":
        prompt = request.POST.get("search")

        if prompt:
            print(f"\n🔹 User Searched for: {prompt}")
            # ✅ Get AI-generated response
            ai_response = get_ai_response(prompt)
            

            # ✅ Store in database
            search_entry = UserSearchHistory.objects.create(user=request.user, prompt=prompt)

            for subtopic_name, subtopic_data in ai_response["subtopics"].items():
                subtopic_entry = Subtopic.objects.create(search=search_entry, name=subtopic_name)
                
                # ✅ Store YouTube video
                if subtopic_data["video"]:
                    Resource.objects.create(
                        subtopic=subtopic_entry, 
                        resource_type="youtube",
                        title=subtopic_data["video"]["title"],
                        url=subtopic_data["video"]["url"]
                    )
                    print(f"🎥 YouTube Video: {subtopic_data['video']['title']} - {subtopic_data['video']['url']}")

                # ✅ Store Blo
                if subtopic_data["blog"]:
                    Resource.objects.create(
                        subtopic=subtopic_entry, 
                        resource_type="blog",
                        title=subtopic_data["blog"]["title"],
                        url=subtopic_data["blog"]["url"]
                    )
                    print("\n🔹 AI Response Sent to Template:", ai_response)
            
    history = UserSearchHistory.objects.filter(user=request.user).order_by("-created_at")[:20]

    return render(request, "hometest.html", {"ai_response": ai_response, "history": history})

def update_profile(request):
    if request.method == "POST":
        name = request.POST.get("name")
        linkedin = request.POST.get("linkedin")
        college = request.POST.get("college")
        age = request.POST.get("age")
        skills = request.POST.get("skills")
        experience = request.POST.get("experience")
        location = request.POST.get("location")

        # ✅ Create or Update Student Profile (without profile image)
        profile, created = StudentProfile.objects.get_or_create(user=request.user)
        profile.name = name
        profile.linkedin = linkedin
        profile.college = college
        profile.grad_year = age
        profile.skills = skills
        profile.experience = experience
        profile.location = location
        profile.save()

        return render(request, "profile.html")  # ✅ Redirect to profile page after saving

    return render(request, "updateProfile.html")

# def get_quiz_view(request):
#     if request.method == "POST":
#         subtopic_name = request.POST.get("subtopic")  # ✅ Get subtopic name from button click
#         if subtopic_name:
#             quiz_data = get_quiz(subtopic_name)  # ✅ Generate quiz
#             if quiz_data["questions"]:  
#                 quiz_url = create_google_form(subtopic_name, quiz_data)  # ✅ Create Google Form quiz

#                 # ✅ Store the quiz URL in the database
#                 subtopic, created = Subtopic.objects.get_or_create(name=subtopic_name)
#                 subtopic.quiz_url = quiz_url
#                 subtopic.save()

#                 return redirect("search")  # ✅ Redirect back to search results page

#     return redirect("search")
# def get_quiz_view(request):
#     if request.method == "POST":
#         subtopic_name = request.POST.get("subtopic")  # ✅ Get subtopic name from button click
#         if subtopic_name:
#             quiz_data = get_quiz(subtopic_name)  # ✅ Generate quiz
#             if quiz_data["questions"]:  
#                 quiz_url = create_google_form(subtopic_name, quiz_data)  # ✅ Create Google Form quiz

#                 # ✅ Update quiz URL in the database
#                 Subtopic.objects.filter(name=subtopic_name).update(quiz_url=quiz_url)

#                 # ✅ Fetch the latest search results (including updated quiz links)
#                 search_results = UserSearchHistory.objects.filter(user=request.user).order_by('-created_at')[:7]

#                 return render(request, "hometest.html", {"search_results": search_results, "quiz_url": quiz_url, "subtopic_name": subtopic_name})

#     return redirect("search")

# def get_quiz_view(request):
#     if request.method == "POST":
#         subtopic_name = request.POST.get("subtopic")  # ✅ Get subtopic name from button click
#         if subtopic_name:
#             quiz_data = get_quiz(subtopic_name)  # ✅ Generate quiz
#             if quiz_data["questions"]:  
#                 quiz_url = create_google_form(subtopic_name, quiz_data)  # ✅ Generate Google Form quiz

#                 # ✅ Store the quiz URL in the database
#                 Subtopic.objects.filter(name=subtopic_name).update(quiz_url=quiz_url)

#                 return JsonResponse({"quiz_url": quiz_url})  # ✅ Return JSON response

#     return JsonResponse({"error": "Quiz could not be generated"}, status=400)


def get_quiz_view(request):
    if request.method == "POST":
        subtopic_name = request.POST.get("subtopic")
        print(f"📌 Debug: Received subtopic -> {subtopic_name}")

        if subtopic_name:
            try:
                quiz_data = get_quiz(subtopic_name)  # ✅ Generate quiz
                print(f"📌 Debug: API Response -> {quiz_data}")

                if quiz_data["questions"]:  
                    quiz_url = create_google_form(subtopic_name, quiz_data)  # ✅ Generate Google Form quiz
                    print(f"📌 Debug: Generated Quiz URL -> {quiz_url}")

                    # ✅ Store in database
                    Subtopic.objects.filter(name=subtopic_name).update(quiz_url=quiz_url)

                    return JsonResponse({"quiz_url": quiz_url})

            except Exception as e:
                print(f"❌ Error in get_quiz: {e}")
                return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Quiz could not be generated"}, status=400)

def ai_ml_page(request):
    return render(request, "ai_ml.html")

def finance_page(request):
    return render(request, "finance.html")

def cybersecurity_page(request):
    return render(request, "cybersecurity.html")

def web_dev_page(request):
    return render(request, "web_dev.html")

def blockchain_page(request):
    return render(request, "blockchain.html")

def data_science_page(request):
    return render(request, "data_science.html")




