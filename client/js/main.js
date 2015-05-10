var IGame = angular.module('imaginarium', []);

IGame.controller('page-switcher', function($scope) {

    $scope.pcount = 7;
    $scope.pages = ['page-lobby', 'page-wait', 'page-turn', 'page-main-turn', 'page-vote', 'page-score'];
    $scope.activepage = $scope.pages[0];

 })