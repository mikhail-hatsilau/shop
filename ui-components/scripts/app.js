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
        auth: ["$rootScope", "Api", '$timeout', '$cookies', '$location', function($rootScope, Api, $timeout, $cookies, $location) {
            var sessionId = $cookies.get('sessionid');

            if (!sessionId){      
              $location.url('/login');
            } else {
              Api.loggedUser.get(function(data){
                $rootScope.user = data;
                return data;
              });
            }
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

  app.run(['$http', '$cookies', function($http, $cookies){
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.get('csrftoken');
    $http.defaults.xsrfCookieName = 'csrftoken';
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
  }]);
})();
