function initialise() {
    c_screen_to('page-lobby');
    console.log('Page loaded');
    for (i = 0; i<6; i++) {
        e_style = document.body.getElementsByClassName('card').item(i).style;
        var pic = 'url("res/cards/' + i + '.jpg")';
        e_style.backgroundImage = pic;
        e_style.backgroundSize = '100% 100%'
    }
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
    document.body.getElementsByClassName('intro-form').item(0).style.display = 'none';
    document.body.getElementsByClassName('intro-text').item(0).style.display = 'block';
    gameSocket.send(JSON.stringify({
        type: 'join',
        data: document.getElementById('player-name').value
    }))
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

function close_modal() {
    document.body.getElementsByClassName('modal-accept').item(0).style.display = 'none';
}

function turn_accept() {

}
