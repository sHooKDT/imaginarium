var IGame = angular.module('imaginarium', ['ngAnimate', 'ngWebSocket']);

var gamestate = undefined;

IGame.controller('game-controller', function ($scope, gameData) {

	gamestate = gameData
	gamescope = $scope

	$scope.activepage = 0

    /* Page switcher*/
    //$scope.playerscount = gameData.data.pcount;
    $scope.pages = ['page-lobby', 'page-wait', 'page-turn', 'page-vote', 'page-score'];
    // $scope.activepage = $scope.pages[0];

    /* Join form control */
    $scope.playername = '';
    $scope.formvisible = false;

    $scope.join = function () {
    	gameData.join_game($scope.playername)
    }

    /* Turn controller */
    //$scope.hand = gameData.data.hand;
    $scope.selectedcard = undefined;
    $scope.overlayon = false;
    //$scope.cardass = gameData.data.association;

/*    $scope.choice = function (c_id) {
        $scope.selectedcard = c_id;
        if (gameData.data.main == true) {
            $scope.overlayon = true
        }
        else {
            $scope.send_choice(c_id, '')
        }
    };*/

    //$scope.send_choice = gameData.data.send_choice;

    /* Table var */
   //$scope.table = gameData.data.table


    $scope.startgame = gameData.start_game
});