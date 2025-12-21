an alternative to the git cli

features
Tracks changes automatically but can be tagged
changes are delta based, tags are snapshot based
branches are constantly rebased
No such thing as untracked files. They are automatically add unless they are ignored 
Restore should delete "untracked" files
Auto detect moving files
? No remote repos only remote branches

an deltas and snapshots model

Tags are just named snapshots
Each branch has a series of snapshots and deltas in between them.
A repo has a series of branches
Remote branches can be added and shared across repos

auto rebase when changes are local, merge when external sources depend on them