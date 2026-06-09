from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from .models import User, HealthRecord
from .forms import UserRegistrationForm
from django.views import View
import requests
from django.conf import settings

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):

        if not request.session.get('user_id'):
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

class LoginView(View):

    template_name = 'users/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(
                email_address=email,
                password=password
            )

            request.session['user_id'] = user.id
            request.session['user_name'] = user.full_name

            return redirect('dashboard')

        except User.DoesNotExist:
            return render(
                request,
                self.template_name,
                {
                    'error': 'Invalid Email or Password'
                }
            )
class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


class HealthPredictionView(View):
    template_name = 'users/prediction.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        glucose = request.POST.get('glucose')
        haemoglobin = request.POST.get('haemoglobin')
        cholesterol = request.POST.get('cholesterol')

        prompt = f"""You are a medical risk prediction assistant.
Based on the following patient data, classify the risk level:
Glucose: {glucose}
Haemoglobin: {haemoglobin}
Cholesterol: {cholesterol}

Rules:
- If glucose > 160 or cholesterol > 240 → High Risk
- If glucose between 120–160 → Moderate Risk
- Otherwise → Low Risk

Return output strictly in this format:
Risk Level: <Low/Moderate/High>
Remarks: <one sentence explanation>"""

        prediction_text = self._fetch_api_prediction(prompt, glucose, cholesterol)

        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                HealthRecord.objects.create(
                    user=user,
                    glucose=glucose,
                    haemoglobin=haemoglobin,
                    cholesterol=cholesterol,
                    remarks=prediction_text
                )
            except User.DoesNotExist:
                pass

        return render(
            request,
            self.template_name,
            {'prediction': prediction_text}
        )

    def _fetch_api_prediction(self, prompt, glucose, cholesterol):
        """Helper method to handle the API request and parsing."""
        api_url = "https://api-inference.huggingface.co/models/google/flan-t5-base"
        headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}

        try:
            response = requests.post(
                api_url,
                headers=headers,
                json={"inputs": prompt, "options": {"wait_for_model": True}},
                timeout=15
            )

            if response.status_code != 200:
                return self.get_local_fallback(glucose, cholesterol)

            result = response.json()

            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "").strip()

            return f"Unexpected API structural response: {result}"

        except requests.exceptions.RequestException:
            return self.get_local_fallback(glucose, cholesterol)

    def get_local_fallback(self, glucose, cholesterol):
        """Helper engine to compute rules locally if Hugging Face fails."""
        try:
            g = float(glucose)
            c = float(cholesterol)
            if g > 160 or c > 240:
                return "Risk Level: High\nRemarks: Elevated indicators meet high risk parameters. (Local Engine Fallback)"
            elif 120 <= g <= 160:
                return "Risk Level: Moderate\nRemarks: Borderline glycemic metrics noted. (Local Engine Fallback)"
            else:
                return "Risk Level: Low\nRemarks: Indicators appear within expected reference ranges. (Local Engine Fallback)"
        except (ValueError, TypeError):
            return "Risk Level: High\nRemarks: Critical health indicators could not be verified due to data processing anomalies."
class DashboardView(View):
    template_name = 'users/dashboard.html'

    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        user = get_object_or_404(User, id=user_id)
        records = HealthRecord.objects.filter(user=user).order_by('id')  # Newest first

        return render(request, self.template_name, {
            'user': user,
            'records': records
        })

class EditRecordView(View):
    template_name = 'users/edit_record.html'

    def get(self, request, record_id):
        if not request.session.get('user_id'):
            return redirect('login')

        record = get_object_or_404(HealthRecord, id=record_id, user_id=request.session['user_id'])
        return render(request, self.template_name, {'record': record})

    def post(self, request, record_id):
        record = get_object_or_404(HealthRecord, id=record_id, user_id=request.session['user_id'])

        glucose = request.POST.get('glucose')
        haemoglobin = request.POST.get('haemoglobin')
        cholesterol = request.POST.get('cholesterol')

        try:
            g = float(glucose)
            c = float(cholesterol)
            if g > 160 or c > 240:
                prediction_text = "Risk Level: High\nRemarks: Elevated indicators meet high risk parameters."
            elif 120 <= g <= 160:
                prediction_text = "Risk Level: Moderate\nRemarks: Borderline glycemic metrics noted."
            else:
                prediction_text = "Risk Level: Low\nRemarks: Indicators appear within expected reference ranges."
        except (ValueError, TypeError):
            prediction_text = "Risk Level: Unknown\nRemarks: Calculation failed due to invalid data format."

        record.glucose = glucose
        record.haemoglobin = haemoglobin
        record.cholesterol = cholesterol
        record.remarks = prediction_text
        record.save()

        return redirect('dashboard')


class DeleteRecordView(View):
    template_name = 'users/delete_confirmation.html'

    def get(self, request, record_id):
        if not request.session.get('user_id'):
            return redirect('login')

        record = get_object_or_404(HealthRecord, id=record_id, user_id=request.session['user_id'])

        return render(request, self.template_name, {'record': record})

    def post(self, request, record_id):
        if not request.session.get('user_id'):
            return redirect('login')

        record = get_object_or_404(HealthRecord, id=record_id, user_id=request.session['user_id'])
        record.delete()
        return redirect('dashboard')

class LogoutView(View):
    def get(self, request):
        # Completely clears out the session data and deletes the session cookie
        request.session.flush()
        return render(request, 'users/logout.html')