var IGame = angular.module('imaginarium', ['ngAnimate', 'ngWebSocket']);
var gamescope = undefined;
IGame.controller('game-controller', function ($scope, gameData) {

    gamescope = $scope;

    $scope.state = {
        stage: 0,
        hand: [],
        main: false,
        table: [],
        score: [],
        pcount: 0,
        association: '',
        name: ''
    };

    $scope.$on('info-update', function(event, state) {
        $scope.state = state
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
                $scope.activepage = 3
                break;
            case 4:
                $scope.activepage = 4
                break;
        }
        console.log(state)
    })


    /* Pages initialization */
    $scope.pages = ['page-lobby', 'page-wait', 'page-turn', 'page-vote', 'page-score'];
    $scope.activepage = $scope.pages[0];

    /* Join form control */
    $scope.formvisible = false;

    $scope.join = function () {
    	gameData.join_game($scope.state.name)
    }

    /* Turn controller */
    $scope.selectedcard = undefined;
    $scope.overlayon = false;

    $scope.choice = function (c_id, w_ass) {
        $scope.selectedcard = c_id;
        console.log('Choice: ' + c_id)
        if ($scope.state.main && !w_ass) {
            $scope.overlayon = true
        }
        else {
            console.log('Sending choice: ' + c_id + ', ass: ' + $scope.state.association)
            $scope.send_choice(c_id, $scope.state.association);
            $scope.activepage = 1
            $scope.overlayon = false
        }
    };

    $scope.send_choice = gameData.send_choice;
    $scope.start_game = gameData.start_game
});