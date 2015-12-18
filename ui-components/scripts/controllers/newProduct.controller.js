(function(){
  'use sctrict'

  var app = angular.module('shopApp');

  app.controller('NewProductController', NewProductController);

  NewProductController.$inject = ['$scope', 'Api', 'users', 'productsCategories', '$uibModalInstance'];

  function NewProductController($scope, Api, users, productsCategories, $uibModalInstance){
    $scope.categories = productsCategories;
    $scope.product = new Api.products();

    $scope.save = save;
    $scope.cancel = cancel;


    function save(formIsValid){
      if (!formIsValid) {
        return;
      }
      $scope.product.$save(function(data){
        console.dir(data);
        $uibModalInstance.close(data);
      });
    }

    function cancel(){
      $uibModalInstance.dismiss();
    }
  }

})();
