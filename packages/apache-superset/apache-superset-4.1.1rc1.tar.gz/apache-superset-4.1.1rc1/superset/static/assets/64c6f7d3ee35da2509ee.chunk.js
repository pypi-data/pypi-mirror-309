"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[5672],{185672:(t,e,o)=>{o.d(e,{Z:()=>B});var n=o(204942),i=o(739450);const s=new Float32Array(12);function r(t,e=2){let o=0;for(const n of t)for(let t=0;t<e;t++)s[o++]=n[t]||0;return s}var a=o(106948),u=o(844211),l=o(904912),h=o(263346),d=o(53478),g=o(541576),c=o(733321),m=o(184287),p=o(339769),x=o(453982),T=o(905259),f=o(537832);class v extends T.Z{getShaders(){return{vs:"#define SHADER_NAME heatp-map-layer-vertex-shader\n\nuniform sampler2D maxTexture;\nuniform float intensity;\nuniform vec2 colorDomain;\nuniform float threshold;\nuniform float aggregationMode;\n\nattribute vec3 positions;\nattribute vec2 texCoords;\n\nvarying vec2 vTexCoords;\nvarying float vIntensityMin;\nvarying float vIntensityMax;\n\nvoid main(void) {\n  gl_Position = project_position_to_clipspace(positions, vec3(0.0), vec3(0.0));\n  vTexCoords = texCoords;\n  vec4 maxTexture = texture2D(maxTexture, vec2(0.5));\n  float maxValue = aggregationMode < 0.5 ? maxTexture.r : maxTexture.g;\n  float minValue = maxValue * threshold;\n  if (colorDomain[1] > 0.) {\n    maxValue = colorDomain[1];\n    minValue = colorDomain[0];\n  }\n  vIntensityMax = intensity / maxValue;\n  vIntensityMin = intensity / minValue;\n}\n",fs:"#define SHADER_NAME triangle-layer-fragment-shader\n\nprecision highp float;\n\nuniform float opacity;\nuniform sampler2D texture;\nuniform sampler2D colorTexture;\nuniform float aggregationMode;\n\nvarying vec2 vTexCoords;\nvarying float vIntensityMin;\nvarying float vIntensityMax;\n\nvec4 getLinearColor(float value) {\n  float factor = clamp(value * vIntensityMax, 0., 1.);\n  vec4 color = texture2D(colorTexture, vec2(factor, 0.5));\n  color.a *= min(value * vIntensityMin, 1.0);\n  return color;\n}\n\nvoid main(void) {\n  vec4 weights = texture2D(texture, vTexCoords);\n  float weight = weights.r;\n\n  if (aggregationMode > 0.5) {\n    weight /= max(1.0, weights.a);\n  }\n  if (weight <= 0.) {\n     discard;\n  }\n\n  vec4 linearColor = getLinearColor(weight);\n  linearColor.a *= opacity;\n  gl_FragColor =linearColor;\n}\n",modules:[f.Z]}}initializeState({gl:t}){this.getAttributeManager().add({positions:{size:3,noAlloc:!0},texCoords:{size:2,noAlloc:!0}}),this.setState({model:this._getModel(t)})}_getModel(t){const{vertexCount:e}=this.props;return new p.Z(t,{...this.getShaders(),id:this.props.id,geometry:new x.Z({drawMode:6,vertexCount:e})})}draw({uniforms:t}){const{model:e}=this.state,{texture:o,maxTexture:n,colorTexture:i,intensity:s,threshold:r,aggregationMode:a,colorDomain:u}=this.props;e.setUniforms({...t,texture:o,maxTexture:n,colorTexture:i,intensity:s,threshold:r,aggregationMode:a,colorDomain:u}).draw()}}(0,n.Z)(v,"layerName","TriangleLayer");var w=o(389033),y=o(579543);const _={mipmaps:!1,parameters:{10240:9729,10241:9729,10242:33071,10243:33071},dataFormat:6408},S=[0,0],C={SUM:0,MEAN:1},M={getPosition:{type:"accessor",value:t=>t.position},getWeight:{type:"accessor",value:1},intensity:{type:"number",min:0,value:1},radiusPixels:{type:"number",min:1,max:100,value:50},colorRange:y.K,threshold:{type:"number",min:0,max:1,value:.05},colorDomain:{type:"array",value:null,optional:!0},aggregation:"SUM",weightsTextureSize:{type:"number",min:128,max:2048,value:2048},debounceTimeout:{type:"number",min:0,max:1e3,value:500}},b=[a.h.BLEND_EQUATION_MINMAX,a.h.TEXTURE_FLOAT],D=[a.h.COLOR_ATTACHMENT_RGBA32F,a.h.FLOAT_BLEND],P={data:{props:["radiusPixels"]}};class B extends w.Z{constructor(...t){super(...t),(0,n.Z)(this,"state",void 0)}initializeState(){const{gl:t}=this.context;if(!(0,u.ag)(t,b))return this.setState({supported:!1}),void g.Z.error("HeatmapLayer: ".concat(this.id," is not supported on this browser"))();super.initializeAggregationLayer(P),this.setState({supported:!0,colorDomain:S}),this._setupTextureParams(),this._setupAttributes(),this._setupResources()}shouldUpdateState({changeFlags:t}){return t.somethingChanged}updateState(t){this.state.supported&&(super.updateState(t),this._updateHeatmapState(t))}_updateHeatmapState(t){const{props:e,oldProps:o}=t,n=this._getChangeFlags(t);(n.dataChanged||n.viewportChanged)&&(n.boundsChanged=this._updateBounds(n.dataChanged),this._updateTextureRenderingBounds()),n.dataChanged||n.boundsChanged?(clearTimeout(this.state.updateTimer),this.setState({isWeightMapDirty:!0})):n.viewportZoomChanged&&this._debouncedUpdateWeightmap(),e.colorRange!==o.colorRange&&this._updateColorTexture(t),this.state.isWeightMapDirty&&this._updateWeightmap(),this.setState({zoom:t.context.viewport.zoom})}renderLayers(){if(!this.state.supported)return[];const{weightsTexture:t,triPositionBuffer:e,triTexCoordBuffer:o,maxWeightsTexture:n,colorTexture:i,colorDomain:s}=this.state,{updateTriggers:r,intensity:a,threshold:u,aggregation:l}=this.props;return new(this.getSubLayerClass("triangle",v))(this.getSubLayerProps({id:"triangle-layer",updateTriggers:r}),{coordinateSystem:c.Df.DEFAULT,data:{attributes:{positions:e,texCoords:o}},vertexCount:4,maxTexture:n,colorTexture:i,aggregationMode:C[l]||0,texture:t,intensity:a,threshold:u,colorDomain:s})}finalizeState(t){super.finalizeState(t);const{weightsTransform:e,weightsTexture:o,maxWeightTransform:n,maxWeightsTexture:i,triPositionBuffer:s,triTexCoordBuffer:r,colorTexture:a,updateTimer:u}=this.state;null==e||e.delete(),null==o||o.delete(),null==n||n.delete(),null==i||i.delete(),null==s||s.delete(),null==r||r.delete(),null==a||a.delete(),u&&clearTimeout(u)}_getAttributeManager(){return new m.Z(this.context.gl,{id:this.props.id,stats:this.context.stats})}_getChangeFlags(t){const e={},{dimensions:o}=this.state;e.dataChanged=this.isAttributeChanged()||this.isAggregationDirty(t,{compareAll:!0,dimension:o.data}),e.viewportChanged=t.changeFlags.viewportChanged;const{zoom:n}=this.state;return t.context.viewport&&t.context.viewport.zoom===n||(e.viewportZoomChanged=!0),e}_createTextures(){const{gl:t}=this.context,{textureSize:e,format:o,type:n}=this.state;this.setState({weightsTexture:new l.Z(t,{width:e,height:e,format:o,type:n,..._}),maxWeightsTexture:new l.Z(t,{format:o,type:n,..._})})}_setupAttributes(){this.getAttributeManager().add({positions:{size:3,type:5130,accessor:"getPosition"},weights:{size:1,accessor:"getWeight"}}),this.setState({positionAttributeName:"positions"})}_setupTextureParams(){const{gl:t}=this.context,{weightsTextureSize:e}=this.props,o=Math.min(e,(0,i.ZS)(t,3379)),n=(0,u.ag)(t,D),{format:s,type:r}=function({gl:t,floatTargetSupport:e}){return e?{format:(0,i.D0)(t)?34836:6408,type:5126}:{format:6408,type:5121}}({gl:t,floatTargetSupport:n}),a=n?1:1/255;this.setState({textureSize:o,format:s,type:r,weightsScale:a}),n||g.Z.warn("HeatmapLayer: ".concat(this.id," rendering to float texture not supported, fallingback to low precession format"))()}getShaders(t){return super.getShaders("max-weights-transform"===t?{vs:"attribute vec4 inTexture;\nvarying vec4 outTexture;\n\nvoid main()\n{\noutTexture = inTexture;\ngl_Position = vec4(0, 0, 0, 1.);\ngl_PointSize = 1.0;\n}\n",_fs:"varying vec4 outTexture;\nvoid main() {\n  gl_FragColor = outTexture;\n  gl_FragColor.g = outTexture.r / max(1.0, outTexture.a);\n}\n"}:{vs:"attribute vec3 positions;\nattribute vec3 positions64Low;\nattribute float weights;\nvarying vec4 weightsTexture;\nuniform float radiusPixels;\nuniform float textureWidth;\nuniform vec4 commonBounds;\nuniform float weightsScale;\nvoid main()\n{\n  weightsTexture = vec4(weights * weightsScale, 0., 0., 1.);\n\n  float radiusTexels  = project_pixel_size(radiusPixels) * textureWidth / (commonBounds.z - commonBounds.x);\n  gl_PointSize = radiusTexels * 2.;\n\n  vec3 commonPosition = project_position(positions, positions64Low);\n  gl_Position.xy = (commonPosition.xy - commonBounds.xy) / (commonBounds.zw - commonBounds.xy) ;\n  gl_Position.xy = (gl_Position.xy * 2.) - (1.);\n}\n",_fs:"varying vec4 weightsTexture;\nfloat gaussianKDE(float u){\n  return pow(2.71828, -u*u/0.05555)/(1.77245385*0.166666);\n}\nvoid main()\n{\n  float dist = length(gl_PointCoord - vec2(0.5, 0.5));\n  if (dist > 0.5) {\n    discard;\n  }\n  gl_FragColor = weightsTexture * gaussianKDE(2. * dist);\n  DECKGL_FILTER_COLOR(gl_FragColor, geometry);\n}\n"})}_createWeightsTransform(t={}){var e;const{gl:o}=this.context;let{weightsTransform:n}=this.state;const{weightsTexture:i}=this.state;null===(e=n)||void 0===e||e.delete(),n=new h.Z(o,{id:"".concat(this.id,"-weights-transform"),elementCount:1,_targetTexture:i,_targetTextureVarying:"weightsTexture",...t}),this.setState({weightsTransform:n})}_setupResources(){const{gl:t}=this.context;this._createTextures();const{textureSize:e,weightsTexture:o,maxWeightsTexture:n}=this.state,i=this.getShaders("weights-transform");this._createWeightsTransform(i);const s=this.getShaders("max-weights-transform"),r=new h.Z(t,{id:"".concat(this.id,"-max-weights-transform"),_sourceTextures:{inTexture:o},_targetTexture:n,_targetTextureVarying:"outTexture",...s,elementCount:e*e});this.setState({weightsTexture:o,maxWeightsTexture:n,maxWeightTransform:r,zoom:null,triPositionBuffer:new d.Z(t,{byteLength:48,accessor:{size:3}}),triTexCoordBuffer:new d.Z(t,{byteLength:48,accessor:{size:2}})})}updateShaders(t){this._createWeightsTransform(t)}_updateMaxWeightValue(){const{maxWeightTransform:t}=this.state;t.run({parameters:{blend:!0,depthTest:!1,blendFunc:[1,1],blendEquation:32776}})}_updateBounds(t=!1){const{viewport:e}=this.context,o=[e.unproject([0,0]),e.unproject([e.width,0]),e.unproject([e.width,e.height]),e.unproject([0,e.height])].map((t=>t.map(Math.fround))),n=function(t){const e=t.map((t=>t[0])),o=t.map((t=>t[1])),n=Math.min.apply(null,e),i=Math.max.apply(null,e);return[n,Math.min.apply(null,o),i,Math.max.apply(null,o)]}(o),i={visibleWorldBounds:n,viewportCorners:o};let s=!1;if(t||!this.state.worldBounds||(r=this.state.worldBounds,!((a=n)[0]>=r[0]&&a[2]<=r[2]&&a[1]>=r[1]&&a[3]<=r[3]))){const t=this._worldToCommonBounds(n),e=this._commonToWorldBounds(t);this.props.coordinateSystem===c.Df.LNGLAT&&(e[1]=Math.max(e[1],-85.051129),e[3]=Math.min(e[3],85.051129),e[0]=Math.max(e[0],-360),e[2]=Math.min(e[2],360));const o=this._worldToCommonBounds(e);i.worldBounds=e,i.normalizedCommonBounds=o,s=!0}var r,a;return this.setState(i),s}_updateTextureRenderingBounds(){const{triPositionBuffer:t,triTexCoordBuffer:e,normalizedCommonBounds:o,viewportCorners:n}=this.state,{viewport:i}=this.context;t.subData(r(n,3));const s=n.map((t=>function(t,e){const[o,n,i,s]=e;return[(t[0]-o)/(i-o),(t[1]-n)/(s-n)]}(i.projectPosition(t),o)));e.subData(r(s,2))}_updateColorTexture(t){const{colorRange:e}=t.props;let{colorTexture:o}=this.state;const n=(0,y.P)(e,!1,Uint8Array);o?o.setImageData({data:n,width:e.length}):o=new l.Z(this.context.gl,{data:n,width:e.length,height:1,..._}),this.setState({colorTexture:o})}_updateWeightmap(){const{radiusPixels:t,colorDomain:e,aggregation:o}=this.props,{weightsTransform:n,worldBounds:s,textureSize:r,weightsTexture:a,weightsScale:u}=this.state;this.state.isWeightMapDirty=!1;const l=this._worldToCommonBounds(s,{useLayerCoordinateSystem:!0});if(e&&"SUM"===o){const{viewport:t}=this.context,o=t.distanceScales.metersPerUnit[2]*(l[2]-l[0])/r;this.state.colorDomain=e.map((t=>t*o*u))}else this.state.colorDomain=e||S;const h={radiusPixels:t,commonBounds:l,textureWidth:r,weightsScale:u};n.update({elementCount:this.getNumInstances()}),(0,i.s8)(this.context.gl,{clearColor:[0,0,0,0]},(()=>{n.run({uniforms:h,parameters:{blend:!0,depthTest:!1,blendFunc:[1,1],blendEquation:32774},clearRenderTarget:!0,attributes:this.getAttributes(),moduleSettings:this.getModuleSettings()})})),this._updateMaxWeightValue(),a.setParameters({10240:9729,10241:9729})}_debouncedUpdateWeightmap(t=!1){let{updateTimer:e}=this.state;const{debounceTimeout:o}=this.props;t?(e=null,this._updateBounds(!0),this._updateTextureRenderingBounds(),this.setState({isWeightMapDirty:!0})):(this.setState({isWeightMapDirty:!1}),clearTimeout(e),e=setTimeout(this._debouncedUpdateWeightmap.bind(this,!0),o)),this.setState({updateTimer:e})}_worldToCommonBounds(t,e={}){const{useLayerCoordinateSystem:o=!1}=e,[n,i,s,r]=t,{viewport:a}=this.context,{textureSize:u}=this.state,{coordinateSystem:l}=this.props,h=o&&(l===c.Df.LNGLAT_OFFSETS||l===c.Df.METER_OFFSETS),d=h?a.projectPosition(this.props.coordinateOrigin):[0,0],g=2*u/a.scale;let m,p;return o&&!h?(m=this.projectPosition([n,i,0]),p=this.projectPosition([s,r,0])):(m=a.projectPosition([n,i,0]),p=a.projectPosition([s,r,0])),function(t,e,o){const[n,i,s,r]=t,a=s-n,u=r-i;let l=a,h=u;a/u<e/o?l=e/o*u:h=o/e*a,l<e&&(l=e,h=o);const d=(s+n)/2,g=(r+i)/2;return[d-l/2,g-h/2,d+l/2,g+h/2]}([m[0]-d[0],m[1]-d[1],p[0]-d[0],p[1]-d[1]],g,g)}_commonToWorldBounds(t){const[e,o,n,i]=t,{viewport:s}=this.context,r=s.unprojectPosition([e,o]),a=s.unprojectPosition([n,i]);return r.slice(0,2).concat(a.slice(0,2))}}(0,n.Z)(B,"layerName","HeatmapLayer"),(0,n.Z)(B,"defaultProps",M)}}]);
//# sourceMappingURL=64c6f7d3ee35da2509ee.chunk.js.map