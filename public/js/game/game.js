define( ['vendor/jquery', 'vendor/promise', 'lib/socket', 'lib/StateMachine'],
function ($, Promise, Socket, StateMachine) {

    console.dir({s: Socket});

    var GameHandler = function() {
        this.init();
    }

    GameHandler.prototype = {
        init: function() {
            var self = this;


        },

        connectBackend: function() {

        },
    };

    var socket = new Socket('ws://localhost:9000/');

    socket.on('open', function() {
        console.log('Open function called');
        socket.send('set_nickname', {name: 'Tom'});

        socket.send('list_games', {});
    });

    socket.on('message', function(event) {
        console.log('Message received: ' + event.data);
    });
});