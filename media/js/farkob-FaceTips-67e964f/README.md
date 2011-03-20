FaceTip
=======

FaceTip is a Mootools plugin that lets you have Facebook style tooltips.
[Demo](http://jsfiddle.net/farkob/zjvyM/)

![Screenshot](http://img213.imageshack.us/img213/6250/facetip.jpg)

How to Use
----------

With this, you add tips to all images with the 'tipped' class.

JS:

	new FaceTip($$('.tipped'));

HTML:

	<img src="http://site.com/somepic.png" tip="Some Pic" class="tipped"  />

Of course, you can pass all kinds of elements to FaceTip.

Options
-------

- delay: the time user needs to hold his cursor over the element (in miliseconds)
- attr: if you don't want to store the tip caption on tip (it's not valid), you can specify (i.e. 'rel')


	new FaceTip($$('a.tipped'), { delay: 1000, attr: 'rel' });


Styles
------

They're on facetip.css.

Notes
-----

Thanks to trobrock and foxbunny at #mootools for debuggin with me :)
