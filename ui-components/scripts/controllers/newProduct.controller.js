(function(){
  'use sctrict'

  var app = angular.module('shopApp');

  app.controller('NewProductController', NewProductController);

  NewProductController.$inject = ['$scope', 'Api', 'user', 'productsCategories', '$uibModalInstance'];

  function NewProductController($scope, Api, user, productsCategories, $uibModalInstance){

    $scope.categories = productsCategories;
    $scope.product = new Api.products();

    $scope.save = save;
    $scope.cancel = cancel;


    function save(){
      $scope.product.$save(function(data){
        $uibModalInstance.close(data);
      });
    }

    function cancel(){
      $uibModalInstance.dismiss();
    }
  }

})();
