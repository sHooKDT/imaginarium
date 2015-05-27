IGame.factory('gameData', function ($websocket) {

    var gameSocket = $websocket('ws://' + location.host + '/socket');

    var gameState = {
        stage: 0,
        hand: [],
        main: false,
        table: [],
        pcount: 0,
        association: '',
        name: ''
    };

    var scoreTable = []

    gameSocket.onMessage(function (mes) {
        var data = JSON.parse(mes.data);
        switch (data.type) {
            case 'update':
                gameState = data.state;
                gamescope.$broadcast('state-update', gameState);
                break;
            case 'score':
                scoreTable = data.score;
                gamescope.$broadcast('score-update', scoreTable);
                break;
        }
    });

    function send_choice(c_id, ass) {
        console.log('Sending choice, id: %d, ass: ' + ass, c_id)
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
        state: gameState,
        send_choice: send_choice,
        join_game: join_game,
        start_game: start_game
    }
});