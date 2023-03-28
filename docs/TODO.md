# TODO

- [ ] add missing support for file attachments (also see: [supported blocks](supported%20blocks.md))

- [ ] refactor code (ie. put downloading / saving functionality into a separate module)

- [ ] make projects easily accessible and ready for use
  - [x] make a dedicated website for documentation (most notion users don't know what github is)
  - [ ] fix poetry (some dependencies are not installed correctly and need to be installed manually with pip)
  - [ ] push everything to pypi with poetry

- [ ] finish up uniCourseSummary project (see: https://github.com/sueszli/uniCourseSummaries)

---

<br>

then optionally:

- [ ] advertise for project, get some traction
  - [ ] on loconotion page (in issues section, only if we could successfully resolve any of them)
  - [ ] on reddit (see: https://www.reddit.com/r/Notion/)
  - [ ] on hackernews (see: https://news.ycombinator.com/item?id=35316679)

- [ ] make project more accessible for people who don't code (= most notion users) 
  - [ ] build simple gui with tkinter (see: https://github.com/stars/sueszli/lists/python-guis)
  - [ ] build executables for windows and mac (most notion users don't have python installed)

then wait 1 month to see if this project gained traction, any issues were reported, any pull requests were made, etc. to decide whether it is worth continuing to work on.

<br>

ideas for the future:
- [ ] make contributing easier
  - [ ] automated CI/CD end-to-end tests for PRs
- [ ] improve performance
  - [ ] concurrently download assets (https://docs.aiohttp.org/en/stable/client_quickstart.html#streaming-response-content)
