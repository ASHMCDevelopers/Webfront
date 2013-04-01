# ASHMC/vote - The Voting System

All description text is parsed with markdown.

## Measures

Measures can contain an arbitrary number of ballots.

### Measures can be scheduled.

A measure needn't be ready immediately; feel free to set its vote-start date
to any time you like. If all else fails, you can toggle its vote-ability
with the `is_open` flag.

### Measures require a description of some sort.

This is negotiable, but I think it's good policy to be able to motivate the
need for a measure.

### Measures can be restricted to certain dorms, certain classes, and can ban specific users.

But they don't have to. By default, all measures are open to the entire
student body - and closed to anyone who isn't _currently_ attending Mudd.

### Measures will automatically close the midnight after they reach whatever quorum is set for them.

This is a nice feature, I think - though chronically late voters may learn
new habits the hard way.

### You can rearrange the position of the ballots.
It's easy! You just type in some new numbers, and press 'save'.

### Votes can be anonymous by default

Or, not. Currently, there is no 'gradient' of anonymity; a vote in a ballot
is either tied to a user, or not at all tied to a user. This means that
anonymous ballots won't be able to generate as many stats as non-anonymous
ballots.

In a future release, there will be non-identifying metadata associated with
a vote, in addition to a user, so that anonymous votes can still be
demographically interesting.

## Ballots

### Four types of Ballot
There are four types of Ballot supported:

#### Popularity
Popularity votes are the most direct kind of vote: One User, one Vote, for one
Candidate.

The winner is the Candidate with the most Votes.

#### Yes/No
A special case of the Popularity type, the Yes-or-no ballot type removes the
description and automatically generates the yes/no choices for you.

This was designed to closely model the budget elections that ASHMC has to do
periodically; the candidates themselves don't require much description.

If you want to do a yes/no with descriptions of the impacts of yes vs no, then
use a regular popularity vote.

#### Select X
Unlike the Popularity type, Select X ballots allow a User to vote for multiple
candidates.

The Select X type allows you to specify a maxmimum number of choices each user
can make. Usually, you'll want this to be a smaller number than the number of
candidates on the ballot (otherwise, you could end up with an awkward election
that didn't narrow anybody out).

The winner is the Candidate with the most Votes.

#### Preference
A Preference Ballot has users rank the candidates from best (1) to worst (# of
candidates). The appropriate worst number is automatically created by the system.

The winner is the candidate with the lowest total.

##### Instant-runoff voting
Preference ballots can, optionally, be declared as IRV ballots. This means that
they will perform automatic runoff elections until one candidate has a majority
of the votes.

For more details about the process, hit up the
[IRV Wikipedia page](http://en.wikipedia.org/wiki/Instant-runoff_voting).

### Support for Write-ins
If the ballot is flagged as "can write-in", Users will be presented with a
text-box that they are free to use to write in the name of a new candidate.

Their write-in candidate will be treated as a real candidate in all ways -
except that the new name won't appear on the ballot along with the 'legit'
Candidates.

Any Users who write in the same name will have their votes attributed to the
same candidate.

### Support for abstaining

Just flag the ballot as 'can abstain', and Users will be given that option.

### Any (non-zero) number of Candidates
A Ballot can have an arbitrary number of Candidates. You can even mix
PersonCandidates and raw candidates, if you really want to.

## Candidates
Candidates are either raw Candidates or PersonCandidates, tied to User(s).

Candidates do not have to provide descriptions. If they don't, the system will
note on the ballot that 'no information was provided' for that candidate (except
in yes/no ballots).

# Management Commands

The voting system supports sending reminder emails:

```bash
python manage.py send_reminder_emails
```

You may optionally give it a list of Measure ID's, which will restrict who gets
emails and about what:

```bash
python manage.py send_reminder_emails 25 18 32 104
```

If you use the `--dry-run` flag, no emails will be sent. This allows you to
double check the intended recipients beforehand, if you like.
