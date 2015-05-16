IGame.factory('gameData', function ($websocket) {

    var gameSocket = $websocket('ws://' + location.host + '/socket');

    var gameState = {
        stage: 0,
        hand: [],
        main: false,
        table: [],
        score: [],
        pcount: 0
    };

    gameSocket.onMessage(function (mes) {
        var data = JSON.parse(mes.data);
        console.log(mes)
        console.log(data)
        if (data.type == 'status') {
            gameState.stage = data.stage;
            gameState.hand = data.hand;
            gameState.main = data.main;
            gameState.table = data.table;
            gameState.score = data.score;
            gameState.association = data.association
        }
        else {
            if (data.type == 'lobby') {
                //noinspection CommaExpressionJS
                gameState.pcount = data.pcount,
                    gameState.stage = data.stage
            }
        }
    });

    function send_choice(c_id, ass) {
        gameSocket.send(JSON.stringify({
            type: 'choice',
            choice: c_id,
            data: ass
        }))
    }

    function join_game(name) {
        gameSocket.send(JSON.stringify({
            type: 'join',
            data: name
        }))
    }

    function start_game() {
        gameSocket.send(JSON.stringify({
            type: 'start'
        }))
    }

    return {
        stage: gameState.stage,
        hand: gameState.hand,
        main: gameState.main,
        table: gameState.table,
        score: gameState.score,
        association: gameState.association,
        pcount: gameState.pcount,

        send_choice: send_choice,
        join_game: join_game,
        start_game: start_game
    }
});