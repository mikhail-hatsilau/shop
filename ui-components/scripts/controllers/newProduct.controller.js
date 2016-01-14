(function(){
  'use sctrict'

  var app = angular.module('shopApp');

  app.controller('NewProductController', NewProductController);

  NewProductController.$inject = ['$scope', 'Api', 'user', 'productsCategories', '$uibModalInstance'];

  function NewProductController($scope, Api, user, productsCategories, $uibModalInstance){

    $scope.categories = productsCategories;
    $scope.product = new Api.products();

    $scope.minDate = new Date();
    $scope.fromOpened = false;
    $scope.toOpened = false;
    $scope.dateFormat = 'dd-MM-yyyy';

    $scope.save = save;
    $scope.cancel = cancel;
    $scope.openFrom = openFrom;
    $scope.openTo = openTo;

    function openFrom($event){
      $scope.fromOpened= true;
      $event.preventDefault();
    }

    function openTo($event){
      $scope.toOpened= true;
      $event.preventDefault();
    }


    function save(){
      $scope.product.seller = user.resource_uri;
      $scope.product.$save(function(data){
        $uibModalInstance.close(data);
      });
    }

    function cancel(){
      $uibModalInstance.dismiss();
    }
  }

})();
