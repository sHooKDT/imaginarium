var IGame = angular.module('imaginarium', ['ngAnimate', 'ngWebSocket']);
var gamescope = undefined;
IGame.controller('game-controller', function ($scope, gameData) {

    gamescope = $scope;
    $scope.debug_mode = false; // Show debug panel

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

    $scope.$on('score-update', function(event, new_score) {
        console.log('Got new score at scope context: ' + new_score);
        temp_score = new_score;
        console.log('Temping success: ' + temp_score)
        for (i=0;i<new_score.length;i++) {
            if ($scope.score_table.length >= 1) {
                temp_score[i].delta = new_score[i].score - $scope.score_table[i].score;
            }
            else {temp_score[i].delta = new_score[i].score}
        }
        $scope.score_table = temp_score;
        console.log('Score updated: ' + $scope.score_table)
    })

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
        }
    });


    /* Pages initialization */
    $scope.pages = ['page-lobby', 'page-wait', 'page-turn', 'page-vote', 'page-score'];
    $scope.activepage = 0;

    /* Join form control */
    $scope.formvisible = false;

    $scope.join = function () {
    	gameData.join_game($scope.state.name);
        $scope.start_ready = true
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
        console.log('Choice: ' + c_id);
        if ($scope.state.main && !w_ass) {
            $scope.overlayon = true
        }
        else {
            console.log('Sending choice: ' + c_id + ', ass: ' + $scope.state.association);
            $scope.send_choice(c_id, $scope.state.association);
            $scope.activepage = 1;
            $scope.overlayon = false
        }
    };

    $scope.send_choice = gameData.send_choice;
});