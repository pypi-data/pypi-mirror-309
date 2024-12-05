"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[2219],{492219:(t,e,o)=>{o.d(e,{Z:()=>ft});var s=o(204942),i=o(905259),n=o(537832),r=o(113717),a=o(733321),c=o(339769),g=o(453982);const l={getSourcePosition:{type:"accessor",value:t=>t.sourcePosition},getTargetPosition:{type:"accessor",value:t=>t.targetPosition},getColor:{type:"accessor",value:[0,0,0,255]},getWidth:{type:"accessor",value:1},widthUnits:"pixels",widthScale:{type:"number",value:1,min:0},widthMinPixels:{type:"number",value:0,min:0},widthMaxPixels:{type:"number",value:Number.MAX_SAFE_INTEGER,min:0}};class u extends i.Z{getBounds(){var t;return null===(t=this.getAttributeManager())||void 0===t?void 0:t.getBounds(["instanceSourcePositions","instanceTargetPositions"])}getShaders(){return super.getShaders({vs:"#define SHADER_NAME line-layer-vertex-shader\n\nattribute vec3 positions;\nattribute vec3 instanceSourcePositions;\nattribute vec3 instanceTargetPositions;\nattribute vec3 instanceSourcePositions64Low;\nattribute vec3 instanceTargetPositions64Low;\nattribute vec4 instanceColors;\nattribute vec3 instancePickingColors;\nattribute float instanceWidths;\n\nuniform float opacity;\nuniform float widthScale;\nuniform float widthMinPixels;\nuniform float widthMaxPixels;\nuniform float useShortestPath;\nuniform int widthUnits;\n\nvarying vec4 vColor;\nvarying vec2 uv;\nvec2 getExtrusionOffset(vec2 line_clipspace, float offset_direction, float width) {\n  vec2 dir_screenspace = normalize(line_clipspace * project_uViewportSize);\n  dir_screenspace = vec2(-dir_screenspace.y, dir_screenspace.x);\n\n  return dir_screenspace * offset_direction * width / 2.0;\n}\n\nvec3 splitLine(vec3 a, vec3 b, float x) {\n  float t = (x - a.x) / (b.x - a.x);\n  return vec3(x, mix(a.yz, b.yz, t));\n}\n\nvoid main(void) {\n  geometry.worldPosition = instanceSourcePositions;\n  geometry.worldPositionAlt = instanceTargetPositions;\n\n  vec3 source_world = instanceSourcePositions;\n  vec3 target_world = instanceTargetPositions;\n  vec3 source_world_64low = instanceSourcePositions64Low;\n  vec3 target_world_64low = instanceTargetPositions64Low;\n\n  if (useShortestPath > 0.5 || useShortestPath < -0.5) {\n    source_world.x = mod(source_world.x + 180., 360.0) - 180.;\n    target_world.x = mod(target_world.x + 180., 360.0) - 180.;\n    float deltaLng = target_world.x - source_world.x;\n\n    if (deltaLng * useShortestPath > 180.) {\n      source_world.x += 360. * useShortestPath;\n      source_world = splitLine(source_world, target_world, 180. * useShortestPath);\n      source_world_64low = vec3(0.0);\n    } else if (deltaLng * useShortestPath < -180.) {\n      target_world.x += 360. * useShortestPath;\n      target_world = splitLine(source_world, target_world, 180. * useShortestPath);\n      target_world_64low = vec3(0.0);\n    } else if (useShortestPath < 0.) {\n      gl_Position = vec4(0.);\n      return;\n    }\n  }\n  vec4 source_commonspace;\n  vec4 target_commonspace;\n  vec4 source = project_position_to_clipspace(source_world, source_world_64low, vec3(0.), source_commonspace);\n  vec4 target = project_position_to_clipspace(target_world, target_world_64low, vec3(0.), target_commonspace);\n  float segmentIndex = positions.x;\n  vec4 p = mix(source, target, segmentIndex);\n  geometry.position = mix(source_commonspace, target_commonspace, segmentIndex);\n  uv = positions.xy;\n  geometry.uv = uv;\n  geometry.pickingColor = instancePickingColors;\n  float widthPixels = clamp(\n    project_size_to_pixel(instanceWidths * widthScale, widthUnits),\n    widthMinPixels, widthMaxPixels\n  );\n  vec3 offset = vec3(\n    getExtrusionOffset(target.xy - source.xy, positions.y, widthPixels),\n    0.0);\n  DECKGL_FILTER_SIZE(offset, geometry);\n  DECKGL_FILTER_GL_POSITION(p, geometry);\n  gl_Position = p + vec4(project_pixel_size_to_clipspace(offset.xy), 0.0, 0.0);\n  vColor = vec4(instanceColors.rgb, instanceColors.a * opacity);\n  DECKGL_FILTER_COLOR(vColor, geometry);\n}\n",fs:"#define SHADER_NAME line-layer-fragment-shader\n\nprecision highp float;\n\nvarying vec4 vColor;\nvarying vec2 uv;\n\nvoid main(void) {\n  geometry.uv = uv;\n\n  gl_FragColor = vColor;\n\n  DECKGL_FILTER_COLOR(gl_FragColor, geometry);\n}\n",modules:[n.Z,r.Z]})}get wrapLongitude(){return!1}initializeState(){this.getAttributeManager().addInstanced({instanceSourcePositions:{size:3,type:5130,fp64:this.use64bitPositions(),transition:!0,accessor:"getSourcePosition"},instanceTargetPositions:{size:3,type:5130,fp64:this.use64bitPositions(),transition:!0,accessor:"getTargetPosition"},instanceColors:{size:this.props.colorFormat.length,type:5121,normalized:!0,transition:!0,accessor:"getColor",defaultValue:[0,0,0,255]},instanceWidths:{size:1,transition:!0,accessor:"getWidth",defaultValue:1}})}updateState(t){if(super.updateState(t),t.changeFlags.extensionsChanged){var e;const{gl:t}=this.context;null===(e=this.state.model)||void 0===e||e.delete(),this.state.model=this._getModel(t),this.getAttributeManager().invalidateAll()}}draw({uniforms:t}){const{widthUnits:e,widthScale:o,widthMinPixels:s,widthMaxPixels:i,wrapLongitude:n}=this.props;this.state.model.setUniforms(t).setUniforms({widthUnits:a.iI[e],widthScale:o,widthMinPixels:s,widthMaxPixels:i,useShortestPath:n?1:0}).draw(),n&&this.state.model.setUniforms({useShortestPath:-1}).draw()}_getModel(t){return new c.Z(t,{...this.getShaders(),id:this.props.id,geometry:new g.Z({drawMode:5,attributes:{positions:new Float32Array([0,-1,0,0,1,0,1,-1,0,1,1,0])}}),isInstanced:!0})}}(0,s.Z)(u,"layerName","LineLayer"),(0,s.Z)(u,"defaultProps",l);var h=o(491567),d=o(541576);const p=.5,S=1/6,f={N:[0,p],E:[p,0],S:[0,-.5],W:[-.5,0],NE:[p,p],NW:[-.5,p],SE:[p,-.5],SW:[-.5,-.5]},_=[f.W,f.SW,f.S],w=[f.S,f.SE,f.E],m=[f.E,f.NE,f.N],v=[f.NW,f.W,f.N],y=[[-.5,S],[-.5,-S],[-S,-.5],[S,-.5]],E=[[-S,-.5],[S,-.5],[p,-S],[p,S]],N=[[p,-S],[p,S],[S,p],[-S,p]],W=[[-.5,S],[-.5,-S],[S,p],[-S,p]],P=[f.W,f.SW,f.SE,f.E],x=[f.S,f.SE,f.NE,f.N],A=[f.NW,f.W,f.E,f.NE],b=[f.NW,f.SW,f.S,f.N],C=[[-.5,S],[-.5,-S],[p,-S],[p,S]],z=[[-S,-.5],[S,-.5],[S,p],[-S,p]],D=[f.NW,f.SW,f.SE,f.NE],L=[f.NW,f.SW,f.SE,f.E,f.N],O=[f.W,f.SW,f.SE,f.NE,f.N],I=[f.NW,f.W,f.S,f.SE,f.NE],M=[f.NW,f.SW,f.S,f.E,f.NE],R=[f.NW,f.W,[p,-S],[p,S],f.N],T=[[-S,-.5],[S,-.5],f.E,f.NE,f.N],Z=[[-.5,S],[-.5,-S],f.S,f.SE,f.E],F=[f.W,f.SW,f.S,[S,p],[-S,p]],U=[f.NW,f.W,[-S,-.5],[S,-.5],f.N],B=[[-.5,S],[-.5,-S],f.E,f.NE,f.N],k=[f.S,f.SE,f.E,[S,p],[-S,p]],G=[f.W,f.SW,f.S,[p,-S],[p,S]],j=[f.W,f.SW,f.SE,f.E,[S,p],[-S,p]],V=[[-.5,S],[-.5,-S],f.S,f.SE,f.NE,f.N],K=[f.NW,f.W,[-S,-.5],[S,-.5],f.E,f.NE],H=[f.NW,f.SW,f.S,[p,-S],[p,S],f.N],Q=[f.W,f.SW,f.S,f.E,f.NE,f.N],X=[f.NW,f.W,f.S,f.SE,f.E,f.N],q=[[-.5,S],[-.5,-S],[-S,-.5],[S,-.5],f.E,f.NE,f.N],J=[f.W,f.SW,f.S,[p,-S],[p,S],[S,p],[-S,p]],Y=[f.NW,f.W,[-S,-.5],[S,-.5],[p,-S],[p,S],f.N],$=[[-.5,S],[-.5,-S],f.S,f.SE,f.E,[S,p],[-S,p]],tt=[[-.5,S],[-.5,-S],[-S,-.5],[S,-.5],[p,-S],[p,S],[S,p],[-S,p]],et={0:[],1:[[f.W,f.S]],2:[[f.S,f.E]],3:[[f.W,f.E]],4:[[f.N,f.E]],5:{0:[[f.W,f.S],[f.N,f.E]],1:[[f.W,f.N],[f.S,f.E]]},6:[[f.N,f.S]],7:[[f.W,f.N]],8:[[f.W,f.N]],9:[[f.N,f.S]],10:{0:[[f.W,f.N],[f.S,f.E]],1:[[f.W,f.S],[f.N,f.E]]},11:[[f.N,f.E]],12:[[f.W,f.E]],13:[[f.S,f.E]],14:[[f.W,f.S]],15:[]};function ot(t){return parseInt(t,4)}const st={[ot("0000")]:[],[ot("2222")]:[],[ot("2221")]:[_],[ot("2212")]:[w],[ot("2122")]:[m],[ot("1222")]:[v],[ot("0001")]:[_],[ot("0010")]:[w],[ot("0100")]:[m],[ot("1000")]:[v],[ot("2220")]:[y],[ot("2202")]:[E],[ot("2022")]:[N],[ot("0222")]:[W],[ot("0002")]:[y],[ot("0020")]:[E],[ot("0200")]:[N],[ot("2000")]:[W],[ot("0011")]:[P],[ot("0110")]:[x],[ot("1100")]:[A],[ot("1001")]:[b],[ot("2211")]:[P],[ot("2112")]:[x],[ot("1122")]:[A],[ot("1221")]:[b],[ot("2200")]:[C],[ot("2002")]:[z],[ot("0022")]:[C],[ot("0220")]:[z],[ot("1111")]:[D],[ot("1211")]:[L],[ot("2111")]:[O],[ot("1112")]:[I],[ot("1121")]:[M],[ot("1011")]:[L],[ot("0111")]:[O],[ot("1110")]:[I],[ot("1101")]:[M],[ot("1200")]:[R],[ot("0120")]:[T],[ot("0012")]:[Z],[ot("2001")]:[F],[ot("1022")]:[R],[ot("2102")]:[T],[ot("2210")]:[Z],[ot("0221")]:[F],[ot("1002")]:[U],[ot("2100")]:[B],[ot("0210")]:[k],[ot("0021")]:[G],[ot("1220")]:[U],[ot("0122")]:[B],[ot("2012")]:[k],[ot("2201")]:[G],[ot("0211")]:[j],[ot("2110")]:[V],[ot("1102")]:[K],[ot("1021")]:[H],[ot("2011")]:[j],[ot("0112")]:[V],[ot("1120")]:[K],[ot("1201")]:[H],[ot("2101")]:[Q],[ot("0121")]:[Q],[ot("1012")]:[X],[ot("1210")]:[X],[ot("0101")]:{0:[_,m],1:[Q],2:[Q]},[ot("1010")]:{0:[v,w],1:[X],2:[X]},[ot("2121")]:{0:[Q],1:[Q],2:[_,m]},[ot("1212")]:{0:[X],1:[X],2:[v,w]},[ot("2120")]:{0:[q],1:[q],2:[y,m]},[ot("2021")]:{0:[J],1:[J],2:[_,N]},[ot("1202")]:{0:[Y],1:[Y],2:[v,E]},[ot("0212")]:{0:[$],1:[$],2:[w,W]},[ot("0102")]:{0:[y,m],1:[q],2:[q]},[ot("0201")]:{0:[_,N],1:[J],2:[J]},[ot("1020")]:{0:[v,E],1:[Y],2:[Y]},[ot("2010")]:{0:[w,W],1:[$],2:[$]},[ot("2020")]:{0:[W,E],1:[tt],2:[y,N]},[ot("0202")]:{0:[N,y],1:[tt],2:[W,E]}},it={ISO_LINES:1,ISO_BANDS:2},nt={zIndex:0,zOffset:.005};function rt(t,e){return Array.isArray(e)?t<e[0]?0:t<e[1]?1:2:t>=e?1:0}function at(t){const{cellWeights:e,x:o,y:s,width:i,height:n}=t;let r=t.threshold;t.thresholdValue&&(d.Z.deprecated("thresholdValue","threshold")(),r=t.thresholdValue);const a=o<0,c=o>=i-1,g=s<0,l=s>=n-1,u=a||c||g||l,h={},p={};a||l?p.top=0:(h.top=e[(s+1)*i+o],p.top=rt(h.top,r)),c||l?p.topRight=0:(h.topRight=e[(s+1)*i+o+1],p.topRight=rt(h.topRight,r)),c||g?p.right=0:(h.right=e[s*i+o+1],p.right=rt(h.right,r)),a||g?p.current=0:(h.current=e[s*i+o],p.current=rt(h.current,r));const{top:S,topRight:f,right:_,current:w}=p;let m=-1;Number.isFinite(r)&&(m=S<<3|f<<2|_<<1|w),Array.isArray(r)&&(m=S<<6|f<<4|_<<2|w);let v=0;return u||(v=rt((h.top+h.topRight+h.right+h.current)/4,r)),{code:m,meanCode:v}}function ct(t){const{gridOrigin:e,cellSize:o,x:s,y:i,code:n,meanCode:r,type:a=it.ISO_LINES}=t,c={...nt,...t.thresholdData};let g=a===it.ISO_BANDS?st[n]:et[n];Array.isArray(g)||(g=g[r]);const l=c.zIndex*c.zOffset,u=(s+1)*o[0],h=(i+1)*o[1],d=e[0]+u,p=e[1]+h;if(a===it.ISO_BANDS){const t=[];return g.forEach((e=>{const s=[];e.forEach((t=>{const e=d+t[0]*o[0],i=p+t[1]*o[1];s.push([e,i,l])})),t.push(s)})),t}const S=[];return g.forEach((t=>{t.forEach((t=>{const e=d+t[0]*o[0],s=p+t[1]*o[1];S.push([e,s,l])}))})),S}var gt=o(772958),lt=o(844059),ut=o(941669),ht=o(392026);const dt=[255,255,255,255],pt="positions",St={data:{props:["cellSize"]},weights:{props:["aggregation"],accessors:["getWeight"]}};class ft extends ht.Z{initializeState(){super.initializeAggregationLayer({dimensions:St}),this.setState({contourData:{},projectPoints:!1,weights:{count:{size:1,operation:lt.KM.SUM}}}),this.getAttributeManager().add({[pt]:{size:3,accessor:"getPosition",type:5130,fp64:this.use64bitPositions()},count:{size:3,accessor:"getWeight"}})}updateState(t){super.updateState(t);let e=!1;const{oldProps:o,props:s}=t,{aggregationDirty:i}=this.state;o.contours===s.contours&&o.zOffset===s.zOffset||(e=!0,this._updateThresholdData(t.props)),this.getNumInstances()>0&&(i||e)&&this._generateContours()}renderLayers(){const{contourSegments:t,contourPolygons:e}=this.state.contourData,o=this.getSubLayerClass("lines",u),s=this.getSubLayerClass("bands",h.Z);return[t&&t.length>0&&new o(this.getSubLayerProps({id:"lines"}),{data:this.state.contourData.contourSegments,getSourcePosition:t=>t.start,getTargetPosition:t=>t.end,getColor:t=>t.contour.color||dt,getWidth:t=>t.contour.strokeWidth||1}),e&&e.length>0&&new s(this.getSubLayerProps({id:"bands"}),{data:this.state.contourData.contourPolygons,getPolygon:t=>t.vertices,getFillColor:t=>t.contour.color||dt})]}updateAggregationState(t){const{props:e,oldProps:o}=t,{cellSize:s,coordinateSystem:i}=e,{viewport:n}=this.context,r=o.cellSize!==s;let a=e.gpuAggregation;this.state.gpuAggregation!==e.gpuAggregation&&a&&!gt.Z.isSupported(this.context.gl)&&(d.Z.warn("GPU Grid Aggregation not supported, falling back to CPU")(),a=!1);const c=a!==this.state.gpuAggregation;this.setState({gpuAggregation:a});const{dimensions:g}=this.state,l=this.isAttributeChanged(pt),{data:u,weights:h}=g;let{boundingBox:p}=this.state;if(l&&(p=(0,ut.A5)(this.getAttributes(),this.getNumInstances()),this.setState({boundingBox:p})),l||r){const{gridOffset:t,translation:e,width:o,height:r,numCol:a,numRow:c}=(0,ut.PQ)(p,s,n,i);this.allocateResources(c,a),this.setState({gridOffset:t,boundingBox:p,translation:e,posOffset:e.slice(),gridOrigin:[-1*e[0],-1*e[1]],width:o,height:r,numCol:a,numRow:c})}const S=l||c||this.isAggregationDirty(t,{dimension:u,compareAll:a}),f=this.isAggregationDirty(t,{dimension:h});f&&this._updateAccessors(t),(S||f)&&this._resetResults(),this.setState({aggregationDataDirty:S,aggregationWeightsDirty:f})}_updateAccessors(t){const{getWeight:e,aggregation:o,data:s}=t.props,{count:i}=this.state.weights;i&&(i.getWeight=e,i.operation=lt.KM[o]),this.setState({getValue:(0,lt._D)(o,e,{data:s})})}_resetResults(){const{count:t}=this.state.weights;t&&(t.aggregationData=null)}_generateContours(){const{numCol:t,numRow:e,gridOrigin:o,gridOffset:s,thresholdData:i}=this.state,{count:n}=this.state.weights;let{aggregationData:r}=n;r||(r=n.aggregationBuffer.getData(),n.aggregationData=r);const{cellWeights:a}=gt.Z.getCellData({countsData:r}),c=function({thresholdData:t,cellWeights:e,gridSize:o,gridOrigin:s,cellSize:i}){const n=[],r=[],a=o[0],c=o[1];let g=0,l=0;for(const o of t){const{contour:t}=o,{threshold:u}=t;for(let h=-1;h<a;h++)for(let d=-1;d<c;d++){const{code:p,meanCode:S}=at({cellWeights:e,threshold:u,x:h,y:d,width:a,height:c}),f={type:it.ISO_BANDS,gridOrigin:s,cellSize:i,x:h,y:d,width:a,height:c,code:p,meanCode:S,thresholdData:o};if(Array.isArray(u)){f.type=it.ISO_BANDS;const e=ct(f);for(const o of e)r[l++]={vertices:o,contour:t}}else{f.type=it.ISO_LINES;const e=ct(f);for(let o=0;o<e.length;o+=2)n[g++]={start:e[o],end:e[o+1],contour:t}}}}return{contourSegments:n,contourPolygons:r}}({thresholdData:i,cellWeights:a,gridSize:[t,e],gridOrigin:o,cellSize:[s.xOffset,s.yOffset]});this.setState({contourData:c})}_updateThresholdData(t){const{contours:e,zOffset:o}=t,s=e.length,i=new Array(s);for(let t=0;t<s;t++){const s=e[t];i[t]={contour:s,zIndex:s.zIndex||t,zOffset:o}}this.setState({thresholdData:i})}}(0,s.Z)(ft,"layerName","ContourLayer"),(0,s.Z)(ft,"defaultProps",{cellSize:{type:"number",min:1,max:1e3,value:1e3},getPosition:{type:"accessor",value:t=>t.position},getWeight:{type:"accessor",value:1},gpuAggregation:!0,aggregation:"SUM",contours:{type:"object",value:[{threshold:1}],optional:!0,compare:3},zOffset:.005})}}]);
//# sourceMappingURL=a03285b1dc884048474f.chunk.js.map