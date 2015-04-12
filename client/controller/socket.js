var gameSocket = new WebSocket('ws://localhost:8275/socket');

/*
protocol = {
    type: 'id, turn, vote, main_turn, score, status',
    id: 'id',
    choice: 'choose',
    data: 'ass'
}
*/

gameSocket.onopen = function () {
   /* give_id = {
        type: 'res_id'
    }
    gameSocket.send(JSON.stringify(give_id)) */
}

gameSocket.onmessage = function (event) {
    var data = JSON.parse(event.data)
    switch(data.type) {
        case 'id':
            clientID = data.id;
            break;
        case 'status':
            console.log(data.data);
            break;
    }
}

function send_smth(smth) {
    gameSocket.send(smth)
}

