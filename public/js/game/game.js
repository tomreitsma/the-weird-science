define( ['vendor/jquery', 'lib/socket', 'game/games/tetris'],
function ($, Socket, GameTetris) {

    var GameHandler = function() {
        this.init();
    }

    GameHandler.prototype = {
        init: function() {
            var self = this;

            self.game = GameTetris;

            self.connectBackend().then(function(socket) {
                self.socket = socket;

                self.socket.send('create_lobby', {
                    name: 'TestLobby',
                    game: 'TETRIS'
                });

                self.startGame();
            });
        },

        startGame: function() {
            var self = this;

            self._game_instance = new self.game({socket: self.socket});

            self.socket.send('start_game', {});
        },

        messageReceived: function(data) {
            //console.dir({received_message_data: data});
        },

        connectBackend: function() {
            var self = this;

            return new Promise(function(resolve, reject) {
                var socket = new Socket('ws://localhost:9000/');

                socket.on('open', function() {
                    socket.send('set_nickname', {name: 'Tom'});
                    resolve(socket);
                });

                socket.on('message', function(data) {
                    self.messageReceived(data);
                });
            });
        },
    };

    return new GameHandler();
});