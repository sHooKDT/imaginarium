var gameSocket = new WebSocket('ws://localhost:8275/socket');

/*
protocol = {
    type: 'status, choice, join',
    choice: 'card_id',
    data: 'text'
}

client = {
  type: 'choice',
  choice: ,
  data: 'ass'
}

server = {
  type: 'status',
  stage: 'id',
  isMain: false
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
