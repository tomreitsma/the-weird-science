define(function (require) {
    var game = require('./game/game');
    var lobby = require('./game/lobby');

    var $ = require('jquery');
    var Socket = require('./lib/socket');

    var backend_socket = null;

    var config = require('config');

    function connectToBackend() {
        return new Promise(function(resolve, reject) {
            var socket = new Socket('ws://'+config.WEBSOCKET_HOST+':'+config.WEBSOCKET_PORT+'/');

            socket.on('open', function() {
                socket.send('set_nickname', {name: 'Tom'});
                resolve(socket);
            });
        });
    }

    var lobbies_container = $('<div />', {id: 'lobbies_container'});
    $(document.body).append(lobbies_container);

    function displayLobbies(lobby_data) {
        var ul = $('<ul/>');

        $.each(lobby_data, function() {
            var li = $('<li/>', {html:this.name + ': (' + this.clients + ')'});
            var lobby_id = this.id;

            $(li).on('click', function() {
                backend_socket.send('join_lobby', {id:lobby_id});
            });

            ul.append(li);
        });

        var create_lobby_button = $('<input>', {
            type: 'button',
            value: 'Create lobby'
        });

        $(create_lobby_button).on('click', function() {
            backend_socket.send('create_lobby', {
                name: 'TestLobby',
                game: 'TETRIS'
            });
        });

        var li = $('<li/>', {html:create_lobby_button});

        ul.append(li);

        $(lobbies_container).html('');
        $(lobbies_container).append(ul);
    }

    connectToBackend().then(function(socket) {
        backend_socket = socket;
        backend_socket.send('list_lobbies', {});

        backend_socket.listen('list_lobbies', function(lobby_data) {
            displayLobbies(lobby_data);
        });

        backend_socket.listen('create_lobby', function(lobby_data){
            backend_socket.send('list_lobbies', {});
        });

        backend_socket.listen('join_lobby', function() {
            game.setSocket(backend_socket);
            game.startGame();
        });
    })

});