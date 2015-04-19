function initialise() {
    c_screen_to('page-lobby');
    console.log('Page loaded');
}

function c_screen_to(tar_class) {
    var pages = document.body.getElementsByClassName('sw-page');

    for (i = 0; i < pages.length; i++) {
        if (!pages.item(i).classList.contains(tar_class)) {
            pages.item(i).style.display = 'none';
        }
        else {pages.item(i).style.display = 'block'
                     if (pages.item(i).classList.contains('map-on')) {
            pages.item(i).style.width = '75%';
            document.body.getElementsByClassName('map-bar').item(0).style.display = 'block';
        }
        else {
            pages.item(i).style.width = '100%';
            document.body.getElementsByClassName('map-bar').item(0).style.display = 'none';
        }
             }
    }
    document.body.getElementsByClassName('c_cards').
    var n_screen = document.body.getElementsByClassName(tar_class).item(0)
    n_screen.insertAdjacentHTML('beforeend', '<div class="c_cards"><div class="card" onclick="select_card(0)"></div><div class="card" onclick="select_card(1)"></div><div class="card" onclick="select_card(2)"></div><div class="card" onclick="select_card(3)"></div><div class="card" onclick="select_card(4)"></div><div class="card" onclick="select_card(5)"></div></div>')
}

function toggle_map() {
    if (document.body.getElementsByClassName('map-bar').item(0).style.display == 'block') {
        document.body.getElementsByClassName('map-bar').item(0).style.display = 'none';
        // document.body.getElementsByClassName('sw-page').item(0).style.width = 'none';
    }
    else {
        document.body.getElementsByClassName('map-bar').item(0).style.display = 'block'
    }
}

function join_game() {
    gameSocket.send(JSON.stringify({
        type: 'join',
        data: document.getElementById('player-name').value
    }))
}

function update_cards(cards) {
    cards.forEach(function (card, i, array) {
      c_style = document.body.getElementsByClassName('card').item(i).style;
      var pic = 'url("res/cards/' + card + '.jpg")';
      c_style.backgroundImage = pic;
      c_style.backgroundSize = '100% 100%'
    })
}

function select_card(id) {
    document.body.getElementsByClassName('modal-accept').item(0).style.display = 'block';
    card_view = document.body.getElementsByClassName('card_view').item(0).style;
    card_view.backgroundImage = 'url("../res/cards/' + id + '.jpg")';
    card_view.backgroundSize = '100% 100%'

    gameSocket.send(json.stringify({
      type: 'choice',
      choice: id,
      data: cur_ass
    }))
}
 /*
function close_modal() {
    document.body.getElementsByClassName('modal-accept').item(0).style.display = 'none';
}

function turn_accept() {

}
*/
