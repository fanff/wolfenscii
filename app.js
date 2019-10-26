
webglUtils = require('./extra/webgl-utils.js');
m4 = require('./extra/m4.js');

gamemap = require("./src/gamemap.js")


function randLine(linelen) {
  var text = "";
  var possible = "abcdefghijklmnopqrstuvwxyz0123456789";

  for (var i = 0; i < linelen; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));

  return text;
}


function makePosition(fontInfo,len,lineCount,numComponents) {
  var numVertices = lineCount*len * 1;
  var positions = new Float32Array(numVertices * numComponents);

  var offset = 0;


  var y = fontInfo.letterHeight/2;
  for (var lineid = 0; lineid < lineCount; ++lineid) {
      var x = fontInfo.letterWidth/2;
      for (var ii = 0; ii < len; ++ii) {
          var x2 = x + fontInfo.letterWidth;

          // 6 vertices per letter
          positions[offset++] = x;
          positions[offset++] = y;
          if(numComponents>=3) positions[offset++] = 0.1;
          if(numComponents==4) positions[offset++] = 1;

          //positions[offset++] = x2;
          //positions[offset++] = y;
          //if(numComponents==3) positions[offset++] = 0.9;

          //positions[offset++] = x;
          //positions[offset++] = y+fontInfo.letterHeight;
          //if(numComponents==3) positions[offset++] = 0.9;

          //positions[offset++] = x;
          //positions[offset++] = y+fontInfo.letterHeight;
          //if(numComponents==3) positions[offset++] = 0.1;

          //positions[offset++] = x2;
          //positions[offset++] = y;
          //if(numComponents==3) positions[offset++] = 0.9;

          //positions[offset++] = x2;
          //positions[offset++] = y+fontInfo.letterHeight;
          //if(numComponents==3) positions[offset++] = 0.9;

          x += fontInfo.letterWidth
      }
      y+=fontInfo.letterHeight
  }

  for(var offset=0;offset< numVertices*numComponents;offset+=numComponents){
    positions[offset]=   positions[offset]/ (x/2)   - 1.0
  }
  for(var offset=1;offset< numVertices*numComponents;offset+=numComponents){
    positions[offset]=   positions[offset]/ (y/2)   - 1.0
  }
  return positions;
}
      

      function FontInfo(imageFontInfo){
        
         //console.log(imageFontInfo)         

         this.letterHeight= 8
         this.letterWidth= 8

         this.textureWidth= 0
         this.textureHeight= 0
         this.glyphSet=imageFontInfo.glyphSet
         this.inLetterWidth=imageFontInfo.inLetterWidth
         this.inLetterHeight=imageFontInfo.inLetterHeight

         this.glyphInfos=[] 
      }
      FontInfo.prototype.preLoad=function(textureWidth,textureHeight,inLetterWidth,inLetterHeight){
          this.textureWidth  = textureWidth;
          this.textureHeight = textureHeight;
          
          this.glyphByRow = textureWidth/inLetterWidth;
          this.glyphByCol = textureHeight/inLetterHeight;

          this.glyphInfos=[]

          var maxX = this.textureWidth;
          var maxY = this.textureHeight;
          //console.log(this.fontInfo.glyphInfos);
          var glyphId=0
          //console.log("preload now! ",maxX,maxY)
          // glyphID = y* maxX+ x
          for(var y =0;y<maxY;y+=inLetterHeight){
              for(var x =0;x<maxX;x+=inLetterWidth){

                  
                  //console.log(glyphId,this.glyphSet[glyphId],x,y)
                  
                  u1 = x / maxX;
                  v1 = (y + inLetterWidth-1) / maxY;
                  u2 = (x + inLetterWidth-1) / maxX;
                  v2 = y / maxY;
                  
                  //console.log(i,this.glyphSet[i],glyphInfo);
                  var uvBuff = new Float32Array(12)
                  uvBuff[0] = u1;
                  uvBuff[1] = v1;

                  uvBuff[2] = u2;
                  uvBuff[3] = v1;

                  uvBuff[4] = u1;
                  uvBuff[5] = v2;

                  uvBuff[6] = u1;
                  uvBuff[7] = v2;

                  uvBuff[8] = u2;
                  uvBuff[9] = v1;

                  uvBuff[10] =u2;
                  uvBuff[11] =v2;

                  this.glyphInfos.push(uvBuff)
                  glyphId+=1;
              }
          }
      }
      FontInfo.prototype.getUV=function(glyphId){
          let res = this.glyphInfos[glyphId]
          if(res){
              return res
          }else{
              return new Float32Array(12)
          } 
      }
      FontInfo.prototype.getCharUV=function(cha){
          let res = this.glyphSet.indexOf(cha)
          if(res>=0){
              return this.getUV(res)
          }else{
              return new Float32Array(12)
          } 
      }
      FontInfo.prototype.getCharGlyphId=function(cha){
          return this.glyphSet.indexOf(cha)
      }




      function Sbuff() {
      }
      Sbuff.prototype.init=function (lines,cols,fontInfo){
          this.sbuff_lines = lines;
          this.sbuff_cols = cols;
          this.posbuff= false;
          this.fontInfo = fontInfo;    
          this.shadingbuff= new Float32Array(4*lines*cols)
          this.fullBright = new Float32Array([999.9,999.9,1,1])
          
          
          this.cBLACK = new Float32Array([.0,.0,.0])
          this.cRED = new Float32Array([.9,.0,.0])
          this.cGREEN = new Float32Array([.0,.9,.0])
          this.cBLUE = new Float32Array([.0,.0,.9])
          this.cWHITE = new Float32Array([.9,.9,.9])
          return this
      }

      Sbuff.prototype.shadingColor=function(color1){
        return this.computeShading(color1,color1,1,0);
      }
      Sbuff.prototype.computeShading=function(color1,color2,period,phase){
        // color bw 0->9,
        // period in second -> 0.00->9
        // phase in second -> 0.0000 -> 9
        return new Float32Array([
          period/10.0+color1[0]*10+color1[1]*100+color1[2]*1000,
          phase/10.0+color2[0]*10+color2[1]*100+color2[2]*1000,
          1.0,
          1.0
        ])
      }



      Sbuff.prototype.acceptLoc=function (col,line){

          let x = Math.floor(line);
          let y = Math.floor(col);
          if (x < 0 || x >= this.sbuff_lines || y < 0 || y >= this.sbuff_cols ) return false;
          return ((x*this.sbuff_cols) + y)
      }
      

      Sbuff.prototype.setGlyphId=function(col,line,glyphId,fontInfo,shading){
          let offset = this.acceptLoc(col,line)
          if(offset===false) return 
          shading = shading || this.fullBright

          this.posbuff[offset*3 +2] = glyphId

          this.shadingbuff.set(shading,offset*4)
          //this.shadingbuff.set([
          //    900.9,
          //    0.0,
          //    1.0,1.0],offset*4)
      }
      Sbuff.prototype.setChar=function(col,line,cha,fontInfo,shading){
          let offset = this.acceptLoc(col,line)
          if(offset===false) return 
          shading = shading || this.fullBright

          //this.buff.set(fontInfo.getCharUV(cha),offset*12)

          this.posbuff[offset*3 +2] = fontInfo.getCharGlyphId(cha);
          this.shadingbuff.set(shading,offset*4)


      }
      Sbuff.prototype.text=function(col,line,text){
          for(var i=0;i<text.length;i++){
              this.setChar(i+col,line,text[i],this.fontInfo)
          }
      }
      Sbuff.prototype.multiLine=function(col,line,lines,fontInfo,withBox){
        var maxLineLength = Math.max(...lines.map(function(x){return x.length})) // explode
        //console.log("maxLine",maxLineLength)
        var shiftCol = 0
        var shiftline = 0
        if(withBox){
           
          this.boxFill(col,line-lines.length-1,maxLineLength+2,lines.length+1,
              this.fontInfo.getCharGlyphId("-"),
              this.fontInfo.getCharGlyphId("|"),
              -1,//this.fontInfo.getCharGlyphId("A"),
              this.fontInfo.getCharGlyphId("/"),
              this.shadingColor(this.cGREEN),
              this.shadingColor(this.cRED),
              this.shadingColor(this.cGREEN),
              );

          shiftCol=1
          shiftline=-1
        } 
        for(var lineid=lines.length-1;lineid>=0;--lineid){
            rightFiller = ""
            for(var i=lines[lineid].length;i<=maxLineLength;i+=1){
              rightFiller+=" "
            }
            this.text(col+shiftCol,line-lineid+shiftline,lines[lineid]+rightFiller,this.fontInfo )

        }
      }

      Sbuff.prototype.boxFill=function(col,line,length,height,
          gh,gv,ginside,gcorner,
          shadingLines,shadingCorners,shadingInside){
        this.hLine(col+1,line,length-1,gh,shadingLines);
        this.hLine(col+1,line+height,length-1,gh,shadingLines);
        
        this.vLine(col,line+1,height-1,gv,shadingLines);
        this.vLine(col+length,line+1,height-1,gv,shadingLines);
        

        this.setGlyphId(col,line,gcorner,this.fontInfo,shadingCorners);
        this.setGlyphId(col+length,line,gcorner,this.fontInfo,shadingCorners);
        this.setGlyphId(col,line+height,gcorner,this.fontInfo,shadingCorners);
        this.setGlyphId(col+length,line+height,gcorner,this.fontInfo,shadingCorners);
        
        if(ginside>=0){
          var i = 0;
          for(i=1;i<height;i++){
            this.hLine(col+1,line+i,length-1,ginside,shadingInside)

          }

        }

      }
      Sbuff.prototype.hLine=function(col,line,length,glyphId,shading){
        //strait line
        var i =0
        for(i=0;i<length;i++){
          this.setGlyphId(col+i,line,glyphId,this.fontInfo,shading)
        }
      }
      Sbuff.prototype.vLine=function(col,line,length,glyphId,shading){
        //strait line
        var i =0
        for(i=0;i<length;i++){
          this.setGlyphId(col,line+i,glyphId,this.fontInfo,shading)
        }
      }


      Sbuff.prototype.drawSprite=function(col,line,height,sprite,distanceToPlayer,distanceByColBuff){
        //strait line
        var i =0
        var j =0
        for(i=0;i<height;i++){
          for(j=0;j<height;j++){
            if(this.acceptLoc(col+i,line+j) && 
                distanceByColBuff[col+i]>distanceToPlayer)
            {
              var glyphId = sprite.getAutoGlyphId(i/height,1-j/height)
              if(glyphId>=0){
                
                this.setGlyphId(col+i,line+j,glyphId,this.fontInfo,
                    this.shadingColor(sprite.getColor(i/height,1-j/height)))
              }
            }

          }
        }
      }


  

      function Controls() {
        this.codes  = { 37: 'left', 39: 'right', 38: 'forward', 40: 'backward' ,
          //esdf 
          83: 'sleft', 70: 'sright', 69: 'forward', 68: 'backward' ,
          16: "running",  // left shift
          80: "debug", 
          79: "increaseQuality", 
          73: "decreaseQuality", 
          27: "escape"
        
        };

        this.states = { 'left': false, 'right': false, 'forward': false, 'backward': false, 
        'mouseXBuff':0,
        'mouseYBuff':0,

        'lastMouseX':0,
        'lastMouseY':0,

        'running':false,

        'mouseAct' : false,
        'sright': false,
        'sleft' : false,
        };

        this.switchs = {
          'map':false,
          'debug':true,

          'increaseQuality':false,
          'decreaseQuality':false,

        };
        this.magics = [0,5]

        document.addEventListener('keydown', this.onKey.bind(this, true), false);
        document.addEventListener('keyup', this.onKey.bind(this, false), false);
        document.addEventListener('touchstart', this.onTouch.bind(this), false);
        document.addEventListener('touchmove', this.onTouch.bind(this), false);
        document.addEventListener('touchend', this.onTouchEnd.bind(this), false);
        
        this.mouseSensitivity = 0.1
        this.mouseSensitivityY = 0.001
        this.mouseAttached=false;

        this.gameLoop = false;
      }
      Controls.prototype.onTouch = function(e) {
        var t = e.touches[0];
        this.onTouchEnd(e);
        if (t.pageY < window.innerHeight * 0.5) this.onKey(true, { keyCode: 38 });
        else if (t.pageX < window.innerWidth * 0.5) this.onKey(true, { keyCode: 37 });
        else if (t.pageY > window.innerWidth * 0.5) this.onKey(true, { keyCode: 39 });
      };
      Controls.prototype.onTouchEnd = function(e) {
        this.states = { 'left': false, 
            'right': false, 'forward': false, 'backward': false ,

            'sright':false,
            'sleft' : false,


            'mouseXBuff':0,
            'mouseYBuff':0,

            'mouseAct' : false,
        
        
        
        };
        e.preventDefault();
        e.stopPropagation();
      };
      Controls.prototype.onKey = function(val, e) {
        if(e.repeat) return; // do not care repeatition

        //magic 
        if(val && e.keyCode==75){
          this.magics[0]-=1;
          console.log("control magics",this.magics)
          return
        }
        if(val &&e.keyCode==76){
          this.magics[0]+=1;
          console.log("control magics",this.magics)
          return
        }
        if(val &&e.keyCode==72){
          this.magics[1]-=1;
          console.log("control magics",this.magics)
          return
        }
        if(val &&e.keyCode==74){
          this.magics[1]+=1;
          console.log("control magics",this.magics)
          return
        }
        //
        //
        //
        var actCode = this.codes[e.keyCode];
        if (typeof actCode === 'undefined') {
          
          console.log("key"+ val?"down":"up",e.keyCode,e) 
          return;

        }        
        
        if(this.states[actCode]>=0){
          // key is statable
          this.states[actCode] = val;
        }else if (val && this.switchs[actCode]>=0){
          //switch
          this.switchs[actCode] = ! this.switchs[actCode];
        }


        e.preventDefault && e.preventDefault();
        e.stopPropagation && e.stopPropagation();
      };

      Controls.prototype.updateMousePosition=function (e) {
        if(!this.mouseAttached) return;
        
        //console.log(e);
        this.states.mouseXBuff+= e.movementX*this.mouseSensitivity;
        this.states.mouseYBuff+= e.movementY*this.mouseSensitivityY;

        // set this true here, when player .update run, it will swithc false
        this.states.mouseAct = true;


        //if(mouseX<0){mouseX = max_X+mouseX}
        //else if(mouseX>max_X){mouseX = mouseX-max_X}
        //
        //if(mouseY<0){mouseY = 0}
        //else if(mouseY>max_Y){mouseY = max_Y}
        //
        //
        //mouseLine = sbuff_lines-Math.floor(mouseY/fontInfo.letterHeight)
        //mouseCol = Math.floor(mouseX/fontInfo.letterWidth)
        //cols[mouseCol][mouseLine] = " ";
        e.preventDefault && e.preventDefault();
        e.stopPropagation && e.stopPropagation();
      };

      Controls.prototype.onMouseClick=function (val,e) {
        if(!this.mouseAttached) return;

          console.log("click",e)
        e.preventDefault && e.preventDefault();
        e.stopPropagation && e.stopPropagation();
      };






      function Bitmap(src, width, height) {
        this.image = new Image();
        this.image.src = src;
        this.width = width;
        this.height = height;
      }



      
      function Player(x, y, direction) {
        this.x = x;
        this.y = y;
        
        this.direction = direction;
        this.updateCosSin();
        

        this.viewAngle = 0;

        this.walkSpeed = 3;
        this.runSpeed = 5;

        this.paces = 0;

        this.CIRCLE = Math.PI * 2;

        this.isMoving = false;

      }
      Player.prototype.updateCosSin = function() {
          this.dirCos = Math.cos(this.direction)
          this.dirSin = Math.sin(this.direction)
      };
      Player.prototype.rotate = function(angle) {
        this.direction = (this.direction + angle + this.CIRCLE) % (this.CIRCLE);
        this.updateCosSin();
        this.isMoving = true;
      };
      Player.prototype.walk = function(distance, map) {
        var dx = this.dirCos * distance;
        var dy = this.dirSin * distance;
        
        var sensi=0.2 ;
        var moveX = true
        var moveY = true
        for(var i=-1;i<=1;i+=0.3){
            for(var j=-1;j<=1;j+=0.3){
                if (map.get(this.x + dx + i*sensi, this.y+ j*sensi ) > 0) moveX=false;
                if (map.get(this.x + i*sensi, this.y+dy + j*sensi ) > 0) moveY=false;
            }

        }
        if (moveX) this.x += dx;
        if (moveY) this.y += dy;
        this.paces += distance;
        this.isMoving = true;
      };
      Player.prototype.update = function(controls, map, seconds) {
        this.isMoving = false;
        if (controls.mouseAct){
            var rotateBy = controls.mouseXBuff * seconds 
            this.rotate(rotateBy);
            controls.mouseAct=false;
            controls.mouseXBuff=0;
            

            //up date viewagent
            this.viewAngle=Math.max(-1*controls.mouseYBuff, -2);
            //console.log(controls.mouseXBuff,controls.mouseYBuff)

        }
        if (controls.left) this.rotate(-Math.PI * seconds);
        if (controls.right) this.rotate(Math.PI * seconds);
        
        var stepspeed=controls.running ? this.runSpeed : this.walkSpeed;
        if (controls.forward) this.walk(stepspeed * seconds, map);
        if (controls.backward) this.walk(-1*stepspeed * seconds, map);
        if (controls.sleft) {
          this.rotate(-Math.PI/2 );
          this.walk(stepspeed * seconds, map);
          this.rotate(Math.PI/2 );
          
        }
        if (controls.sright) {
          this.rotate( Math.PI/2 );
          this.walk(stepspeed * seconds, map);
          this.rotate(-Math.PI/2 );
          
        }
      };




     function SpriteLayer(){
        
        this.sprites = [new WallTexture().init("tree")]

        this.entityBuff = []

     } 

     SpriteLayer.prototype.render = function(camera,sbuff,map,player){
       this.entityBuff = [] 
       var entityCount = map.entities.length
       var i =0 
       const CIRCLE = Math.PI*2
       const minAngle = -1
       const maxAngle = 1
       for(i=0;i < entityCount ; i++){
         var sprite = this.sprites[0];
         var entity = map.entities[i];
        
        
         var a2 = Math.atan2(entity.y-player.y,entity.x-player.x)
         var a1 = Math.atan2(player.dirSin,player.dirCos)
         //var a2 = Math.atan2(source.y, source.x);
         //var a1 = Math.atan2(compare.y, compare.x);
         var sign = a1 > a2 ? 1 : -1;
         var angle = a1 - a2;
         var K = -sign * Math.PI * 2;
         var angleToPlayer = (Math.abs(K + angle) < Math.abs(angle))? K + angle : angle;
        
         // if angle good
         if(angleToPlayer>minAngle && angleToPlayer<maxAngle){
           //
           var distanceToPlayer = Math.sqrt((entity.y-player.y)**2+(entity.x-player.x)**2)

           if (distanceToPlayer>camera.focalLength){
             // entity drawable
             var ppg = camera.project(1,angleToPlayer,distanceToPlayer)
             var col = Math.floor(((Math.tan(-angleToPlayer)*camera.focalLength)+0.5 ) * camera.width)

             entity.angleToPlayer = angleToPlayer
             entity.distanceToPlayer = distanceToPlayer
             entity.ppg = ppg
             entity.colCenter = col
             entity.sprite = sprite

             this.entityBuff.push(entity)

           }
         } 

       }
       this.entityBuff.sort(function(a,b){
          return a.distanceToPlayer<b.distanceToPlayer
       })
       for(i=0;i < this.entityBuff.length ; i++){
         var entity = this.entityBuff[i]

         sbuff.drawSprite(entity.colCenter-Math.floor(entity.ppg.height/2),
             entity.ppg.top,
             entity.ppg.height,
             entity.sprite,
             entity.distanceToPlayer,
             camera.distanceByColBuff);

         //sbuff.text(entity.colCenter,entity.ppg.top,  "angle    : "+entity.distanceToPlayer);
         //sbuff.text(entity.colCenter,entity.ppg.top+1,"wall     : "+camera.distanceByColBuff[entity.colCenter]);


       }

     }















      function Camera(canvas, qualityFactor,focalLength,fontInfo) {
        this.gl = canvas.getContext('webgl');
        if (!this.gl){
          console.error("Webgl not supported :( ")
          return;
        }
        this.gameLoop=false;
        

        this.utimes = 0.0
        this.focalLength = focalLength || 0.8;
        this.range = 20 //MOBILE ? 8 : 14;

        this.textProgramInfo = webglUtils.createProgramInfo(this.gl, [require("./src/pix.vs"), require("./src/pix.fs")]);
        this.finalTexturePI = webglUtils.createProgramInfo(this.gl, [require("./src/drawImg.vs"),require("./src/drawImg.fs"),]);

        // Create a texture.
        this.glyphTex = this.gl.createTexture();
        this.gl.bindTexture(this.gl.TEXTURE_2D, this.glyphTex);
        // Fill the texture with a 1x1 blue pixel.
        this.gl.texImage2D(this.gl.TEXTURE_2D, 0, this.gl.RGBA, 1, 1, 0, this.gl.RGBA, this.gl.UNSIGNED_BYTE,
          new Uint8Array([0, 0, 255, 255]));
        
        // Asynchronously load an image
        this.fontInfo=new FontInfo(require("./assets/f.json"))
        this.fontInfo.preLoad(1,1,1,1);
        
        var image = new Image();
    
        var gl = this.gl;
        var fontInfo = this.fontInfo
        var glyphTex = this.glyphTex
        var self = this;
        image.addEventListener('load', function() {
          // Now that the image has loaded make copy it to the texture.
          gl.bindTexture(gl.TEXTURE_2D, glyphTex);
          //gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true);
          gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    
           //console.log("texture Loaded",image.width,image.height)
           fontInfo.preLoad(image.width,image.height,
                   
                   fontInfo.inLetterWidth,fontInfo.inLetterHeight);

            self.updateQuality(qualityFactor);
         });
    
        image.src = require("./assets/f.png");
        

        this.w1 = new WallTexture().init("tex3")
        this.g1 = new WallTexture().init("grd2")

        this.layers=[new SpriteLayer()]

        this.debugLines=[]
        for(var i=0;i<100;i++){
          this.debugLines.push("")
        }

        this.updateQuality(qualityFactor);


      }
  
      Camera.prototype.updateQuality = function(qualityFactor) {
        this.qualityFactor = qualityFactor;

        this.width = this.qualityFactor*6//canvas.width = window.innerWidth * 0.5;
        this.height = this.qualityFactor*3; // canvas.height = window.innerHeight * 0.5;;//window.innerHeight * 0.5;


        this.sbuff_cols = this.width ; 
        this.sbuff_lines =this.height;//60; 

        
        this.sbuff2 = new Sbuff().init(this.height,this.width,this.fontInfo);
        var positionComponents = 3
        this.sbuff2.posbuff=makePosition(this.fontInfo,this.sbuff_cols,this.sbuff_lines,positionComponents)
        
        this.raysBuff=[];

        for(var i=0;i<this.width;i++){
          this.raysBuff.push(gamemap.makeCastBuff(this.range))
        }
        this.raysLenBuff=new Uint32Array(this.width);

        this.textInfo = {

            textBufferInfo : {
                attribs: {
                  a_position: { buffer: this.gl.createBuffer(), 
                      numComponents: positionComponents, },
                  a_shading: { buffer: this.gl.createBuffer(), 
                      numComponents: 4, },
                },
                numElements: 0,
                },

            numVertices:this.height*this.width
        }
        


        this.textUniforms = {
            u_matrix: m4.identity(),
            u_texture: this.glyphTex,
            u_color: [0, 0, 0, 1],  // black,
            u_globallight: [1, 1, 1, 1],  // black,
            u_times:this.utimes,
            u_glyphByCol: this.fontInfo.glyphByCol,
            u_glyphByRow: this.fontInfo.glyphByRow,
            
            u_inLetterWidth: this.fontInfo.inLetterWidth,
            u_inLetterHeight: this.fontInfo.inLetterHeight,

            u_pixelSize:24.0,
        };
        this.forceDrawCols = 1




    // Create a buffer.
        this.targetInfo = {

                attribs: {
                  a_position: { buffer: this.gl.createBuffer(), 
                      numComponents: 2, },
                  a_texcoord: { buffer: this.gl.createBuffer(), 
                      numComponents: 2, },
                },
                numElements: 0,
        }
    this.targetTexturePositionBuff = this.gl.createBuffer();
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.targetTexturePositionBuff);
    this.targetTexturePosition = new Float32Array([0,0,0,1,1,0,1,0, 0,1,1,1])
    this.targetTextureFillTo = new Float32Array([0,0,0,1,1,0,1,0, 0,1,1,1])
    this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.targetTexturePosition), this.gl.STATIC_DRAW);


    // create to render to
    this.targetTextureWidth =  this.width *8*2;
    this.targetTextureHeight = this.height*8*2;

    this.targetTexture = this.gl.createTexture();
    this.gl.bindTexture(this.gl.TEXTURE_2D, this.targetTexture);
     
    {
      // define size and format of level 0
      const level = 0;
      const internalFormat = this.gl.RGBA;
      const border = 0;
      const format = this.gl.RGBA;
      const type = this.gl.UNSIGNED_BYTE;
      const data = null; //new Float32Array(this.targetTextureWidth*this.targetTextureHeight*4);
      this.gl.texImage2D(this.gl.TEXTURE_2D, level, internalFormat,
                    this.targetTextureWidth, this.targetTextureHeight, border,
                    format, type, data);
     
      // set the filtering so we don't need mips
      this.gl.texParameteri(this.gl.TEXTURE_2D, this.gl.TEXTURE_MIN_FILTER, this.gl.LINEAR);
      this.gl.texParameteri(this.gl.TEXTURE_2D, this.gl.TEXTURE_WRAP_S, this.gl.CLAMP_TO_EDGE);
      this.gl.texParameteri(this.gl.TEXTURE_2D, this.gl.TEXTURE_WRAP_T, this.gl.CLAMP_TO_EDGE);
    }
        this.targetUniforms = {
            u_matrix: m4.identity(),
            u_texture: this.targetTexture,
        }
    // Create and bind the framebuffer
    this.fb = this.gl.createFramebuffer();
    this.gl.bindFramebuffer(this.gl.FRAMEBUFFER, this.fb);
    // 
    //// attach the texture as the first color attachment
    const attachmentPoint = this.gl.COLOR_ATTACHMENT0;
    this.gl.framebufferTexture2D(this.gl.FRAMEBUFFER, attachmentPoint, this.gl.TEXTURE_2D, 
			this.targetTexture, 0);

        this.distanceByColBuff = [];
        for(var i=0; i<this.width;i++){
          this.distanceByColBuff.push(this.range)
        }
        
      }



      Camera.prototype.render = function(player, map,controls,seconds) {
        this.utimes+=seconds 
        var gl = this.gl; 
        if(controls.switchs.increaseQuality){
          if(this.qualityFactor<80){

            this.updateQuality(this.qualityFactor+1)
          }
          controls.switchs.increaseQuality=false;
        }else if(controls.switchs.decreaseQuality){
          if(this.qualityFactor>1){

            this.updateQuality(this.qualityFactor-1)
          }
          controls.switchs.decreaseQuality=false;
        }
        


        this.viewAngle=player.viewAngle

        if(controls.magics){

          //player.viewAngle=controls.magics[0]
          //this.textUniforms.u_shadersize = controls.magics
        }
        
        
        // all clear
        
        this.drawColumns(player, map,this.forceDrawCols>0);
        this.forceDrawCols=-1

        for(var i=0;i<this.layers.length;i++){
          this.layers[i].render(this,this.sbuff2,map,player)
        }

        if(controls.switchs.debug){

          this.drawDebug(player,controls);
        }
        //this.drawMap
        //this.draw..
        // sbuff is now filled with data
        //
        //
        //for(var i=0;i<this.width;i++){
        //  for(var j=0;j<this.height;j++){
        //    //this.sbuff2.setGlyphId(i,j,0,this.fontInfo);
        //  }
        //}
        var textBufferInfo = this.textBufferInfo; 
        var textProgramInfo = this.textProgramInfo;
        var sbuff_cols = this.sbuff_cols; 
        var sbuff_lines = this.sbuff_lines; 
        var textUniforms = this.textUniforms;
        var fontInfo = this.fontInfo;
        //console.log(s)
        
        webglUtils.resizeCanvasToDisplaySize(this.gl.canvas);
        // Tell WebGL how to convert from clip space to pixels
        //this.gl.viewport(0, 0, this.gl.canvas.width, this.gl.canvas.height);
        //
        
        //gl.bindTexture(gl.TEXTURE_2D, this.targetTexture);
        //this.gl.bindFramebuffer(gl.FRAMEBUFFER, null);
        //var pixSizeX = (this.gl.canvas.clientWidth/this.width);
        //var pixSizeY = (this.gl.canvas.clientHeight/this.height);
        
				this.gl.bindFramebuffer(gl.FRAMEBUFFER, this.fb);
        var pixSizeX = (this.targetTextureWidth/this.width);
        var pixSizeY = (this.targetTextureHeight/this.height);
        
        //  calculate pixel size
        var pixelSize=Math.max(pixSizeY,pixSizeX);
        this.textUniforms.u_pixelSize=pixelSize;
        
        //update universal time 
        this.textUniforms.u_times=this.utimes;
        
          
        gl.bindTexture(gl.TEXTURE_2D, this.glyphTex);
        this.gl.viewport(0, 0, this.width*pixelSize, this.height*pixelSize);
        

        // Set clear color to black, fully opaque
        this.gl.clearColor(0.0, 0.0, 0.0, 1.0);
        this.gl.enable(this.gl.BLEND);
         
        this.gl.useProgram(this.textProgramInfo.program);
	      webglUtils.setBuffersAndAttributes(gl, textProgramInfo, 
            this.textInfo.textBufferInfo);
              


	      
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.textInfo.textBufferInfo.attribs.a_position.buffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, this.sbuff2.posbuff, this.gl.STREAM_DRAW);
        

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.textInfo.textBufferInfo.attribs.a_shading.buffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, this.sbuff2.shadingbuff, this.gl.STREAM_DRAW);


	      webglUtils.setUniforms(textProgramInfo, textUniforms);
	      // Draw the text.
	      gl.drawArrays(gl.POINTS, 0, this.textInfo.numVertices);







	      //
        //
        this.gl.bindFramebuffer(gl.FRAMEBUFFER, null);
        this.gl.bindTexture(this.gl.TEXTURE_2D, this.targetTexture);

        this.gl.viewport(0, 0, this.gl.canvas.width, this.gl.canvas.height);
        this.gl.clearColor(1.0, 1.0, 1.0, 1.0);
        
        this.gl.useProgram(this.finalTexturePI.program);
        
	      webglUtils.setBuffersAndAttributes(gl, this.finalTexturePI, 
            this.targetInfo);

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.targetInfo.attribs.a_position.buffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, this.targetTexturePosition, this.gl.STREAM_DRAW);
        

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.targetInfo.attribs.a_texcoord.buffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, this.targetTexturePosition, this.gl.STREAM_DRAW);
			  
			  //var projectionMatrix = m4.orthographic(0,0,this.gl.canvas.width, this.gl.canvas.height, -100,200);
			  
			  // this matrix will scale our 1 unit quad
        //
        var magicratiox=this.gl.canvas.height/this.gl.canvas.width
			  var scaleMatrix = m4.scaling(2*Math.min(magicratiox*1.6,1), 2/Math.max(magicratiox*1.6,1), 1);
			  
			  var translationMatrix = m4.translation(-1,-1, 0);
			  
			  // multiply them all togehter
			  var matrix = m4.multiply(translationMatrix, scaleMatrix);
			  this.targetUniforms.u_matrix = matrix;
	      webglUtils.setUniforms(this.finalTexturePI, this.targetUniforms);
			  // Tell the shader to get the texture from texture unit 0
	      
        gl.drawArrays(gl.TRIANGLES, 0, 6);
		  
      };
     




      Camera.prototype.drawDebug = function(player,controls) {

          var toPrint = []
          if(this.gameLoop){
              s = Math.floor(this.gameLoop.fps).toString();
              toPrint.push("q:"+this.qualityFactor+" "+this.width+" * "+this.height + " @"+s+ " fps" )
              toPrint.push("  ")
              toPrint.push("----player---") 
              toPrint.push(" va :"+player.viewAngle) 
              toPrint.push(" run :"+controls.states.running) 
              toPrint.push(" m xy :"+
                      controls.states.lastMouseX+
                  " "+controls.states.lastMouseY) 
              
              toPrint.push("----tiles---") 
              toPrint.push("abcdefgh") 
              toPrint.push("ijklmnop") 
              toPrint.push("qrstuvwx") 
              toPrint.push("yz012345") 
              toPrint.push("6789-*!©") 
              toPrint.push("AB@|EF?:") 
              toPrint.push("/\\#\"'=[]") 
              toPrint.push("().;") 
              toPrint.push("-------------") 
          }

          this.debugLines.forEach(function(l){
              if(l.length>0){
                toPrint.push(l)
              }
          });


          this.sbuff2.multiLine(3,this.height-2,toPrint,this.fontInfo,true)

          //this.sbuff2.boxFill(2,1,10,6,
          //    this.fontInfo.getCharGlyphId("-"),
          //    this.fontInfo.getCharGlyphId("|"),
          //    -1,//this.fontInfo.getCharGlyphId("A"),
          //    this.fontInfo.getCharGlyphId("#"),
          //    this.sbuff2.shadingColor(this.sbuff2.cRED),
          //    this.sbuff2.shadingColor(this.sbuff2.cBLUE),
          //    this.sbuff2.shadingColor(this.sbuff2.cGREEN),
          //    
          //    
          //    
          //    );

          for(var i=0;i<this.debugLines.length;i++){
            this.debugLines[i]=""
          }
      }


      Camera.prototype.drawColumns = function(player, map,force) {
        force=force||false

        
        for (var column = 0; column < this.width; column++) {
          var x = column / this.width - 0.5;
          var angle = Math.atan2(x, this.focalLength);

          //rayBuff = gamemap.makeCastBuff(20);
          //
          var firststep = this.raysBuff[column][0];

          if(player.isMoving || force ){
            firststep.x = player.x
            firststep.y = player.y
            this.raysLenBuff[column] = gamemap.cast2(this.raysBuff[column],map,0,player.direction + angle,this.range);
            //var ray = map.cast(player, player.direction + angle, this.range);

          }
          var hitDist = this.drawColumn(column, this.raysBuff[column], angle, map, this.raysLenBuff[column]);
          this.distanceByColBuff[column] = hitDist
        }

        //this.sbuff2.text(10,10," "+this.distanceByColBuff );

      };

      
      Camera.prototype.drawColumn = function(column, ray, angle, map,raylength) {
        var self = this;
        var groundHorizon = this.height/(2)
        function drawGround(groundHorizon,hit ){
          //groundHorizon : maximum height from 0
          //hit : first wallHit
          var ss=1
          var itcol=0
          
          //buffer allocations
                   var glyphid=0
                   var x0=0
                   var y0=0
                   var x1=0
                   var y1=0
                   var t0=0
                   var t1=0
                   var x0Fl = 0
                   var y0Fl = 0
                       var tfactor=0
                       var onTexX= 0
                       var onTexY= 0
                       var shading=0
          //end buffer allocations

          

          var ray1 = ray[1]
          var ray0 = ray[0]
          
          var ppg0 = self.project(ray0.height,angle,0.1) // bellow distance
          var ppg1 = false;
          
          var limitLastitcol = self.height
          while(true && ss<raylength && itcol<limitLastitcol){
             ray1 = ray[ss]
             ppg1 = self.project(ray1.height,angle,ray1.distance)
             
             if(ppg0.height==0){
               //its ground
               if (ppg1.top>itcol ){
                   x0=ray0.x
                   y0=ray0.y
                   x1=ray1.x
                   y1=ray1.y
                   t0=ppg0.top
                   t1=ppg1.top
                   x0Fl = Math.floor(x0)  
                   y0Fl = Math.floor(y0) 

                   while(itcol<=Math.min(ppg1.top,groundHorizon)){
                       // draw some lines
                       // texture info are at Math.floo(x0 y0)
                       tfactor= (itcol-t0)/(t1-t0)
                       onTexX=(x0+((x1-x0)*tfactor)-x0Fl)
                       onTexY=(y0+((y1-y0)*tfactor)-y0Fl)
                       

                       // associate texture on ground to sbuff2
                       // var glyphId = self.g1.getAutoGlyphId(
                       //     onTexX>=0 ? onTexX : onTexX+1,
                       //     onTexY>=0 ? onTexY :  onTexY+1   )

                       // self.sbuff2.setGlyphId(column,itcol,glyphId,self.fontInfo,shading)
                       
                       
                       
                       
                       
                       var glyphId = self.g1.getAutoGlyphId(
                                 onTexX>=0 ? onTexX : onTexX+1,
                                 onTexY>=0 ? onTexY :  onTexY+1   )
                       var color = self.g1.getColor( 
                                 onTexX>=0 ? onTexX : onTexX+1,
                                 onTexY>=0 ? onTexY :  onTexY+1   )

                        
                       //console.log(color)
                       var shading = self.sbuff2.computeShading(
                           color,color,9,
                           0)

                       self.sbuff2.setGlyphId(column,
                           itcol,
                           glyphId,
                           self.fontInfo,shading)

                       itcol++;
                   }

                }
              }else{
                 //its a wall
                 
                 while(itcol <= ppg0.bottom && itcol<limitLastitcol && ppg0.height>0){
                   var color = self.w1.getColor( 
                      ray0.offset,
                      (ppg0.bottom-itcol)/ppg0.height)


                   var shading = self.sbuff2.computeShading(
                    color,
                    color,
                    1,
                    0)
                   var glyphId = self.w1.getAutoGlyphId(
                      ray0.offset,
                      (ppg0.bottom-itcol)/ppg0.height)

                   self.sbuff2.setGlyphId(column,itcol,glyphId,self.fontInfo,shading)
                   itcol++;
                 }


              }
              ppg0 = ppg1;
              ray0 = ray1;
              ss+=1
            }
            return itcol 
          

        }


        //var left = Math.floor(column * this.spacing);
        //var width = Math.ceil(this.spacing);
        var hit = -1;
        var itcol = 0;
        var glyphId = 0;
        while (++hit < raylength && ray[hit].height <= 0);

        function drawSkyChar(column,startAt,chr){
          for(itcol = startAt;itcol<self.height;itcol++){
             
              shading = self.sbuff2.computeShading(
                self.sbuff2.cBLUE,
                self.sbuff2.cWHITE,
                9,
                itcol/self.height+column/self.width

              ) 

             self.sbuff2.setChar(column,itcol,"A",self.fontInfo,shading)
          }
        }
        

        if(hit==raylength){
          //no collisions
          var startSkyAt =drawGround(this.height,0)   ; 
          drawSkyChar(column,startSkyAt," ");
          return this.range
        }else{
            var skyStartAt = 10;
            // iter throud the ray
            skyStartAt = drawGround(this.height,raylength) 
            
            // finaly draw the sky
            drawSkyChar(column,skyStartAt," ");
            return ray[hit].distance
        }
        // end ray containing collions
        //

      };
      Camera.prototype.project = function(height, angle, distance) {
        var z = distance * Math.cos(angle) // /Math.sqrt(1+distance);
        
        var wallHeight = Math.floor( (this.height * height) / z );
        var bottom = Math.floor( this.viewAngle*this.height +( (this.height /2) * (1 + 1 / z)  ) );

        return {
          top: this.height-bottom ,
          height: wallHeight,
          bottom: this.height-bottom + wallHeight
        }; 

      };
      

