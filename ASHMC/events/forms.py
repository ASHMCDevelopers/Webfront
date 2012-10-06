from django import forms


class AttendanceForm(forms.Form):
    css_error_class = 'error_field'

    def __init__(self, event=None, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)

        self.event = event

        for number in range(1, self.event.guests_per_user + 1):
            name_field = forms.CharField(
                max_length=100,
                required=False,
                widget=forms.TextInput(
                    attrs={
                        'class': 'name_input',
                        'placeholder': "firstname lastname".format(number),
                    },
                )
            )

            age_field = forms.IntegerField(
                min_value=10,
                required=False,
                error_messages={
                    'min_value': "too young",
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

    def clean(self):
        cleaned_data = super(AttendanceForm, self).clean()
        #print "CLEAN ", cleaned_data
        for number in range(1, self.event.guests_per_user + 1):
            age = cleaned_data.get("age_{}".format(number), None)
            name = cleaned_data.get("name_{}".format(number), '')

            # If neither name nor age was specified, that's cool with us.
            if name == '' and age == None:
                continue

            if not all([name, age]):
                raise forms.ValidationError('Please give both name and age for all guests.')

            if len(name.split(' ')) < 2:
                self._errors['name_{}'.format(number)] = self.error_class(["Please give both first and last name."])

        return cleaned_data
