from django import forms
from .models import Bot, Table, Phrase, BlockedUsers


class BotForm(forms.ModelForm):

    # keywords_table = forms.ModelChoiceField(queryset=Table.objects.none(), widget=forms.Select(attrs={'class': 'form-select'}))
    # excluded_words_table = forms.ModelChoiceField(queryset=Table.objects.none(), widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Bot
        fields = [ 
                  'api_id', 
                  'api_hash', 
                  'session_name', 
                  'phone',  
                  'password', 
                  'recipient', 
                  'keywords_table', 
                  'excluded_words_table',
                  'owner'
                ]
        widgets = {
            'keywords_table': forms.Select(attrs={'class': "form-select"}), 
            'excluded_words_table': forms.Select(attrs={'class': "form-select"}),
        }
    
    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['keywords_table'].empty_label = 'Выберете таблицу'
        self.fields['keywords_table'].queryset = Table.objects.filter(owner=owner)
        
        self.fields['excluded_words_table'].empty_label = 'Выберете таблицу'
        self.fields['excluded_words_table'].queryset = Table.objects.filter(owner=owner)



class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': ''}),
            'description': forms.Textarea(attrs={'placeholder': '', 'style': 'height: 70px;'}),
        }


class PhraseForm(forms.ModelForm):
    class Meta:
        model = Phrase
        fields = ['phrase',]


class BlockedUsersForm(forms.ModelForm):
    class Meta:
        model = BlockedUsers
        fields = '__all__'
