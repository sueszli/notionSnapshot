# TODO

- [ ] add missing support for file attachments (also see: [supported blocks](supported%20blocks.md))

- [ ] refactor code (ie. put downloading / saving functionality into a separate module)
  - [ ] file_downloader.py
  - [ ] file_saver.py

- [ ] fix depsendencies / issue with poetry, put everything on pypi

- [ ] advertise on loconotion, reddit, hackernews (see: https://news.ycombinator.com/item?id=35316679)

---

if the project actually gets some traction, here are some ideas for the future:

- [ ] make it more accessible for people who don't code / don't have python (= most notion users) 
  - [ ] build simple gui with tkinter (see: https://github.com/stars/sueszli/lists/python-guis)
  - [ ] build executables for windows and osx

- [ ] make contributing easier
  - [ ] build CI/CD end-to-end tests for PRs

- [ ] improve performance
  - [ ] concurrently download assets using https://docs.aiohttp.org/en/stable/client_quickstart.html#streaming-response-content
