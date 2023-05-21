from django import forms
from .models import Bot, Table, Phrase, BlockedUsers


class BotForm(forms.ModelForm):
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
                  'excluded_words_table'
                ]
        widgets = {
            'keywords_table': forms.Select(attrs={'class': "form-select"}), 
            'excluded_words_table': forms.Select(attrs={'class': "form-select"}),
        }


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
