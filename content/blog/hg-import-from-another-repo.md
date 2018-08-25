---
title: Importing one Mercurial repository into another
date: 2015-11-04
tags: mercurial
---

In the
[ion trap group](http://phys.au.dk/forskning/forskningsomraader/amo/the-ion-trap-group/),
we usually use [Mercurial][] for version controlling software we write
for experimental control, data analysis, and so on. This post outlines
how to import the full history of one repository into another. This
can be useful for cases where it makes sense to move a sub-project
directly into its parent, for example.

[Mercurial]: https://www.mercurial-scm.org/

## Convert the soon-to-be child repository

With the Mercurial `convert` extension, you can rename branches, move,
and filter files. As an example, say we have a repo with only the
`default` branch which is to be imported into a super-repository.

For starters, we will want all our files in the child repo to be in a
subdirectory of the parent repo and not include the child's
`.hgignore`. To do this, create a file `filemap.txt` with the
following contents:

```
rename . child
exclude .hgignore
```

The first line will move all files in the repo's top level into a
directory named `child`.

Next, optionally create a `branchmap.txt` file for renaming the
`default` branch to something else:

```
default child-repo
```

Now convert:

```
hg convert --filemap branchmap.txt --branchmap branchmap.txt child/ converted/
```

## Pull in the converted repository

From the parent repo:

```
hg pull -f ../converted
```

Ensure the child commits are in the draft phase with:

```
hg phase -f --draft -r <first>:<last>
```

## Rebase as appropriate

```
hg rebase -s <child rev> -d <parent rev>
```

To keep the child's changed branch name, use the `--keepbranches`
option.

## References

* https://mercurial.selenic.com/wiki/ConvertExtension
* https://mercurial.selenic.com/wiki/Phases
* https://mercurial.selenic.com/wiki/RebaseExtension
* https://stackoverflow.com/questions/3214717/how-can-i-import-a-mercurial-repo-including-history-into-another-mercurial-rep
* https://stackoverflow.com/questions/3338672/mercurial-convert-clones-to-branches
