"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[3251],{389033:(t,e,n)=>{n.d(e,{Z:()=>c});var r=n(204942),i=n(336750),s=n(149331),o=n(184287),a=n(739450);function u(t,e){const n={};for(const r in t)e.includes(r)||(n[r]=t[r]);return n}class c extends i.Z{constructor(...t){super(...t),(0,r.Z)(this,"state",void 0)}initializeAggregationLayer(t){super.initializeState(this.context),this.setState({ignoreProps:u(this.constructor._propTypes,t.data.props),dimensions:t})}updateState(t){super.updateState(t);const{changeFlags:e}=t;if(e.extensionsChanged){const t=this.getShaders({});t&&t.defines&&(t.defines.NON_INSTANCED_MODEL=1),this.updateShaders(t)}this._updateAttributes()}updateAttributes(t){this.setState({changedAttributes:t})}getAttributes(){return this.getAttributeManager().getShaderAttributes()}getModuleSettings(){const{viewport:t,mousePosition:e,gl:n}=this.context;return Object.assign(Object.create(this.props),{viewport:t,mousePosition:e,pickingActive:0,devicePixelRatio:(0,a.w)(n)})}updateShaders(t){}isAggregationDirty(t,e={}){const{props:n,oldProps:r,changeFlags:i}=t,{compareAll:o=!1,dimension:a}=e,{ignoreProps:u}=this.state,{props:c,accessors:l=[]}=a,{updateTriggersChanged:g}=i;if(i.dataChanged)return!0;if(g){if(g.all)return!0;for(const t of l)if(g[t])return!0}if(o)return!!i.extensionsChanged||(0,s.tg)({oldProps:r,newProps:n,ignoreProps:u,propTypes:this.constructor._propTypes});for(const t of c)if(n[t]!==r[t])return!0;return!1}isAttributeChanged(t){const{changedAttributes:e}=this.state;return t?e&&void 0!==e[t]:!function(t){let e=!0;for(const n in t){e=!1;break}return e}(e)}_getAttributeManager(){return new o.Z(this.context.gl,{id:this.props.id,stats:this.context.stats})}}(0,r.Z)(c,"layerName","AggregationLayer")},844059:(t,e,n)=>{n.d(e,{KM:()=>r,_D:()=>a,q5:()=>u});const r={SUM:1,MEAN:2,MIN:3,MAX:4};function i(t,e){return t+e}function s(t,e){return e>t?e:t}function o(t,e){return e<t?e:t}function a(t,e,n){const a=r[t]||r.SUM;switch(e=function(t,e={}){return Number.isFinite(t)?t:n=>(e.index=n.index,t(n.source,e))}(e,n),a){case r.MIN:return t=>function(t,e){if(Number.isFinite(e))return t.length?e:null;const n=t.map(e).filter(Number.isFinite);return n.length?n.reduce(o,1/0):null}(t,e);case r.SUM:return t=>function(t,e){if(Number.isFinite(e))return t.length?t.length*e:null;const n=t.map(e).filter(Number.isFinite);return n.length?n.reduce(i,0):null}(t,e);case r.MEAN:return t=>function(t,e){if(Number.isFinite(e))return t.length?e:null;const n=t.map(e).filter(Number.isFinite);return n.length?n.reduce(i,0)/n.length:null}(t,e);case r.MAX:return t=>function(t,e){if(Number.isFinite(e))return t.length?e:null;const n=t.map(e).filter(Number.isFinite);return n.length?n.reduce(s,-1/0):null}(t,e);default:return null}}function u(t,e={}){return n=>(e.indices=n.map((t=>t.index)),t(n.map((t=>t.source)),e))}},489713:(t,e,n)=>{n.d(e,{Z:()=>l});var r=n(204942),i=n(833312);const s=t=>t.length,o=t=>t.points,a=t=>t.index,u=(t,e)=>t<e?-1:t>e?1:t>=e?0:NaN,c={getValue:s,getPoints:o,getIndex:a,filterData:null};class l{constructor(t=[],e=c){(0,r.Z)(this,"maxCount",void 0),(0,r.Z)(this,"maxValue",void 0),(0,r.Z)(this,"minValue",void 0),(0,r.Z)(this,"totalCount",void 0),(0,r.Z)(this,"aggregatedBins",void 0),(0,r.Z)(this,"sortedBins",void 0),(0,r.Z)(this,"binMap",void 0),this.aggregatedBins=this.getAggregatedBins(t,e),this._updateMinMaxValues(),this.binMap=this.getBinMap()}getAggregatedBins(t,e){const{getValue:n=s,getPoints:r=o,getIndex:i=a,filterData:u}=e,c="function"==typeof u,l=t.length,g=[];let h=0;for(let e=0;e<l;e++){const s=t[e],o=r(s),a=i(s),l=c?o.filter(u):o;s.filteredPoints=c?l:null;const d=l.length?n(l):null;null!=d&&(g[h]={i:Number.isFinite(a)?a:e,value:d,counts:l.length},h++)}return g}_percentileToIndex(t){const e=this.sortedBins.length;if(e<2)return[0,0];const[n,r]=t.map((t=>(0,i.uZ)(t,0,100)));return[Math.ceil(n/100*(e-1)),Math.floor(r/100*(e-1))]}getBinMap(){const t={};for(const e of this.aggregatedBins)t[e.i]=e;return t}_updateMinMaxValues(){let t=0,e=0,n=3402823466e29,r=0;for(const i of this.aggregatedBins)t=t>i.counts?t:i.counts,e=e>i.value?e:i.value,n=n<i.value?n:i.value,r+=i.counts;this.maxCount=t,this.maxValue=e,this.minValue=n,this.totalCount=r}getValueRange(t){if(this.sortedBins||(this.sortedBins=this.aggregatedBins.sort(((t,e)=>u(t.value,e.value)))),!this.sortedBins.length)return[];let e=0,n=this.sortedBins.length-1;if(Array.isArray(t)){const r=this._percentileToIndex(t);e=r[0],n=r[1]}return[this.sortedBins[e].value,this.sortedBins[n].value]}getValueDomainByScale(t,[e=0,n=100]=[]){if(this.sortedBins||(this.sortedBins=this.aggregatedBins.sort(((t,e)=>u(t.value,e.value)))),!this.sortedBins.length)return[];const r=this._percentileToIndex([e,n]);return this._getScaleDomain(t,r)}_getScaleDomain(t,[e,n]){const r=this.sortedBins;switch(t){case"quantize":case"linear":default:return[r[e].value,r[n].value];case"quantile":return(0,i.N4)(r.slice(e,n+1),(t=>t.value));case"ordinal":return(0,i.Rr)(r,(t=>t.value))}}}},833312:(t,e,n)=>{n.d(e,{N4:()=>d,Rr:()=>p,ge:()=>b,uZ:()=>f});var r=n(541576);function i(t,e,n){const r=n;return r.domain=()=>t,r.range=()=>e,r}function s(t,e){return i(t,e,(n=>function(t,e,n){const i=t[1]-t[0];if(i<=0)return r.Z.warn("quantizeScale: invalid domain, returning range[0]")(),e[0];const s=i/e.length,o=Math.floor((n-t[0])/s);return e[Math.max(Math.min(o,e.length-1),0)]}(t,e,n)))}function o(t,e){return i(t,e,(n=>function(t,e,n){return(n-t[0])/(t[1]-t[0])*(e[1]-e[0])+e[0]}(t,e,n)))}function a(t,e){const n=t.sort(u);let r=0;const s=Math.max(1,e.length),o=new Array(s-1);for(;++r<s;)o[r-1]=c(n,r/s);const a=t=>function(t,e,n){return e[function(t,e){let n=0,r=t.length;for(;n<r;){const i=n+r>>>1;u(t[i],e)>0?r=i:n=i+1}return n}(t,n)]}(o,e,t);return a.thresholds=()=>o,i(t,e,a)}function u(t,e){return t-e}function c(t,e){const n=t.length;if(e<=0||n<2)return t[0];if(e>=1)return t[n-1];const r=(n-1)*e,i=Math.floor(r),s=t[i];return s+(t[i+1]-s)*(r-i)}function l(t,e){const n=new Map,r=[];for(const e of t){const t="".concat(e);n.has(t)||n.set(t,r.push(e))}return i(t,e,(t=>function(t,e,n,r){const i="".concat(r);let s=e.get(i);return void 0===s&&(s=t.push(r),e.set(i,s)),n[(s-1)%n.length]}(r,n,e,t)))}function g(t){return null!=t}function h(t,e){return("function"==typeof e?t.map(e):t).filter(g)}function d(t,e){return h(t,e)}function p(t,e){return function(t){const e=[];return t.forEach((t=>{!e.includes(t)&&g(t)&&e.push(t)})),e}(h(t,e))}function f(t,e,n){return Math.max(e,Math.min(n,t))}function b(t){switch(t){case"quantize":default:return s;case"linear":return o;case"quantile":return a;case"ordinal":return l}}},336750:(t,e,n)=>{n.d(e,{Z:()=>u});var r=n(204942),i=n(905259),s=n(911482),o=n(77552),a=n(33230);class u extends i.Z{get isComposite(){return!0}get isLoaded(){return super.isLoaded&&this.getSubLayers().every((t=>t.isLoaded))}getSubLayers(){return this.internalState&&this.internalState.subLayers||[]}initializeState(t){}setState(t){super.setState(t),this.setNeedsUpdate()}getPickingInfo({info:t}){const{object:e}=t;return e&&e.__source&&e.__source.parent&&e.__source.parent.id===this.id?(t.object=e.__source.object,t.index=e.__source.index,t):t}filterSubLayer(t){return!0}shouldRenderSubLayer(t,e){return e&&e.length}getSubLayerClass(t,e){const{_subLayerProps:n}=this.props;return n&&n[t]&&n[t].type||e}getSubLayerRow(t,e,n){return t.__source={parent:this,object:e,index:n},t}getSubLayerAccessor(t){if("function"==typeof t){const e={index:-1,data:this.props.data,target:[]};return(n,r)=>n&&n.__source?(e.index=n.__source.index,t(n.__source.object,e)):t(n,r)}return t}getSubLayerProps(t={}){var e;const{opacity:n,pickable:r,visible:i,parameters:s,getPolygonOffset:o,highlightedObjectIndex:u,autoHighlight:c,highlightColor:l,coordinateSystem:g,coordinateOrigin:h,wrapLongitude:d,positionFormat:p,modelMatrix:f,extensions:b,fetch:m,operation:y,_subLayerProps:v}=this.props,x={id:"",updateTriggers:{},opacity:n,pickable:r,visible:i,parameters:s,getPolygonOffset:o,highlightedObjectIndex:u,autoHighlight:c,highlightColor:l,coordinateSystem:g,coordinateOrigin:h,wrapLongitude:d,positionFormat:p,modelMatrix:f,extensions:b,fetch:m,operation:y},S=v&&t.id&&v[t.id],_=S&&S.updateTriggers,M=t.id||"sublayer";if(S){const e=this.props[a.Wb],n=t.type?t.type._propTypes:{};for(const t in S){const r=n[t]||e[t];r&&"accessor"===r.type&&(S[t]=this.getSubLayerAccessor(S[t]))}}Object.assign(x,t,S),x.id="".concat(this.props.id,"-").concat(M),x.updateTriggers={all:null===(e=this.props.updateTriggers)||void 0===e?void 0:e.all,...t.updateTriggers,..._};for(const t of b){const e=t.getSubLayerProps.call(this,t);e&&Object.assign(x,e,{updateTriggers:Object.assign(x.updateTriggers,e.updateTriggers)})}return x}_updateAutoHighlight(t){for(const e of this.getSubLayers())e.updateAutoHighlight(t)}_getAttributeManager(){return null}_postUpdate(t,e){let n=this.internalState.subLayers;const r=!n||this.needsUpdate();if(r){const t=this.renderLayers();n=(0,o.x)(t,Boolean),this.internalState.subLayers=n}(0,s.Z)("compositeLayer.renderLayers",this,r,n);for(const t of n)t.parent=this}}(0,r.Z)(u,"layerName","CompositeLayer")}}]);
//# sourceMappingURL=f2143106c6117d7bb88f.chunk.js.map