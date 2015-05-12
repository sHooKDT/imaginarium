var IGame = angular.module('imaginarium', ['ngAnimate'])


IGame.controller('page-switcher', function($scope) {

	example_scope = $scope
    $scope.playerscount = 7;
    $scope.pages = ['page-lobby', 'page-wait', 'page-turn', 'page-vote', 'page-score'];
    $scope.activepage = $scope.pages[3];

 })

IGame.controller('player-join', function($scope) {

	$scope.playername = '';
    $scope.formvisible = false;

    $scope.joingame = function () {
    	console.log('Player wants to join game with name ' + $scope.playername)
    }

})

IGame.controller('turn-controller', function($scope) {

	$scope.cards = [0, 44, 72, 144, 2, 1]
	$scope.selectedcard = undefined
	$scope.overlayon = false
	$scope.cardass = ''

	$scope.clickcard = function (c_id) {
		console.log('Player selected card: ' + c_id)
		$scope.selectedcard = c_id
		$scope.overlayon = true
	}

	$scope.choice = function () {
		console.log('Player selected card ' + $scope.selectedcard + ' and wrote assocication: ' + $scope.cardass)
	}
})

IGame.controller('vote-controller', function($scope) {

	$scope.table = [5, 6, 7, 99, 555, 2]
	$scope.selectedcard = undefined

	$scope.clickcard = function (c_id) {
		console.log('Player selected card: ' + c_id)
		$scope.selectedcard = c_id
		$scope.overlayon = true
	}
})
