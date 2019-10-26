
gamemap = require("../src/gamemap.js");
var assert = require("chai").assert;
var jStat = require("jStat");



var m1  =  new gamemap.gamemap.Map(90);
m1.randomize();

describe('MapCast', function() {
    it('bench cast2', function() {
      
      var px=9000/2,
          py=9000/2
      m1.set(px,py,0);


      var resolution = 70; 
      var rangeLimit = 500; 

      
      var res1 = []
      for(var i=0;i<=rangeLimit*1.5;i++){
        res1.push({
          x:px,y:py,height:0,distance:0,length2:0,shading:0,offset:0,

        })
      }
      var raylen=0

      var xpstart = Date.now()
      var xpdur = 1; 
      var durs2 = [];


      //
      while(Date.now()<xpstart+(1000*xpdur)){

        var start = Date.now()
        for(var i=0;i<resolution;i++){

          raylen = gamemap.gamemap.cast2( res1,m1,0,i/100,rangeLimit)

        }
        var end = Date.now();
        var dur = end-start;
        
        durs2.push(dur);



      }
      console.log(" count : "+durs2.length ) 
      console.log(" min   : "+jStat.min(durs2) ) 
      console.log(" mean  : "+jStat.mean(durs2))
      console.log(" max   : "+jStat.max(durs2))
      console.log(" hist  : "+jStat.histogram(durs2))
      console.log(" ------: " )
      

    });
    it('bench Original', function() {
      //console.log(gamemap);
      //console.log(gamemap.gamemap.Map);
      
      //var m1  =  new gamemap.gamemap.Map(9000);
      //m1.randomize();
      
      var px=9000/2,
          py=9000/2
      m1.set(px,py,0);

      var resolution = 70; 
      var rangeLimit = 500; 

      var xpstart = Date.now()
      var xpdur = 1; 
      var durs = []
      
      var res = 0
      while(Date.now()<xpstart+(1000*xpdur)){

        var start = Date.now()
        for(var i=0;i<resolution;i++){

          res = m1.cast({x:px,y:py},i/100,rangeLimit);

        }
        var end = Date.now();
        var dur = end-start;
        
        durs.push(dur);



      }
      
      
      console.log(" count : "+durs.length ) 
      console.log(" min   : "+jStat.min(durs) ) 
      console.log(" mean  : "+jStat.mean(durs))
      console.log(" max   : "+jStat.max(durs))
      console.log(" hist  : "+jStat.histogram(durs))
      console.log("-------: ")
      
      

    });


    it('cast2 returns the same as cast on simple case', function() {
      var m1  =  new gamemap.gamemap.Map(20);
      m1.randomize();
      m1.set(10,10,0);

      var resolution = 344; 
      var rangeLimit = 5; 

      var xpstart = Date.now()
      var xpdur = 1; 
      var durs = []
      
      var px=10,
          py=10,
          angle=1

      res0 = m1.cast({x:px,y:py},angle,rangeLimit)

      
      var res1 = []
      for(var i=0;i<=rangeLimit+6;i++){
        res1.push({
          x:px,y:py,height:0,distance:0,length2:0,shading:0,offset:0,

        })
      }
      raylen = gamemap.gamemap.cast2( res1,m1,0,angle,rangeLimit)

      
        
      assert(res0.length == raylen ,"not same size result");

      for(var i=0;i<res0.length;i++){
        var point0 = res0[i]
        var point1 = res1[i]

        assert(point0.x == point1.x,"not same x")
        assert(point0.y == point1.y,"not same y")
        assert(point0.distance == point1.distance,"not same dist")
        assert(point0.height == point1.height,"not same hei")




      }
      //console.log(res0) 
      //console.log(res1.slice(0,3)) 



    });
    it('cast2 always = cast', function() {
      var m1  =  new gamemap.gamemap.Map(20);
      m1.randomize();
      m1.set(10,10,0);

      var resolution = 600; 
      var rangeLimit = 5; 

      var xpstart = Date.now()
      var xpdur = 1; 
      var durs = []
      
      var px=10,
          py=10,
          angle=1

      

      var res1 = gamemap.gamemap.makeCastBuff(rangeLimit,px,py)
      
      for(angle=0;angle<700;angle++){
        res0 = m1.cast({x:px,y:py},angle/100,rangeLimit)
        raylen = gamemap.gamemap.cast2( res1,m1,0,angle/100,rangeLimit)

        
          
        assert(res0.length == raylen ,"not same size result");

        for(var i=0;i<res0.length;i++){
          var point0 = res0[i]
          var point1 = res1[i]

          assert(point0.x == point1.x,"not same x")
          assert(point0.y == point1.y,"not same y")
          assert(point0.distance == point1.distance,"not same dist")
          assert(point0.height == point1.height,"not same hei")

        }

      }
      //console.log(res0) 
      //console.log(res1.slice(0,3)) 



    });
});
