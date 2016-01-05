(function(){
  'use strict'

  var app = angular.module('shopApp');

  app.controller('MainController', mainController);

  mainController.$inject = ['$scope', '$rootScope', 'LoginService', '$state', '$cacheFactory', 'localStorageService'];

  function mainController($scope, $rootScope, LoginService, $state, $cacheFactory, localStorageService){
    
    $scope.logout = logout;

    function logout(){
      LoginService.logout().then(success, error);

      function success(resp){
        var cache = $cacheFactory.get('productsCache');
        if (cache) {
          cache.removeAll();
        }
        localStorageService.clearAll();
        delete $rootScope.user;
        delete $rootScope.token;
        $state.go('login');
      }
 
      function error(resp){
        console.log('error');
      }
    }
  }

})();
