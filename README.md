# ASHMC Webfront

###### Better living without MuddSD

## What is this?

This is the ASHMC (currently) unofficial webfront, v1.x.

The ASHMC webfront allows registered students to vote, learn about events, get updates from
the ASHMC council, and know who the council actually is.

## How do I contribute?

Fork! Develop feature branches based on the `develop` branch; pull requests for
`master` will be closed without review unless they are hotfixes.

Our lead(s) use a workflow that's pretty close to nvie's `git-flow` - with a
little jiggering to fit it into a more active development cycle and GitHub.

1. fork off ASHMCDeveloper/Webfront (hereafter, the core)
1. Make a feature branch off of `develop`.
2. code code code.
3. periodically `pull canon` to keep up to date with the core - rebase on top of `develop`
   (or `release`, if you're working on a release branch).
4. commit! push to your fork - do *not* merge into your version of `develop`.
5. submit a pull request, destination `canon develop`.
6. profit!

Managers have a slightly different life than regular contributers, but we won't
go into that here.

If you're not into coding (or Python, or Django), 1. what's wrong with you,
and 2. no worries! If you're a student, you can submit bugs, enhancements or
questions. One of the devs will get back to you ASAP.

## What if I'm a moderator?

Well, first of all I weep for you.

The moderator's non-development duties look like this:

* Look through pull requests. If there's a hotfix, it gets priority. Hotfixes are
requests to be pulled into master, by definition. Otherwise, skip the next few steps.
    2. If the hotfix looks ready, great. accept the pull request. In your own repository,
`pull canon master`. Run tests to make sure it's actually a good release.
    2. If the tests don't pass, roll back the changes and push to canon (restoring
the old master). Yell at the pull-requester for sucking.
    2. If the tests *do* pass, celebrate! merge your `master` into `develop`, and `push canon`.
Nobody besides managers should be doing work on either `master` or `develop`, so this is safe
(they should be working in feature/hotfix/release branches).

    Pull requests for `develop` work similarly, except you don't merge the result into `master`.
    * release branches will be named like `release/`.
    * feature branches will be named like `feature/`.

    Feature branches are merged into develop just like hotfixes are into `master`.

    Release branches are created by managers, and pushed to `canon`, so that devs can work on them
    and submit pull requests against them.

* Look through issues, assign to developers/ask for more info/etc.
