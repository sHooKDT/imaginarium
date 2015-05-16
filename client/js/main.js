var IGame = angular.module('imaginarium', ['ngAnimate', 'ngWebSocket']);

var gamestate = undefined;

IGame.controller('game-controller', function ($scope, gameData) {

    // Object.observe(gameData, function(changes) {
    //     $scope.$spply
    // })
    
    $scope.$watch(gameData, function() {
        console.log('data changed');
        $scope.state = gameData;
    });

    $scope.state = gameData

	$scope.activepage = 0

    /* Page switcher*/
    $scope.playerscount = $scope.state.pcount;
    $scope.pages = ['page-lobby', 'page-wait', 'page-turn', 'page-vote', 'page-score'];
    // $scope.activepage = $scope.pages[0];

    /* Join form control */
    $scope.playername = '';
    $scope.formvisible = false;

    $scope.join = function () {
    	gameData.join_game($scope.playername)
    }

    /* Turn controller */
    $scope.hand = $scope.state.hand;
    $scope.selectedcard = undefined;
    $scope.overlayon = false;
    $scope.cardass = $scope.state.association;

    $scope.choice = function (c_id) {
        $scope.selectedcard = c_id;
        if ($scope.state.main == true) {
            $scope.overlayon = true
        }
        else {
            $scope.send_choice(c_id, '')
        }
    };

    $scope.send_choice = $scope.state.send_choice;

    /* Table var */
    $scope.table = $scope.state.table


    $scope.startgame = $scope.state.start_game
});