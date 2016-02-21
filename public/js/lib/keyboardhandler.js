define(['vendor/jquery'], function(_$) {

    var KeyboardHandler = function() {
        this.init();
    }

    KeyboardHandler.prototype = {
        ARROW_UP: 38,
        ARROW_DOWN: 40,
        ARROW_LEFT: 37,
        ARROW_RIGHT: 39,
        KEY_SPACE: 32,
        KEY_RETURN: 13,

        KEY_ANY: 'w00t',

        listeners: {},

        EVENT_KEY_UP: 'keyup',
        EVENT_KEY_DOWN: 'keydown',

        init: function() {
            var self = this;

            console.log('trying something');

            $(document.body).on('keydown', function(event) {
                console.log('got keydown event');
                self.onKeyPress(event);
            });
        },

        addListener: function(keys, func) {
            var self = this;

            if(!(Object.prototype.toString.call(keys) === '[object Array]')) {
                keys = [key];
            }

            for(var i=0; i<keys.length; i++) {
                var key = keys[i];

                if(!self.listeners[key]) {
                    self.listeners[key] = [];
                }

                self.listeners[key].push(func);
            }
        },

        onKeyPress: function(event) {
            var self = this,
                key = event.keyCode;

            if(self.listeners[key]) {
                for(var i=0; i<self.listeners[key].length; i++) {
                    self.listeners[key][i](event);
                }
            }
        }
    }

    return new KeyboardHandler();
});
