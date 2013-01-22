# airscript-engine

Lightweight scripts in the cloud

### Warning: Proof of concept made in less than 12 hours!

This is an app to be deployed on Heroku that will let you run Lua
scripts from Github that run as if they were on
[Webscript](http://webscript.io). This effectively gives you a free
version of Webscript.

The goal is to be fully compatible with Webscript, meaning you can
expect the same environment as Webscript and even use both Webscript
maintained and 3rd party modules.

There are plans to go beyond current Webscript functionality.
Airscript will someday support different language runtimes. JavaScript
is first on the list.

## Requirements

First you need a Github account and a Heroku account. Both are free! [Sign up for Heroku.](https://api.heroku.com/signup) [Sign up for Github.](https://github.com/)

Software wise, you need Git and the [Heroku Toolbelt](https://toolbelt.heroku.com/).

## Getting Started

### Get the source
Clone this repo to your machine.

### Edit the Mountfile
Airscript pulls script sources from public Github repos or Gists. Edit
the Mountfile to point paths to any Gist or Github project URL. All
files in the repo or Gist will be available under the mounted path.

    <path>: <gist or repo url>

Be sure to commit your edits.

### Deploy to Heroku

## More Context

Although the idea seems inspired by Webscript, Airscript is actually an attempt to bring back a 4 year old project called Scriptlets. Scriptlets was a free service that let you write code in the browser, hit a Save, and get a URL that would run that code. It supported PHP, Python, Ruby, and JavaScript. It was created specifically for writing webhook handlers. 

Perhaps ahead of its time, Scriptlets usage never grew enough for it to
fully develop. Eventually it went defunct. Some years later, Webscript comes out as a potential
savior. However, their "business model" holds their product back. 

Airscript is intentionally riding on their environment to bootstrap an open and free alternative that may someday fulfill the original dream of Scriptlets.

## License

TBD, Copyright (c) 2013 Jeff Lindsay

