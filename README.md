# CO2 PPM Badge

![latest](https://co2ppmbadge.piazza.energy/latest/ppm00.svg)
![1 year before](https://co2ppmbadge.piazza.energy/latest/ppm01.svg)
![10 years before](https://co2ppmbadge.piazza.energy/latest/ppm10.svg)

**CO2PPMBadge** is a simple app that reads CO2 PPM (Parts Per Million) information from available online APIs and generates badges and images that be embedded in websites to raise awareness of the climate change crisis we are all facing on this planet.

[![CircleCI](https://circleci.com/gh/piazza-energy/co2ppmbadge.svg?style=svg)](https://circleci.com/gh/piazza-energy/co2ppmbadge) [![Coverage Status](https://coveralls.io/repos/github/piazza-energy/co2ppmbadge/badge.svg?branch=develop)](https://coveralls.io/github/piazza-energy/co2ppmbadge?branch=develop)

# How to use

We want to provide a simple mean of communication that can be used on any website as a quick and identifiable tool that can be easily distributed across the internet.

**Please** visit the website https://co2ppmbadge.piazza.energy/

## Web Page

svg images for CO2 PPM, respectively latest, 1 year before, 10 years before

```html
<img src="https://co2ppmbadge.piazza.energy/latest/ppm00.svg">
<img src="https://co2ppmbadge.piazza.energy/latest/ppm01.svg">
<img src="https://co2ppmbadge.piazza.energy/latest/ppm10.svg">
```

## Javascript

json endpoint for CO2 PPM, respectively latest, 1 year before, 10 years before

```
https://co2ppmbadge.piazza.energy/latest/ppm00.json
https://co2ppmbadge.piazza.energy/latest/ppm01.json
https://co2ppmbadge.piazza.energy/latest/ppm10.json
```

## Markdown, e.g. Github

svg images for CO2 PPM embedded in Markdown, respectively latest, 1 year before, 10 years before

```markdown
![latest](https://co2ppmbadge.piazza.energy/latest/ppm00.svg)
![1 year before](https://co2ppmbadge.piazza.energy/latest/ppm01.svg)
![10 years before](https://co2ppmbadge.piazza.energy/latest/ppm10.svg)
```

# Further readings

have a look at the following:

- [development](./docs/dev.md)
- CO2 [reference](./docs/ref.md), documents and APIs
