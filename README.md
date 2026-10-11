# note-cli

A tiny command-line tool that stores plain-text notes as content-addressed files.

## Requirements

- Python 3.10+
- No third-party dependencies

## Install

From this repository directory, make the script executable and put it on your `PATH`:

```sh
chmod +x note
mkdir -p ~/.local/bin
cp note ~/.local/bin/note
export PATH="$HOME/.local/bin:$PATH"
```

The default database is `.notes/db/` relative to the current working directory. To use a different database directory, set `NOTE_DB_DIR`.

## Usage

```sh
note add "Remember to call Sam"
note list
note delete <sha256-hash>
```

`add` prints the SHA-256 hash of the note. The note is stored as `.notes/db/<hash>` with no title or extension. The file contains the note text as provided (the CLI does not append a newline). Identical text produces the same hash and is stored only once.

`list` prints stored filenames (hashes), one per line, sorted alphabetically. If the database does not exist, it prints nothing.

`delete` removes the note matching the supplied 64-character lowercase SHA-256 hash. It prints an error and returns a non-zero status if the hash is invalid or the note does not exist.

## Examples

```sh
hash="$(note add "Buy oat milk")"
note list
note delete "$hash"
```

## Development

Run tests with:

```sh
python3 -m unittest discover -s tests -v
```

## Storage note

The default `.notes/` directory is intended for local data and is ignored by Git. Notes are plain text and are not encrypted.
