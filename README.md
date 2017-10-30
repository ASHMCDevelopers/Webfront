# ASHMC Webfront

## What is this?

This is the ASHMC official webfront, and it is in continuous development.

The ASHMC webfront allows registered students to vote, learn about events, get updates from
the ASHMC council, and know who the council actually is.

## How do I contribute?

Fork! Develop feature branches based on the `develop` branch; pull requests for
`master` will be closed without review unless they are hotfixes.

Our lead(s) use a workflow that's pretty close to nvie's `git-flow` - with a
little jiggering to fit it into a more active development cycle and GitHub.

1. fork off ASHMCDeveloper/Webfront (hereafter, `canon`)
1. Make a feature branch off of `develop`.
2. code code code.
3. periodically `pull canon` to keep up to date with `canon` and rebase your features on top of `develop`.
4. commit! push to your fork (usually `origin`) - there's no reason to merge into your local develop branch.
5. submit a pull request, destination `canon develop`.
6. profit!

For example:
```
git pull canon
git flow feature start my-sweet-feature
// code code code
// pull
// code code code
// I think i'm done coding!
git commit -am "done!"
git flow feature publish
// on github, make pull request into canon/develop
// code as necessary in response to reviews.
// when the feature is accepted, you can delete your local and origin feature branches.
git branch -D feature/my-sweet-feature
git push origin --delete feature/my-sweet-feature
// or not, as you choose.
```

Managers have a slightly different life than regular contributers, but we won't
go into that until the next section.

If you're not into coding (or Python, or Django), 1. what's wrong with you,
and 2. no worries! If you're a student, you can submit bugs, enhancements or
questions. One of the devs will get back to you ASAP.

## What if I'm a moderator?

The moderator's non-development duties look like this (a slightly modified form of git-flow):

* Look through pull requests. If there's a hotfix, it gets priority. Hotfixes skip the standard
'live in develop for a while' lifecycle of a branch, because they are urgent things that need to be
in production immediately (as opposed to later in the day, or maybe tomorrow).

    Hotfix branches are created by managers and pushed to canon so that others can pull-request into them.
    When a hotfix branch is complete, a manager will merge it into `master` and `develop`, then
    push both of those to `canon` so that the changes will head downstream.

    ```
    git pull canon
    git checkout master
    git checkout -b hotfix/{$identifier}
    git push -u canon hotfix/{$identifier}
    // ...
    // After devs have solved the issue:
    git pull canon
    git checkout master
    git merge --no-ff hotfix/{$identifier}
    git tag -a {$tag}
    // if there's no release branch:
    git checkout develop
    // if there's a release branch:
    git checkout release/{$release}
    git merge --no-ff hotfix/{$identifier}
    ```

    Pull requests for `develop` work similarly, except you don't merge the result into `master`.
    * release branches will be named like `release/`.
    * feature branches will be named like `feature/`.

    Feature branches are merged into develop just like hotfixes are into `master`.

    Feature pull requests are the simplest (and, hopefully, the most common): they're just
    regular pull requests. Code review, and when the feature looks good, accept the pull into
    `develop` (and _only_ `develop`).

    Release branches are created by managers, and pushed to `canon`, so that devs can work on them
    and submit pull requests against them. When the release is satisfactory, merge into both `master` and
    `develop`, then push those to `canon`. The release branch should then be deleted.

    ```
    git pull canon
    git checkout develop
    git checkout -b release/{$identifier}
    git push -u canon release/{$identifier}
    // ...
    // ...
    // After devs have fixed all the bugs:
    git pull canon
    git checkout master
    git merge --no-ff release/{$identifier}
    git tag -a ${tag}
    git checkout develop
    git merge --no-ff release/{$identifier}
    git push canon
    ```

* Look through issues, assign to developers/ask for more info/etc.
* Repeat.
