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
        users: ["$rootScope", "Api", function($rootScope, Api) {
          return Api.users.query(function(users){
            $rootScope.userName = users[0].username;
          });
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
      templateUrl: "static/templates/orders.html",
      controller: "OrdersController"
    });
  }]);

  app.config(["$resourceProvider", function($resourceProvider){
    $resourceProvider.defaults.stripTrailingSlashes = false;
  }]);
})();
