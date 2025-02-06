from django.shortcuts import render
from django.views import View



class StudentsDashboard(View):
    template_name = 'accounts/dashboards/student_dashboard.html'
    
    def get(self, request):
        return render(request, self.template_name)
