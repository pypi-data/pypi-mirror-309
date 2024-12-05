"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[1458],{281458:(t,i,e)=>{e.d(i,{Z:()=>k});var r=e(215671),n=e(143144),o=e(182963),a=e(661120),h=e(360136),s=e(497326),u=e(529439),l=e(607778);function c(t,i){var e=l.fF([],i,t);return l.bA(e,e,1/e[3]),e}var p=e(885975),v=e(631437),d=e(277160);function g(t,i){if(!t)throw new Error(i||"viewport-mercator-project: assertion failed.")}var M=Math.PI,f=M/4,b=M/180,j=180/M,x=4003e4;function m(t){return Math.pow(2,t)}function Z(t,i){var e=(0,u.Z)(t,2),r=e[0],n=e[1];g(Number.isFinite(r)&&Number.isFinite(i)),g(Number.isFinite(n)&&n>=-90&&n<=90,"invalid latitude");var o=n*b;return[(i*=512)*(r*b+M)/(2*M),i*(M-Math.log(Math.tan(f+.5*o)))/(2*M)]}function w(t,i){var e=(0,u.Z)(t,2),r=e[0],n=e[1],o=r/(i*=512)*(2*M)-M,a=2*(Math.atan(Math.exp(M-n/i*(2*M)))-f);return[o*j,a*j]}function P(t,i){var e=arguments.length>2&&void 0!==arguments[2]?arguments[2]:0,r=(0,u.Z)(t,3),n=r[0],o=r[1],a=r[2];if(g(Number.isFinite(n)&&Number.isFinite(o),"invalid pixel coordinate"),Number.isFinite(a))return c(i,[n,o,a,1]);var h=c(i,[n,o,0,1]),s=c(i,[n,o,1,1]),l=h[2],p=s[2],d=l===p?0:((e||0)-l)/(p-l);return v.t7([],h,s,d)}var F=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1];function N(t){var i=t.width,e=t.height,r=t.bounds,n=t.minExtent,o=void 0===n?0:n,a=t.maxZoom,h=void 0===a?24:a,s=t.padding,l=void 0===s?0:s,c=t.offset,p=void 0===c?[0,0]:c,v=(0,u.Z)(r,2),d=(0,u.Z)(v[0],2),M=d[0],f=d[1],b=(0,u.Z)(v[1],2),j=b[0],x=b[1];Number.isFinite(l)?l={top:l,bottom:l,left:l,right:l}:g(Number.isFinite(l.top)&&Number.isFinite(l.bottom)&&Number.isFinite(l.left)&&Number.isFinite(l.right));var m=new k({width:i,height:e,longitude:0,latitude:0,zoom:0}),Z=m.project([M,x]),w=m.project([j,f]),P=[Math.max(Math.abs(w[0]-Z[0]),o),Math.max(Math.abs(w[1]-Z[1]),o)],F=[i-l.left-l.right-2*Math.abs(p[0]),e-l.top-l.bottom-2*Math.abs(p[1])];g(F[0]>0&&F[1]>0);var N=F[0]/P[0],y=F[1]/P[1],L=(l.right-l.left)/2/N,z=(l.bottom-l.top)/2/y,I=[(w[0]+Z[0])/2+L,(w[1]+Z[1])/2+z],A=m.unproject(I),C=m.zoom+Math.log2(Math.abs(Math.min(N,y)));return{longitude:A[0],latitude:A[1],zoom:Math.min(C,h)}}var k=function(t){function i(){var t,e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},n=e.width,h=e.height,u=e.latitude,l=void 0===u?0:u,c=e.longitude,v=void 0===c?0:c,M=e.zoom,f=void 0===M?0:M,j=e.pitch,w=void 0===j?0:j,P=e.bearing,F=void 0===P?0:P,N=e.altitude,k=void 0===N?1.5:N,y=e.nearZMultiplier,L=e.farZMultiplier;(0,r.Z)(this,i),n=n||1,h=h||1;var z=m(f);k=Math.max(.75,k);var I=Z([v,l],z);I[2]=0;var A=function(t){var i=t.width,e=t.height,r=t.pitch,n=function(t){var i=t.width,e=t.height,r=t.altitude,n=void 0===r?1.5:r,o=t.pitch,a=t.nearZMultiplier,h=void 0===a?1:a,s=t.farZMultiplier,u=void 0===s?1:s,l=(void 0===o?0:o)*b,c=Math.atan(.5/n),p=Math.sin(c)*n/Math.sin(Math.PI/2-l-c),v=Math.cos(Math.PI/2-l)*p+n;return{fov:2*Math.atan(e/2/n),aspect:i/e,focalDistance:n,near:h,far:v*u}}({width:i,height:e,altitude:t.altitude,pitch:r,nearZMultiplier:t.nearZMultiplier,farZMultiplier:t.farZMultiplier}),o=n.fov,a=n.aspect,h=n.near,s=n.far;return p.G3([],o,a,h,s)}({width:n,height:h,pitch:w,bearing:F,altitude:k,nearZMultiplier:y||1/h,farZMultiplier:L||1.01}),C=function(t){var i=t.height,e=t.pitch,r=t.bearing,n=t.altitude,o=t.center,a=void 0===o?null:o,h=t.flipY,s=void 0!==h&&h,u=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1];return p.Iu(u,u,[0,0,-n]),p.bA(u,u,[1,1,1/i]),p.lM(u,u,-e*b),p.jI(u,u,r*b),s&&p.bA(u,u,[1,-1,1]),a&&p.Iu(u,u,d.tk([],a)),u}({height:h,center:I,pitch:w,bearing:F,altitude:k,flipY:!0});return(t=(0,o.Z)(this,(0,a.Z)(i).call(this,{width:n,height:h,viewMatrix:C,projectionMatrix:A}))).latitude=l,t.longitude=v,t.zoom=f,t.pitch=w,t.bearing=F,t.altitude=k,t.scale=z,t.center=I,t.pixelsPerMeter=function(t){var i=t.latitude,e=t.longitude,r=t.zoom,n=t.scale,o=t.highPrecision,a=void 0!==o&&o;n=void 0!==n?n:m(r),g(Number.isFinite(i)&&Number.isFinite(e)&&Number.isFinite(n));var h={},s=512*n,u=Math.cos(i*b),l=s/360,c=l/u,p=s/x/u;if(h.pixelsPerMeter=[p,-p,p],h.metersPerPixel=[1/p,-1/p,1/p],h.pixelsPerDegree=[l,-c,p],h.degreesPerPixel=[1/l,-1/c,1/p],a){var v=b*Math.tan(i*b)/u,d=l*v/2,M=s/x*v,f=M/c*p;h.pixelsPerDegree2=[0,-d,M],h.pixelsPerMeter2=[f,0,f]}return h}((0,s.Z)((0,s.Z)(t))).pixelsPerMeter[2],Object.freeze((0,s.Z)((0,s.Z)(t))),t}return(0,h.Z)(i,t),(0,n.Z)(i,[{key:"projectFlat",value:function(t){return Z(t,arguments.length>1&&void 0!==arguments[1]?arguments[1]:this.scale)}},{key:"unprojectFlat",value:function(t){return w(t,arguments.length>1&&void 0!==arguments[1]?arguments[1]:this.scale)}},{key:"getMapCenterByLngLatPosition",value:function(t){var i=t.lngLat,e=P(t.pos,this.pixelUnprojectionMatrix),r=Z(i,this.scale),n=v.IH([],r,v.tk([],e));return w(v.IH([],this.center,n),this.scale)}},{key:"getLocationAtPoint",value:function(t){var i=t.lngLat,e=t.pos;return this.getMapCenterByLngLatPosition({lngLat:i,pos:e})}},{key:"fitBounds",value:function(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},r=this.width,n=this.height,o=N(Object.assign({width:r,height:n,bounds:t},e));return new i({width:r,height:n,longitude:o.longitude,latitude:o.latitude,zoom:o.zoom})}}]),i}(function(){function t(){var i=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},e=i.width,n=i.height,o=i.viewMatrix,a=void 0===o?F:o,h=i.projectionMatrix,s=void 0===h?F:h;(0,r.Z)(this,t),this.width=e||1,this.height=n||1,this.scale=1,this.pixelsPerMeter=1,this.viewMatrix=a,this.projectionMatrix=s;var u=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1];p.Jp(u,u,this.projectionMatrix),p.Jp(u,u,this.viewMatrix),this.viewProjectionMatrix=u;var l=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1];p.bA(l,l,[this.width/2,-this.height/2,1]),p.Iu(l,l,[1,-1,0]),p.Jp(l,l,this.viewProjectionMatrix);var c=p.U_([1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],l);if(!c)throw new Error("Pixel project matrix not invertible");this.pixelProjectionMatrix=l,this.pixelUnprojectionMatrix=c,this.equals=this.equals.bind(this),this.project=this.project.bind(this),this.unproject=this.unproject.bind(this),this.projectPosition=this.projectPosition.bind(this),this.unprojectPosition=this.unprojectPosition.bind(this),this.projectFlat=this.projectFlat.bind(this),this.unprojectFlat=this.unprojectFlat.bind(this)}return(0,n.Z)(t,[{key:"equals",value:function(i){return i instanceof t&&i.width===this.width&&i.height===this.height&&p.fS(i.projectionMatrix,this.projectionMatrix)&&p.fS(i.viewMatrix,this.viewMatrix)}},{key:"project",value:function(t){var i=(arguments.length>1&&void 0!==arguments[1]?arguments[1]:{}).topLeft,e=void 0===i||i,r=function(t,i){var e=(0,u.Z)(t,3),r=e[0],n=e[1],o=e[2],a=void 0===o?0:o;return g(Number.isFinite(r)&&Number.isFinite(n)&&Number.isFinite(a)),c(i,[r,n,a,1])}(this.projectPosition(t),this.pixelProjectionMatrix),n=(0,u.Z)(r,2),o=n[0],a=n[1],h=e?a:this.height-a;return 2===t.length?[o,h]:[o,h,r[2]]}},{key:"unproject",value:function(t){var i=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},e=i.topLeft,r=void 0===e||e,n=i.targetZ,o=(0,u.Z)(t,3),a=o[0],h=o[1],s=o[2],l=r?h:this.height-h,c=n&&n*this.pixelsPerMeter,p=P([a,l,s],this.pixelUnprojectionMatrix,c),v=this.unprojectPosition(p),d=(0,u.Z)(v,3),g=d[0],M=d[1],f=d[2];return Number.isFinite(s)?[g,M,f]:Number.isFinite(n)?[g,M,n]:[g,M]}},{key:"projectPosition",value:function(t){var i=this.projectFlat(t),e=(0,u.Z)(i,2);return[e[0],e[1],(t[2]||0)*this.pixelsPerMeter]}},{key:"unprojectPosition",value:function(t){var i=this.unprojectFlat(t),e=(0,u.Z)(i,2);return[e[0],e[1],(t[2]||0)/this.pixelsPerMeter]}},{key:"projectFlat",value:function(t){return arguments.length>1&&void 0!==arguments[1]||this.scale,t}},{key:"unprojectFlat",value:function(t){return arguments.length>1&&void 0!==arguments[1]||this.scale,t}}]),t}())}}]);
//# sourceMappingURL=5492b81e50ea2d4f03aa.chunk.js.map