# TODO

- [ ] add missing support for the 2 most important blocks (see: [supported blocks](supported%20blocks.md))
  - [ ] file attachments (pdf)
  - [ ] table view (glitches horizontally, doesn't link to subpages correctly) 

<br>

- [ ] majorly refactor code (put trivial, stateless parts without into their modules)
  - [ ] make a dedicated module just for downloading, just for writing into memory, etc.

<br>

- [ ] make projects easily accessible and ready for use
  - [x] make a dedicated website for documentation (most notion users don't know what github is)
  - [ ] fix poetry (some dependencies are not installed correctly and need to be installed manually with pip)
  - [ ] push everything to pypi with poetry
  - [ ] build simple gui with tkinter (see: https://github.com/stars/sueszli/lists/python-guis)
  - [ ] build executables for windows and mac (most notion users don't have python installed)

<br>

- [ ] advertise everywhere
  - [ ] on loconotion page (in issues section, only if we could successfully resolve any of them)
  - [ ] on reddit (see: https://www.reddit.com/r/Notion/)
  - [ ] on hackernews (see: https://news.ycombinator.com/item?id=35316679)

<br>

then wait 1 month to see if this project gained traction, any issues were reported, any pull requests were made, etc. to decide whether it is worth continuing to work on.

ideas for the future:
- [ ] automated CI/CD end-to-end tests for PRs
- [ ] concurrent downloading of assets (https://docs.aiohttp.org/en/stable/client_quickstart.html#streaming-response-content)
