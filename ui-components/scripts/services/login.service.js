(function(){
  'use strict'

  var app = angular.module('shopApp');

  app.factory('LoginService', loginService);

  loginService.$inject = ['$http'];

  function loginService($http){
    return {
      login: function(username, password){
        var request = {
          method: 'POST',
          url: '/api/v1/login/login/',
          headers: {
            'Content-Type': 'application/json'
          },
          data: {
            login: username,
            password: password, 
          }       
        }

        return $http(request);
      },
      logout: function(){
        var request = {
          method: 'GET',
          url: '/api/v1/login/logout/',
          headers: {
            'Content-Type': 'application/json'
          }
        }

        return $http(request);
      }
    }
  }

})();
