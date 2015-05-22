IGame.factory('gameData', function ($websocket) {

    var gameSocket = $websocket('ws://' + location.host + '/socket');

    var gameState = {
        stage: 0,
        hand: [],
        main: false,
        table: [],
        score: [],
        pcount: 0,
        association: '',
        name: ''
    };

    gameSocket.onMessage(function (mes) {
        var data = JSON.parse(mes.data);
        if (data.type == 'update') {
            gameState = data.state
        }
        console.log('Cur state broadcasted: ' + gameState)
        gamescope.$broadcast('info-update', gameState);
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