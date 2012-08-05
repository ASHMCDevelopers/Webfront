from django import forms


class CandidateChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.cast())


class BallotForm(forms.Form):

    def __init__(self, ballot=None, *args, **kwargs):
        prefix = kwargs.pop('prefix', ballot.id)
        super(BallotForm, self).__init__(*args, prefix=prefix, **kwargs)
        self.ballot = ballot
        choices = ballot.candidate_set.all()

        self.fields['choice'] = CandidateChoiceField(
            widget=forms.RadioSelect,
            empty_label=None if not ballot.can_abstain else "I'm abstaining",
            queryset=choices,
            required=(not ballot.can_write_in),
        )

        if ballot.can_write_in:
            self.fields['write_in_value'] = forms.CharField(
                max_length=50,
                required=False,
                widget=forms.TextInput(
                    attrs={
                        'placeholder': "or, write in here.",
                        'class': 'write_in',
                    })
            )

    def clean(self):
        cleaned_data = super(BallotForm, self).clean()

        write_in = cleaned_data.get('write_in_value', None)
        choice = cleaned_data.get('choice', None)

        # A none choice would have been caught unless there's a write-in field

        if choice is None and not write_in:
            if not self.ballot.can_abstain:
                raise forms.ValidationError(
                    "Must either select a candidate or write one in."
                )

        if choice is not None and write_in:
            raise forms.ValidationError(
                "Can't choose a candidate and write one in for the same ballot."
            )

        return cleaned_data

BallotFormSet = forms.formsets.formset_factory(BallotForm, extra=0)
