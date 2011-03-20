#Growler

A simple, event-based, Growl-style notification system for mooTools.
Growler is compatible with MooTools Core 1.2.5 and 1.3 .

##License

The MIT-License

Copyright (c) 2010-2011 Stephane P. Pericat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

##How to Use

1: To instantiate the growler :

	window.addEvent('domready', function() {
		(!typeof(Browser.ie) == 'undefined') ? Growl = new Growler.Classic() : Growl = new Growler.Modern();
	});
	
2: To listen to an event:

	Growl.listen(window, 'domready', 'the DOM is ready!');
	
3: To simply throw a notification (for example during an ajax request) :

	new Request({
		url: 'some-file.php',
		onRequest: function() {
			Growl.notify('Request sent!');
		},
		onComplete: function(response) {
			Growl.notify(response);
		}
	}).send();
	
##TODO

- implement side visual