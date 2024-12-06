# `nexio`

**Usage**:

```console
$ nexio [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `jobs`
* `todoist`

## `nexio jobs`

**Usage**:

```console
$ nexio jobs [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `close-jobs`
* `pull-jobs`

### `nexio jobs close-jobs`

**Usage**:

```console
$ nexio jobs close-jobs [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `nexio jobs pull-jobs`

**Usage**:

```console
$ nexio jobs pull-jobs [OPTIONS]
```

**Options**:

* `--store [no_store|csv|postgres]`: [default: no_store]
* `--output TEXT`
* `--help`: Show this message and exit.

## `nexio todoist`

**Usage**:

```console
$ nexio todoist [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get-projects`
* `get-tasks`

### `nexio todoist get-projects`

**Usage**:

```console
$ nexio todoist get-projects [OPTIONS]
```

**Options**:

* `--store [no_store|csv|postgres]`: [default: no_store]
* `--help`: Show this message and exit.

### `nexio todoist get-tasks`

**Usage**:

```console
$ nexio todoist get-tasks [OPTIONS]
```

**Options**:

* `--project-ids TEXT`
* `--store [no_store|csv|postgres]`: [default: no_store]
* `--output TEXT`
* `--help`: Show this message and exit.
