# fixercise
A python package for pulling daily exchange rate data from the fixer.io API

## Install Instructions

You *should* be able to `pip install -e .` from the repo root, and that's it.

Some caveats to this:

- On setup it should write a relevant cron job to the installer's crontab, but this might fail for environmental reasons. I've tested it as working on Debian architecture linux.
- A pip install will install this python package to your current python environment, while the cron job will execute it against the user's default python environment. If these don't match, it will fail.
- If there is no relevant job in your crontab, add `0 9 * * * /env/where/it/is/installed fixercise` manually to your crontab.
- Executing cron jobs against arbitrary python envs is outside the scope of this exercise.

## Some Assumptions I Have Made
- A month is 31 days. The requirement for ensuring the last month's rates information is satisfied by checking the history on each run and getting data for all the missing dates, including the current date.
- If I'd had extra time I would have broken out all the config into a separate editable config subsystem. Config subsystems are a pain to test properly, and I didn't think you'd want me wasting my time on this.
- Storing as files to local disk is fine, and possibly even desirable. The files currently store (and logs currently log) to platform-specific app and log directories (On linux these are `~/.local/share/fixercise` and `~/.cache/fixercise/log` respectively. On a Mac you can find them at `~/Library/Application Support/fixercise`. Finding them on a Windows machine is your own adventure.)

## Bits I am particularly proud of
- Fire-and-forget. It's a one-liner to install and configure.
- It has logging out of the box
- The apparatus for getting and storing rates are independent of the retrieval procedure, so you could import them as modules in other scripts if you wanted
- It has a pretty comprehensive mock of the API, so expanding testing is very straightforward
- Data is doubly-idempotent. The app won't let you duplicate data, and neither will the way the file storage works
- Data is stored ordered both lexically and by time with the ISO date format, which makes it easy to pull it into some other application for analysis. An interesting side-effect of this is that it could be put into a date-keyed key-value store very easily.

## Bits I'm less proud of
- The config is horrible. There is a secret in the source code, and I am deeply, deeply unhappy about this horrid state of affairs.
- There is a weird bug with logging where it seems to clobber the entire log file with each run. This is almost certainly caused by a logger config problem but I don't have time to chase it down.
- I'm not entirely happy with the cron scheduling. It's fragile, platform-dependent, and cron is a fairly archaic way of doing things. I wasn't sure how else to do it given the time constraint, though.
- I enforce the "no-weekend" rule in the program logic. I did this because this makes it testable by unit tests, but you would probably want a different real-world solution.
- The use of appdirs to store the data and logs is kind of hacky. With the default config you have to go hunting for the data in your home directory. A fully-featured production-ready version of this would have configurable storage to different paths, including cloud storage.

## How I would deploy and monitor this in the wild
This is probably best deployed as an ephemeral containerised microservice, (i.e. Docker scheduled to run daily on some cloud compute platform). This would also get rid of the config problem as you could set secrets, etc. as environment variables in whatever platform builds your Docker images. In such an environment it would make more sense to write both the data and logs to a "serverless" purpose-built service (such as AWS S3 or DynamoDB). This would allow monitoring of the service outside of the lifetime of the container that runs it.