function WallTexture(){

    this.buff=[]
    this.colors=[]
}
WallTexture.prototype.init = function(texName) {
    var dicInfo = require('./assets/'+texName+'.json')

    if (dicInfo.minSize){
      // new format detected
      //console.log("newformat")
      //
      for(var size=0;size<dicInfo.maxSize;size++){

        if(size<dicInfo.minSize){
          // cant work on this now
          //
          this.buff.push([])
          this.colors.push([])
        
        }else{
          var glyphList=[]
          var colorList=[]

          for(var x=0;x<size;x++){
            for(var y=0;y<size;y++){
              var found = dicInfo.wad.find(function(element){ return element[0] == x && element[1] == y && element[2] == size});
              if(found){
                
                var color = [found[3][0]/255.0,found[3][1]/255.0,found[3][2]/255.0]
                //console.log("color",color);
                colorList.push(color)
                glyphList.push(found[4])
              }else{
                console.log("glyph not found loading texture");
              }
            }
          }


          // 
          this.buff.push(glyphList)
          this.colors.push(colorList)
        }
      }
      
      
    }else{
      for(var i=0;i<dicInfo.length;i++){
          this.buff.push(new Uint32Array(dicInfo[i]) )

      }
    }
    return this
}

WallTexture.prototype.getGlyphId = function(colCount,offset,line) {
    //colCount = int, size of the texture to find
    //offset = float, column in the texture btw 0 and 1
    //line = int, line in the texture
    
    if(colCount<this.buff.length){

      var textureOffset = Math.floor(offset*colCount)
      //textureOffset = int, column in the texture
      //
      var glyphId = this.buff[colCount][textureOffset*(colCount)+line]
      return glyphId
    }else{
      /* take the biggest texture

         scale offset 
         scale line 
         */
      var bigest = this.buff.length-1

      //var offsetSC = Math.floor((bigest*textureOffset)/colCount)
      var lineSC = Math.floor((bigest*line)/colCount)
      return this.getGlyphId(bigest,offset,lineSC)

      
    }
}


