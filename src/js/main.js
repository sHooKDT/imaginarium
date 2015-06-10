var IGame = angular.module('imaginarium', ['ngAnimate', 'ngWebSocket']);
var gamescope = undefined;
IGame.controller('game-controller', function ($scope, gameData) {

    gamescope = $scope;
    $scope.debug_mode = false; // Show debug panel
    $scope.debug_fill = function () {
        $scope.score_table = [
            {name:'Natasha',turn:27,vote:67,score:11,main:false},
            {name:'Time',turn:54,vote:53,score:20,main:true},
            {name:'Vanya',turn:24,vote:11,score:99,main:false},
            {name:'Zhenya',turn:12,vote:9,score:1,main:false}
        ];
        $scope.state.hand = [44, 22, 33, 11, 99, 44];
        $scope.state.table = [22, 44, 11, 66, 77, 88];
        $scope.state.association = 'Grandmother'
        $scope.win_table = {
            winner: 'Denis',
            players: ['Vanya', 'Oleg', 'Bob', 'Bill']
        }
    }

    $scope.state = {
        stage: 0,
        hand: [],
        main: false,
        table: [],
        pcount: 0,
        association: '',
        name: ''
    };

    $scope.score_table = [
        // {name:'Natasha',turn:27,vote:67,score:11,main:false},
        // {name:'Time',turn:54,vote:53,score:10,main:true},
        // {name:'Vanya',turn:24,vote:11,score:9,main:false},
        // {name:'Zhenya',turn:12,vote:9,score:1,main:false}
    ]

    $scope.win_table = {};

    $scope.$on('score-update', function(event, new_score) {
        temp_score = new_score;
        for (i=0;i<new_score.length;i++) {
            if ($scope.score_table.length >= 1) {
                temp_score[i].delta = new_score[i].score - $scope.score_table[i].score;
            }
            else {temp_score[i].delta = new_score[i].score}
        }
        $scope.score_table = temp_score;
    });

    $scope.$on('state-update', function(event, state) {
        $scope.state = state;
        // Page switch
        switch (state.stage) {
            case 0:
                $scope.activepage = 0;
                break;
            case 1:
                if (state.main) {$scope.activepage = 2} else {$scope.activepage = 1}
                break;
            case 2:
                if (!state.main) {$scope.activepage = 2} else {$scope.activepage = 1}
                break;
            case 3:
                if (!state.main) {$scope.activepage = 3} else {$scope.activepage = 1}
                break;
            case 4:
                $scope.activepage = 4;
                break;
            case 5:
                $scope.activepage = 5;
        }
    });


    /* Pages initialization */
    $scope.pages = ['page-lobby', 'page-wait', 'page-turn', 'page-vote', 'page-score', 'page-win'];
    $scope.activepage = 1;

    /* Join form control */
    $scope.form = {state: 0}

    $scope.join = function () {
    	gameData.join_game($scope.state.name);
        $scope.form.state = 2
    };

    /* Start game handler (form switch) */
    $scope.start_ready = false;
    $scope.start_game = function () {
        $scope.activepage = 1;
        gameData.start_game();
    }

    /* Turn controller */
    $scope.selectedcard = undefined;
    $scope.overlayon = false;

    $scope.choice = function (c_id, w_ass) {
        $scope.selectedcard = c_id;
        if ($scope.state.main && !w_ass) {
            $scope.overlayon = true
        }
        else {
            $scope.send_choice(c_id, $scope.state.association);
            $scope.activepage = 1;
            $scope.overlayon = false
        }
    };

    $scope.send_choice = gameData.send_choice;
});