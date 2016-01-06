(function(){
  'use strict'

  var app = angular.module('shopApp');

  app.controller('LoginController', LoginController);

  LoginController.$inject = ['$scope', 'Api', 'LoginService', '$state', '$rootScope', '$cookies'];

  function LoginController($scope, Api, LoginService, $state, $rootScope, $cookies){
    $scope.signIn = signIn;

    function signIn(){
      LoginService.login($scope.login, $scope.password).then(success, error);

      function success(resp){
        $state.go('main.products');
      }

      function error(resp){
        $scope.error = resp.data.reason;
      }
    }
  }

})();
