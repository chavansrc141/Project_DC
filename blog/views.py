from django.shortcuts import get_object_or_404, render,get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
from .models import Post, Salary
# list of dictionaries 


def home(request):
	# context is the dictonary
	context = {	
		#Posts is the keys of the context 
		'posts': Post.objects.all()
	}
	return render(request, 'blog/home.html', context)

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username = self.kwargs.get('username'))
		return Post.objects.filter(author = user).order_by('-date_posted')

class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostSalaryView(LoginRequiredMixin, CreateView):
	model = Salary
	fields = ['name','designation','no_of_overtime','no_of_days','advances']

	def calculate_sal(self, form):
		if form.instance.designation=="Jr.Manager":
			sal_of_day=3000
	
		if form.instance.designation=="Manager":
			sal_of_day=5000
        
		if form.instance.designation=="Sr.Manager":
			sal_of_day=7000

		add = (sal_of_day*form.instance.no_of_days)+((sal_of_day/8)*form.instance.no_of_overtime)+1200-form.instance.advances
		return super().calculate_sal(form)

	def form_valid(self, form):
		form.instance.name = self.request.user
		return super().form_valid(form)

	
	

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post

	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


def about(request):
	return render(request, 'blog/about.html',{'title': 'About'})




