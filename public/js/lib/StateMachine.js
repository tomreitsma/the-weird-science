define(function () {

    var StateMachine = function() {

    };

    StateMachine.Subscription = function(){
        this.init();
    };
    StateMachine.Subscription.prototype = {
        name: null,

        init: function() {
            this.data = [];
            this.__onInitial_cb_stack__ = [];
            this.__onUpdate_cb_stack__ = [];
        },

        hasData: function() {
            return this.data.length > 0;
        },

        addData: function(data) {
            this.data.push(data);
        },

        onUpdate: function(func) {
            if(!$.isFunction(func)) {
                this.addData(func);
                $.each(this.__onUpdate_cb_stack__, function() {
                    this(func);
                });
            } else {
                this.__onUpdate_cb_stack__.push(func);
            }

            return this;
        },

        onInitial: function(func) {
            if(!$.isFunction(func)) {
                this.addData(func);
                $.each(this.__onInitial_cb_stack__, function() {
                    this(func);
                });
            } else {
                this.__onInitial_cb_stack__.push(func);
            }

            return this;
        }
    };

    StateMachine.prototype = {
        __subscriptions__: {},
        __listeners__: {},

        /**
         * Connect the statemachine to the active websocket connection.
         */
        connect: function(ws) {
            var self = this;
            this.ws = ws;
            this.ws.onmessage = function(data) {
                self.handle_message(data);
            }
        },

        handle_message: function(msg) {
            if(!msg.key) {
                if(this.__listeners__[msg.type]) {
                    $.each(this.__listeners__[msg.type], function() {
                        this(msg);
                    });
                }
            }

            if(msg.type && msg.key) {
                var _sn = msg.type + '_' + msg.key,
                    sub = this.__subscriptions__[_sn];

                if(!sub) {
                    //console.warn('No subscription for ' + _sn);
                }

                if(sub.hasData()) {
                    return sub.onUpdate(msg.data);
                } else {
                    return sub.onInitial(msg.data);
                }
            }
        },

        subscription: function(type, identifier) {
            return this.__subscriptions__[type+'_'+identifier];
        },

        listen: function(type, func) {
            if(!this.__listeners__[type]) {
                this.__listeners__[type] = [];
            }

            this.__listeners__[type].push(func);
        },

        subscribe: function(type, key) {
            var _sn = type + '_' + key;
            if(this.__subscriptions__[_sn]) {
                return this.__subscriptions__[_sn];
            }

            this.ws.call({
                type: 'sub',
                data: {
                    type: type,
                    key: key
                }
            });

            var sub_obj = new StateMachine.Subscription();
            sub_obj.type = type;
            sub_obj.key = key;
            this.__subscriptions__[_sn] = sub_obj;

            return this.__subscriptions__[_sn];
        },

        unsubscribe: function(type, key) {
            var _sn = type + '_' + key;

            if(this.__subscriptions__[_sn]) {
                this.__subscriptions__[_sn].data = [];
                delete this.__subscriptions__[_sn];
            } else {
                //console.error('Tried to delete subscription '+_sn);
            }

            this.ws.call({
                type: 'unsub',
                data: {
                    type: type,
                    key: key
                }
            });

            return this;
        },

        unsubscribeAll: function() {
            var self = this;
            $.each(this.__subscriptions__, function() {
                self.unsubscribe(this.type, this.key);
            });
        }
    };

    return StateMachine;
});