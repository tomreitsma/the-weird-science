define(function () {

    var SocketHandler = function(url) {
        this.init(url);
    };

    SocketHandler.prototype = {
        _on: {
            'open': function(){ console.warn("on('open', func(){}) not defined"); },
            'close': function(){ console.warn("on('close', func(){}) not defined"); },
            'message': function(){ console.warn("on('message', func(){}) not defined"); },
        },

        init: function(url) {
            var self = this;

            self._ws = new WebSocket(url);

            /**
             * These events have wrappers to preserve scope
             */
            self._ws.onopen = function() {
                self.onopen();
            };

            self._ws.onmessage = function(event) {
                self.onmessage(event);
            }

            self._ws.onclose = function() {
                self.onclose();
            }
        },

        on: function(evt, func) {
            var self = this;

            if(self._on.hasOwnProperty(evt)) {
                self._on[evt] = func;
            }
        },

        onopen: function() {
            var self = this;

            console.dir({self: self});
            self._on['open']();
        },

        onclose: function() {
            var self = this;

            self._on['close']();
        },

        onmessage: function(event) {
            var self = this,
                msg = event.data.split(/\|(.+)?/);

            console.dir({received_message: msg});

            var result = {
                command: msg[0],
                data: JSON.parse(msg[1])
            }

            self._on['message'](result);
        },

        /**
         * Structure:
         * {command}|{json_valid_message}
         */
        send: function(command, data) {
            var self = this,
                message = [command, JSON.stringify(data)].join('|')

            console.dir({sending_message: message});

            self._ws.send(message);
        }
    }

    return SocketHandler;
});