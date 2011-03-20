/*
---
description: Facebook style tooltips

license: WTFPL

authors: Faruk Can Bilir

requires: core/1.3: '*'

provides: FaceTip
...
*/

var FaceTip = new Class({

    options: {
        attr: 'tip',
        delay: 0
    },

    initialize: function(els, options) {
        Object.append(this.options, options || {});
        els.addEvents({
            'mouseenter': function(e) {
                this.enter($(e.target));
            }.bind(this),
            'mouseleave': function() {
                this.leave();
            }.bind(this)
        });
    },

    enter: function(element) {
        this.on = true;
        this.timer = (function() {
            if (!this.on) {
                clearTimeout(this.timer);
                return;
            }
            var pos = element.getCoordinates();
            var tip = new Element('div', {
                'class': 'facetip',
                styles: {
                    position: 'absolute',
                    left: pos.left
                }
            });
            var arrow = new Element('div', {
                'class': 'facetip-arrow-down'
            });
            tip.set('text', element.getProperty(this.options.attr));
            arrow.inject(tip);
            if (tip.get('text') !== "") {
                tip.inject($$('body')[0]);
            }
            var tipHeight = tip.getSize().y;
            arrow.setStyle('top', tipHeight);
            tip.setStyle('top', pos.top - tipHeight - parseInt(arrow.getStyle('border-top')));
        }).bind(this).delay(this.options.delay);
    },

    leave: function() {
        if (this.on) {
            $$('.facetip').dispose();
        }
        this.on = false;
        clearTimeout(this.timer);
    }
});