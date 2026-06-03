# Examples

Each block below is a ` ```gitsvg ` fence; the source is shown alongside the
rendered diagram. The op-stream syntax is gitsvg's — see the
[gitsvg](https://github.com/bertpl/gitsvg) project for the full reference.

## Linear history

```gitsvg
{"op": "branch", "name": "main", "label_side": "before"}
{"op": "commit", "branch": "main", "id": "c1", "msg": "initial commit", "hash": "auto"}
{"op": "commit", "branch": "main", "id": "c2", "msg": "add README", "hash": "auto"}
{"op": "commit", "branch": "main", "id": "c3", "msg": "add tests", "hash": "auto"}
```

## Branch and merge

```gitsvg
{"op": "branch", "name": "main", "label_side": "before"}
{"op": "commit", "branch": "main", "id": "c1", "msg": "initial commit", "hash": "auto"}
{"op": "branch", "name": "feature", "from_branch": "main"}
{"op": "commit", "branch": "feature", "id": "f1", "msg": "start feature", "hash": "auto"}
{"op": "commit", "branch": "feature", "id": "f2", "msg": "finish feature", "hash": "auto"}
{"op": "merge", "from": "feature", "into": "main", "as": "m1", "msg": "merge feature", "hash": "auto"}
{"op": "commit", "branch": "main", "id": "c2", "msg": "release prep", "hash": "auto"}
```

## Multiple diagrams on one page

Each diagram gets its own id namespace, so any number can coexist on a page:

```gitsvg
{"op": "branch", "name": "main", "label_side": "before"}
{"op": "commit", "branch": "main", "id": "c1", "msg": "init", "hash": "auto"}
{"op": "branch", "name": "topic", "from_branch": "main"}
{"op": "commit", "branch": "topic", "id": "t1", "msg": "topic work", "hash": "auto"}
```

## Themed (`gui`)

A `theme` op selects one of gitsvg's named themes (here `gui`):

```gitsvg
{"op": "theme", "name": "gui"}
{"op": "branch", "name": "main", "label_side": "before"}
{"op": "commit", "branch": "main", "id": "c0", "msg": "init platform", "hash": "auto"}
{"op": "branch", "name": "api", "from_branch": "main"}
{"op": "commit", "branch": "api", "id": "a1", "msg": "graphql schema", "hash": "auto"}
{"op": "branch", "name": "web", "from_branch": "main"}
{"op": "commit", "branch": "web", "id": "w1", "msg": "app shell", "hash": "auto"}
{"op": "commit", "branch": "api", "id": "a2", "msg": "resolvers", "hash": "auto"}
{"op": "branch", "name": "infra", "from_branch": "main"}
{"op": "commit", "branch": "infra", "id": "i1", "msg": "terraform base", "hash": "auto"}
{"op": "commit", "branch": "infra", "id": "i2", "msg": "ci pipeline", "hash": "auto"}
{"op": "commit", "branch": "web", "id": "w2", "msg": "client router", "hash": "auto"}
{"op": "merge", "from": "infra", "into": "main", "as": "mi", "msg": "merge infra", "hash": "auto"}
{"op": "commit", "branch": "main", "id": "c1", "msg": "platform baseline", "hash": "auto"}
{"op": "commit", "branch": "api", "id": "a3", "msg": "subscriptions", "hash": "auto"}
{"op": "merge", "from": "api", "into": "main", "as": "ma", "msg": "merge api", "hash": "auto"}
{"op": "commit", "branch": "main", "id": "c2", "msg": "v1.0 launch", "hash": "auto", "highlight": true}
```