WallTexture.prototype.getAutoGlyphId = function(column,line) {
    //column = float between 0 and 1
    //line = float between 0 and 1
    var bigest = this.buff.length-1
    return this.getGlyphId(bigest,column,Math.floor(line*bigest))
}


WallTexture.prototype.getColor = function(column,line) {
    //column = float between 0 and 1
    //line = float between 0 and 1
    var bigest = this.buff.length-1
    var lineSC = Math.min(Math.floor(line*bigest),bigest-1)
    var textureOffset = Math.min(Math.floor(column*bigest),bigest-1)
    
    return this.colors[bigest][textureOffset*(bigest)+lineSC]


}





      function GameLoop() {
        this.frame = this.frame.bind(this);
        this.lastTime = 0;
        this.callback = function() {};

        this.frameCount=0;
        this.oneSecCount = 0;
        this.fps = 30; // 30 fps at start
      }
      GameLoop.prototype.start = function(callback) {
        this.callback = callback;
        requestAnimationFrame(this.frame);
      };
      GameLoop.prototype.frame = function(time) {
        var seconds = (time - this.lastTime) / 1000;
        this.lastTime = time;
           
        this.oneSecCount+=seconds
        this.frameCount+=1;
        if(this.oneSecCount>1){
            this.fps = 0.25*this.fps + 0.75*this.frameCount 
            console.log("fps",this.fps,seconds);
            this.oneSecCount=0;
            this.frameCount=0;
        }
        if (seconds < 0.2) this.callback(seconds);
        requestAnimationFrame(this.frame);
      };











      function main(){

      var MOBILE = /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent)




      var display = document.getElementById('display');

      var controls = new Controls();
      
	  display.onclick = function() {
        if(!controls.mouseAttached){

		  display.requestPointerLock();
        }
	  };
      function lockChangeAlert() {
        if (document.pointerLockElement === display ||
      	  document.mozPointerLockElement === display) {
            if(!controls.mouseAttached){

                console.log('The pointer lock status is now locked');
                document.addEventListener("mousemove", controls.updateMousePosition.bind(controls), false);
                document.addEventListener("mousedown", controls.onMouseClick.bind(controls,true), false);
                document.addEventListener("mouseup", controls.onMouseClick.bind(controls,false), false);
                controls.mouseAttached=true;
            }
        } else {
      	console.log('The pointer lock status is now unlocked');  
      	    document.removeEventListener("mousemove", controls.updateMousePosition.bind(controls), false);
            document.removeEventListener("mousedown", controls.onMouseClick.bind(controls,true), false);
            document.removeEventListener("mouseup", controls.onMouseClick.bind(controls,false), false);
                controls.mouseAttached=false;
                document.exitPointerLock()
        }
      }  
      display.requestPointerLock = display.requestPointerLock ||
                            display.mozRequestPointerLock;

      document.exitPointerLock = document.exitPointerLock ||
                           document.mozExitPointerLock;
      // Hook pointer lock state change events for different browsers
      document.addEventListener('pointerlockchange', lockChangeAlert, false);
      document.addEventListener('mozpointerlockchange', lockChangeAlert, false);



      var player = new Player(1.5, 1.5, Math.PI * 0.3);
      //var map = new Map(25);
      var map=new gamemap.Map(25);

      var camera = new Camera(display, 13, 0.8);
      var loop = new GameLoop();
      map.randomize();
      camera.gameLoop=loop;
      controls.gameLoop=loop;
      
      loop.start(function frame(seconds) {
        map.update(seconds);
        player.update(controls.states, map, seconds);
        camera.render(player, map,controls,seconds);
      });
      

      }



main();
