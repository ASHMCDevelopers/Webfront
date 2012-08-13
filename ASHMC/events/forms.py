from django import forms


class AttendanceForm(forms.Form):
    def __init__(self, event=None, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)

        self.event = event

        for number in range(1, event.guests_per_user + 1):
            name_field = forms.CharField(
                max_length=100,
                required=False,
                label="Guest's name",
                widget=forms.TextInput(
                    attrs={
                        'class': 'name_input',
                        'placeholder': "guest {}'s name".format(number),
                    },
                )
            )

            age_field = forms.IntegerField(
                min_value=10,
                error_messages={
                    'min_value': "You really shouldn't bring someone that young to a college event."
                },
                widget=forms.TextInput(
                    attrs={
                    'class': 'age_input',
                    'placeholder': "age".format(number),
                    },
                )
            )
            self.fields["name_{}".format(number)] = name_field
            self.fields["age_{}".format(number)] = age_field
