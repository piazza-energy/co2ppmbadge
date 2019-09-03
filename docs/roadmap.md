---
layout: default
---

# Roadmap

[back to the index](./)

## upcoming versions

- implement a Twitter account with posts after each update
- implement cdn logging monitor, maybe with ELK
- make sam work so functions can be tested locally (other than unit tests)

## V1.0.0

released

- ~~index.html in cloudfront distribution with list of published dates.~~ This should:
  - ~~update every day with a SNS publish / subscribe mechanism as described in [flow](./img/flow.png)~~
  - ~~have og and twitter tags for social media sharing~~
  - ~~have a graph based on co2 ppm historical data~~
- ~~more and better looking image types other than just svg badges~~
- ~~publish content to a github page~~
- ~~continuous integration (circleci) and coverage (coveralls) report~~
