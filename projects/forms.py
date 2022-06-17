from django import forms
from projects.models import Project

project = Project.objects.all()
id_and_title = []
for p in project:
    id_and_title.append((p.id,p.title))

class ProjectForm(forms.Form):
    # project_id = forms.ChoiceField(required=True, label='Choose Project')
    # title = forms.ChoiceField(choices=id_and_title)
    select_project = forms.ModelChoiceField(
                        queryset=Project.objects.all(),
                        widget=forms.Select(attrs={
                                        "onChange": 'this.form.submit()'})
                    )
