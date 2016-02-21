define( ['vendor/jquery', 'lib/socket', 'game/games/tetris'],
function ($, Socket, GameTetris) {

    var GameHandler = function() {
        this.init();
    }

    GameHandler.prototype = {
        init: function() {
            var self = this;

            self.game = GameTetris;
        },

        setSocket: function(socket) {
            var self = this;

            self.socket = socket;
        },

        startGame: function() {
            var self = this;

            self._game_instance = new self.game({socket: self.socket});
            self.socket.send('start_game', {});
        }
    };

    return new GameHandler();
});