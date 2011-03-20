/*
---

name: Growler

description: a simple, event-based, Growl-style notification system for mooTools

authors: Stephane P. Pericat (@sppericat)

license: MIT-style license.

requires: [Core]

provides : Growler

...
*/

var Growler = {
	author: "Stephane P. Pericat",
	license: "MIT",
	version: '0.3'
}

/* 
 * Growler.Classic uses a png/gif file as background image, thus making size + style quite static
 * Compatibility: IE 7 / 8, Safari 5, Firefox 3.*, Chrome 
 */

Growler.Classic = new Class({
	Implements: [Options, Events],
	options: {
		background: 'growl.png',
		width: 298,
		height: 73,
		timeOut: 2000
	},
	container: null,

	initialize: function(options) {
		if(options)
			this.setOptions(options);
			
		this.container = new Element('div', {
			styles: {
				width: this.options.width,
				position: 'fixed',
				top: 0,
				right: 0
			}
		});
		$(document.body).grab(this.container);
	},

	listen: function(el, evt, msg) {
		if($(el)) {
			$(el).addEvent(evt, function() {
				if(msg)
					this.notify(msg);
			}.bind(this));
		} else {
			throw 'invalid element id';
		}
	},
	
	notify: function(msg) {
		var growlWindow = new Element('div', {
			styles: {
				background: 'url('+this.options.background+')',
				position: 'relative',
				top: 10,
				right: 10,
				height: this.options.height - 20,
				width: this.options.width - 20,
				padding: '10px',
				marginBottom: '10px',
				color: '#fafafa',
				fontFamily: 'Helvetica, Arial, sans-serif',
				fontSize: '12px',
				opacity: 0
			}
		});
		growlWindow.set('text', msg);
		this.container.grab(growlWindow);
		growlWindow.morph({opacity: 1});
		(function() {
			growlWindow.morph({opacity: 0});
			(function() {
				growlWindow.dispose();
			}).delay(500);
		}).delay(this.options.timeOut);
	}
});

/* 
 * Growler.Modern is a fully customizable html5 / css3 implementation of Growl.
 * Compatibility: Safari 5, Firefox 3.*, Chrome 
 */

Growler.Modern = new Class({
	Implements: [Options, Events],
	options: {
		styles: {
			background: 'rgba(0, 0, 0, 0.7)',
			height: 73,
			width: 298,
			position: 'relative',
			top: 10,
			right: 10,
			borderRadius: '1em',
			MozBorderRadius: '1em',
			padding: '10px',
			marginBottom: '10px',
			color: '#fafafa',
			fontFamily: 'Helvetica, Arial, sans-serif',
			fontSize: '12px',
			opacity: 0,
			WebkitBoxShadow: '2px 2px 12px #777777',
			MozBoxShadow: '2px 2px 12px #777777' 
		},
		timeOut: 2000,
	},
	container: null,
	
	initialize: function(options) {
		if(options)
			this.setOptions(options);
			
		this.container = new Element('div', {
			styles: {
				width: this.options.width,
				position: 'fixed',
				top: 0,
				right: 0
			}
		});
		$(document.body).grab(this.container);
	},
	
	listen: function(el, evt, msg) {
		if($(el)) {
			$(el).addEvent(evt, function() {
				if(msg)
					this.notify(msg);
			}.bind(this));
		} else {
			throw 'invalid element id';
		}
	},
	
	notify: function(msg) {
		var growlWindow = new Element('div', {
			styles: this.options.styles
		});
		growlWindow.set('text', msg);
		this.container.grab(growlWindow);
		growlWindow.morph({opacity: 1});
		(function() {
			growlWindow.morph({opacity: 0});
			(function() {
				growlWindow.dispose();
			}).delay(500);
		}).delay(this.options.timeOut);
	}
});