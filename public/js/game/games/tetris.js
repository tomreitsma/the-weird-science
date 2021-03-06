define(['vendor/jquery', 'lib/keyboardhandler'], function (_$, KeyboardHandler) {

    var config = require('config');

    var canvas = document.createElement('canvas');

    $(canvas).attr('id', 'tetris_canvas')
        .attr('width', config.CANVAS_WIDTH)
        .attr('height', config.CANVAS_HEIGHT)
        .text('unsupported browser');

    $('body').append(canvas);

    var grid_size = config.GRID_SIZE, // w/h
        grid_cell_height = 25,
        grid_cell_width = 25,
        grid_padding = 10,
        grid_cell_padding = 0.5;

    var context = canvas.getContext("2d");

    function drawBoard(board_data) {

        context.clearRect(0, 0, canvas.width, canvas.height);

        for(var y=0; y<grid_size[1]; y++) {
            for(var x=0; x<grid_size[0]; x++) {
                context.beginPath();
                context.lineWidth=0.5;
                context.strokeStyle="black";
                context.rect(
                    x * grid_cell_width+grid_cell_padding,
                    y * grid_cell_height+grid_cell_padding,
                    grid_cell_height,
                    grid_cell_width
                );

                context.stroke();

                if(board_data && board_data[y][x] == 1) {
                    context.fillStyle = "#000";
                    context.fill();
                }
            }
        }
    }

    var Tetris = function(options) {
        this.init(options);
    }

    Tetris.prototype = {
        init: function(options) {
            var self = this;

            self.socket = options.socket || null;

            self.socket.clearListeners('update_board');
            self.socket.listen('update_board', self.drawBoard);

            self.setupAudio();
            self.setupKeyBinds();
        },

        setupAudio: function() {
            var self = this;

            var audio_element = $("<audio></audio>").attr({
                'src':'/audio/tetris.ogg',
                'volume':0.4,
                'autoplay':'false'
            });

            self.audio_element = audio_element;

            $(audio_element).appendTo("body");
        },

        setupKeyBinds: function() {
            var self = this;

            KeyboardHandler.addListener([
                KeyboardHandler.ARROW_LEFT,
                KeyboardHandler.ARROW_RIGHT,
                KeyboardHandler.ARROW_UP,
                KeyboardHandler.ARROW_DOWN
            ], function(event) {
                self.socket.send('keypress', {key: event.keyCode});
            });

            KeyboardHandler.addListener([
                KeyboardHandler.KEY_RETURN
            ], function() {
                self.audio_element.prop("muted",!$(self.audio_element).prop("muted"));
            })
        },

        drawBoard: function(data) {
            drawBoard(data);
        }
    };

    return Tetris
});
