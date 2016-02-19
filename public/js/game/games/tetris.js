define(['vendor/jquery'], function (_$) {

    CANVAS_WIDTH = 500;
    CANVAS_HEIGHT = 500;

    GRID_SIZE = 10

    var canvas = document.createElement('canvas');

    $(canvas).attr('id', 'tetris_canvas')
        .attr('width', CANVAS_WIDTH)
        .attr('height', CANVAS_HEIGHT)
        .text('unsupported browser');

    $('body').append(canvas);

    var grid_size = [10, 22], // w/h
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
            console.dir({got_socket: self.socket});

            self.socket.listen('update_board', self.drawBoard);
        },

        drawBoard: function(data) {
            console.dir({got_in_draw_board: data});

            drawBoard(data);
        }
    };

    return Tetris
});
