from django import forms
from .models import PatientRecord
from datetime import datetime, date


class PatientForm(forms.ModelForm):
    # Use a CharField for DOB to manually handle the dd/mm/yyyy and dd.mm.yyyy format
    date_of_birth = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy', 'class': 'form-control form-control-sm'}),
        help_text="Format: dd/mm/yyyy"
    )

    class Meta:
        model = PatientRecord
        fields = ['full_name', 'date_of_birth', 'email', 'glucose', 'haemoglobin', 'cholesterol']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
            'glucose': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.1'}),
            'haemoglobin': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.1'}),
            'cholesterol': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.1'}),
        }

    def clean_date_of_birth(self):
        dob_str = self.cleaned_data.get('date_of_birth')

        # Remove any accidental leading/trailing spaces
        dob_str = str(dob_str).strip()

        # The test data uses dots (28.01.1960) but requirement says slashes (dd/mm/yyyy).
        # We will try parsing both formats directly.
        parsed_date = None
        for fmt in ('%d/%m/%Y', '%d.%m.%Y'):
            try:
                parsed_date = datetime.strptime(dob_str, fmt).date()
                break  # If it parses successfully, stop looping
            except ValueError:
                continue  # If it fails, try the next format

        # If BOTH formats failed, raise the error
        if parsed_date is None:
            # Print to terminal so you can see exactly what failed!
            print(f"DEBUG: Failed to parse date string: '{dob_str}'")
            raise forms.ValidationError("Invalid date format or impossible date. Please use dd/mm/yyyy.")

        # Check for future dates
        if parsed_date > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future.")

        return parsed_date

    # Global validation to prevent exact duplicate records
    def clean(self):
        cleaned_data = super().clean()
        full_name = cleaned_data.get('full_name')
        date_of_birth = cleaned_data.get('date_of_birth')
        email = cleaned_data.get('email')

        if full_name and date_of_birth and email:
            # Check if a patient with the same name, dob, and email already exists
            existing = PatientRecord.objects.filter(
                full_name__iexact=full_name,
                date_of_birth=date_of_birth,
                email__iexact=email
            )

            # If we are editing an existing record, exclude the current record from the duplicate check
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise forms.ValidationError(
                    "A record with this exact Name, Date of Birth, and Email already exists. Duplicate entries are not allowed.")

        return cleaned_data