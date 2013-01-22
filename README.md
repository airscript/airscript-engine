# airscript-engine

Lightweight scripts in the cloud

### Warning: Proof of concept made in less than 12 hours! Not final form!

This is a Python app to be deployed on Heroku that will let you run Lua
scripts from Github that run as if they were on
[Webscript](http://webscript.io). This effectively gives you a free
version of Webscript.

The goal is to be fully compatible with Webscript, meaning you can
expect the [same environment as Webscript](https://www.webscript.io/documentation) and even use both Webscript
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

Example:

    /: https://gist.github.com/7c74508c98c245c94311
    
Be sure to commit your edits.

### Deploy to Heroku
From the project directory, run this helper script:

    $ ./deploy [name]

It will create a Heroku URL with your optional name as the subdomain. If
you used the example mount, you can now go to:

    http://[name].herokuapp.com/test?name=John 

### Add / Edit Your Scripts Live!
Just edit your scripts from Github or clone them locally to edit.
Pushing to Github will update the source used by the Airscript engine.

For now, read the [Webscript Documentation](https://www.webscript.io/documentation) for details on the Lua environment.

The only time you have to redeploy is if you update the engine code or
change your Mountfile.

## Webscript Parity Status
Here's what works now:

* Request/Response model
* json module
* base64 module

Those were just easy to implement from Python's standard library. More soon...

## More Context

Although the idea seems inspired by Webscript, Airscript is actually an attempt to bring back a 4 year old project called Scriptlets. Scriptlets was a free service that let you write code in the browser, hit a Save, and get a URL that would run that code. It supported PHP, Python, Ruby, and JavaScript. It was created specifically for writing webhook handlers. 

Perhaps ahead of its time, Scriptlets usage never grew enough for it to
fully develop. Eventually it went defunct. Some years later, Webscript comes out as a potential
savior. However, their "business model" holds their product back. 

Airscript is intentionally riding on their environment to bootstrap an open and free alternative that may someday fulfill the original dream of Scriptlets.

## Contribution

Would love to have collaborators join to help with big plans for this project. Check out Issues for ideas on how you can help.

## License

TBD, Copyright (c) 2013 Jeff Lindsay

