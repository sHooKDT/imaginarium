var IGame = angular.module('imaginarium', []);

IGame.controller('page-switcher', function($scope) {

    $scope.playerscount = 7;
    $scope.pages = ['page-lobby', 'page-wait', 'page-turn', 'page-main-turn', 'page-vote', 'page-score'];
    $scope.activepage = $scope.pages[0];

 })

IGame.controller('player-join', function($scope) {
	$scope.playername = '';
    $scope.formvisible = false;

    $scope.joingame = function () {
    	console.log('Player wants to join game with name ' + $scope.playername)
    }
})
