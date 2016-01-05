(function(){
  'use strict'

  var app = angular.module("shopApp");

  app.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider){
    
  $urlRouterProvider.otherwise('products');

  $stateProvider.
    state("main", {
      abstract: true,
      template: "<ui-view>",
      resolve: {
        auth: ["$rootScope", "Api", '$q', '$state', '$timeout', '$cookies', function($rootScope, Api, $q, $state, $timeout, $cookies) {
          var deferred = $q.defer(),
              sessionId = $cookies.get('sessionid');

          $timeout(function(){
            if (!sessionId){      
              $state.go('login');
              deferred.reject();
            } else {
              $rootScope.token = $cookies.get('csrftoken');
              Api.users($rootScope.token).query(function(users){
                $rootScope.user = users[0];
                deferred.resolve(users);
              });
            }
          });

          return deferred.promise;
        }]
      }
    }).
    state("main.products", {
      url: "/products",
      templateUrl: "/static/templates/products.html",
      controller: "ProductsController",
    }).
    state("main.details", {
      url: "/products/:id",
      templateUrl: "/static/templates/product-details.html",
      controller: "ProductDetailsController"
    }).
    state("main.orders", {
      url: "/orders",
      templateUrl: "/static/templates/orders.html",
      controller: "OrdersController"
    }).
    state("main.newProduct", {
      url: "/product/new",
      templateUrl: "/static/templates/new-product.html",
      controller: "NewProductController"
    }).
    state("login", {
      url: '/login',
      templateUrl: '/static/templates/login.html',
      controller: 'LoginController'
    });
  }]);

  app.config(["$resourceProvider", function($resourceProvider){
    $resourceProvider.defaults.stripTrailingSlashes = false;
  }]);

  app.config(['localStorageServiceProvider', function(localStorageServiceProvider){
    localStorageServiceProvider.setPrefix('ShopApp');
  }])
})();
