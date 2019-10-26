




(function(root, factory) {  // eslint-disable-line
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module.
    define([], function() {
      return factory.call(root);
    });
  } else {
    // Browser globals
    root.gamemap = factory.call(root);
  }
}(this, function() {

entity = require("./entity.js")



function Map(size) {
  this.size = size;
  this.wallGrid = new Float32Array(size * size);
  this.entities = [];
  this.light = 0;
}

Map.prototype.get = function(x, y) {
  x = Math.floor(x);
  y = Math.floor(y);
  if (x < 0 || x > this.size - 1 || y < 0 || y > this.size - 1) return -1;
  return this.wallGrid[y * this.size + x];
};


Map.prototype.set = function(x, y,value) {
  x = Math.floor(x);
  y = Math.floor(y);
  if (x < 0 || x > this.size - 1 || y < 0 || y > this.size - 1) return -1;
  this.wallGrid[y * this.size + x]=value;
};
Map.prototype.randomize = function() {
  var e = new entity.Entity(3,3.5)
  this.entities.push(e)
  for (var i = 0; i < this.size ; i++) {
      for (var j = 0; j < this.size ; j++) {
          // make borders
          if ( i==0 || j==0 || i==this.size-1 || j==this.size-1){
              this.set(i,j , 1);
          }else{
              this.set(i,j , 0);
          }


          if ( i>5 && j>5 && i<this.size-1 && j<this.size-1){
            var ran =  Math.random()

            if (ran <0.1){
              //wall
              this.set(i,j , 1);
            }

            else if (ran <0.2){
              var e = new entity.Entity(i+0.5,j+0.5)
              this.entities.push(e)
            }
          }
          //if ( i>5 && j>5){
          //    
          //    this.set(i,j , this.get(i,j)+ Math.random()+0.5 );
          //}
      }
  }

};

Map.prototype.cast = function(point, angle, range) {
  var self = this;
  var sin = Math.sin(angle);
  var cos = Math.cos(angle);
  const noWall = { length2: Infinity };
  return ray({ x: point.x, y: point.y, height: 0, distance: 0 });
  function ray(origin) {
    var stepX = step(sin, cos, origin.x, origin.y);
    var stepY = step(cos, sin, origin.y, origin.x, true);
    var nextStep = stepX.length2 < stepY.length2
      ? inspect(stepX, 1, 0, origin.distance, stepX.y)
      : inspect(stepY, 0, 1, origin.distance, stepY.x);
    if (nextStep.distance > range) return [origin];
    return [origin].concat(ray(nextStep));
  }
  function step(rise, run, x, y, inverted) {
    if (run === 0) return noWall;
    var dx = run > 0 ? Math.floor(x + 1) - x : Math.ceil(x - 1) - x;
    var dy = dx * (rise / run);
    return {
      x: inverted ? y + dy : x + dx,
      y: inverted ? x + dx : y + dy,
      length2: dx * dx + dy * dy
    };
  }
  function inspect(step, shiftX, shiftY, distance, offset) {
    var dx = cos < 0 ? shiftX : 0;
    var dy = sin < 0 ? shiftY : 0;
    step.height = self.get(step.x - dx, step.y - dy);
    step.distance = distance + Math.sqrt(step.length2);
    if (shiftX) step.shading = cos < 0 ? 2 : 0;
    else step.shading = sin < 0 ? 2 : 1;
    step.offset = offset - Math.floor(offset);
    return step;
  }
};
Map.prototype.update = function(seconds) {
  if (this.light > 0) this.light = Math.max(this.light - 10 * seconds, 0);
  else if (Math.random() * 5 < seconds) this.light = 2;
};


var makeCastBuff = function(range,px,py){

  var res1 = []
  for(var i=0;i<=range*2;i++){
    res1.push({
      x:px,y:py,height:0,distance:0,length2:0,shading:0,offset:0,

    })
  }
  return res1
};

var cast2 = function(castBuff,map,buffidx,angle,range){
  
  var sin = Math.sin(angle);
  var cos = Math.cos(angle);

  var stepX = {};
      stepY = {};
      o1 = {};
  return ray(buffidx);




  var ox 
  var oy 
  var odist

  function ray(origin) {
    // in  int   ,   out  int 
    
    ox = castBuff[origin].x
    oy = castBuff[origin].y
    odist = castBuff[origin].distance

    // update stepX and Y
    step(sin, cos, ox, oy,false,stepX);
    step(cos, sin, oy, ox, true,stepY);

    o1 = castBuff[origin+1];
    if(stepX.length2 < stepY.length2){
      o1.x = stepX.x 
      o1.y = stepX.y 
      o1.length2 = stepX.length2

      inspect(o1, 1, 0, odist, stepX.y)
    }else{
      o1.x = stepY.x 
      o1.y = stepY.y 
      o1.length2 = stepY.length2
      inspect(o1, 0, 1, odist, stepY.x);
    }
    if (o1.distance > range) return origin+1;
    return ray(origin+1)
    //return [origin].concat(ray(nextStep));
  }
  function step(rise, run, x, y, inverted,stepbuff) {
    if (run === 0) {
      stepbuff.length2=Infinity;
      return
    } 
    var dx = run > 0 ? Math.floor(x + 1) - x : Math.ceil(x - 1) - x;
    var dy = dx * (rise / run);
    
    stepbuff.x= inverted ? y + dy : x + dx,
    stepbuff.y= inverted ? x + dx : y + dy,
    stepbuff.length2= dx * dx + dy * dy
  }
  function inspect(step, shiftX, shiftY, distance, offset) {
    var dx = cos < 0 ? shiftX : 0;
    var dy = sin < 0 ? shiftY : 0;
    step.height = map.get(step.x - dx, step.y - dy);



    step.distance = distance + Math.sqrt(step.length2);
    step.offset = offset - Math.floor(offset);
    return step;
  }



}





  return {
    Map : Map,
    cast2:cast2,
    makeCastBuff:makeCastBuff
  }


}));
