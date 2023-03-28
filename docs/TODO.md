# TODO

- [ ] add missing support for important blocks (see: [supported blocks](supported%20blocks.md))
  - [ ] file attachments (pdf)
  - [ ] table view (glitches horizontally, doesn't link to subpages correctly) 

<br>

- [ ] majorly refactor code (put trivial parts without a state into modules)
  - [ ] make a dedicated module for just downloading files, saving assets, etc.

<br>

- [ ] make projects easily accessible and ready for use
  - [x] make a dedicated website for documentation (most notion users don't know what github is)
  - [ ] fix poetry (some dependencies are not installed correctly and need to be installed manually with pip)
  - [ ] push everything to pypi
  - [ ] build simple gui with tkinter (see: https://github.com/stars/sueszli/lists/python-guis)
  - [ ] provide executables for windows and mac on the website (most notion users don't have python installed)

<br>

- [ ] advertise everywhere
  - [ ] on loconotion issues page (only if we could resolve any of them)
  - [ ] on reddit
  - [ ] on hackernews (see this similar project: https://news.ycombinator.com/item?id=35316679)

<br>

- [ ] use to finish the uniCourseSummaries project (https://github.com/sueszli/uniCourseSummaries)

<br>

then wait 1 month to see if this project gained traction, any issues were reported, any pull requests were made, etc. to decide whether it is worth continuing to work on.

ideas for the future:
- [ ] automated CI/CD end-to-end tests for PRs
- [ ] concurrent downloading of assets (https://docs.aiohttp.org/en/stable/client_quickstart.html#streaming-response-content)
