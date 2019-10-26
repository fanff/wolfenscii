
(function(root, factory) {  // eslint-disable-line
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module.
    define([], function() {
      return factory.call(root);
    });
  } else {
    // Browser globals
    root.Entity = factory.call(root);
  }
}(this, function() {




function Entity(x,y) {
  this.x = x;
  this.y = y;



  this.angleToPlayer = Math.PI
  this.distanceToPlayer = 1000
  this.ppg = {}
  this.colCenter = 0
  this.sprite = 0
}




  return {
    Entity : Entity
  }


}));
