# TODO

priority highest to lowest

- ~~index.html in cloudfront distribution with list of published dates.~~ This should:
  - ~~update every day with a SNS publish / subscribe mechanism as described in [flow](./img/flow.png)~~
  - ~~have og tags for social media sharing~~
  - ~~potentially have a graph based on historical data~~
- ~~more and better looking image types~~
- implement cdn logging monitor, maybe with ELK
- implement a Twitter account with posts after each update
- implement a form of etag to get the latest update without waiting cache to expire
- publish content to a github page
