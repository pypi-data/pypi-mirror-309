"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[616],{680616:(e,t,r)=>{r.r(t),r.d(t,{default:()=>a});var n=r(263475),l=r(499381),s=r(135944);function a(e){const{height:t,width:r,echartOptions:a,selectedValues:c,refs:u}=e,i=(0,l.C0)(e);return(0,s.tZ)(n.Z,{refs:u,height:t,width:r,echartOptions:a,eventHandlers:i,selectedValues:c})}},263475:(e,t,r)=>{r.d(t,{Z:()=>S});var n=r(667294),l=r(751995),s=r(768023),a=r(281615),c=r(967021),u=r(358062),i=r(781836),o=r(873463),h=r(216026),d=r(259048),f=r(15746),p=r(126947),g=r(302907),N=r(516049),v=r(541969),m=r(938198),b=r(548785),w=r(557494),y=r(570012),k=r(730322),E=r(655958),C=r(603174),F=r(731281),O=r(210680),M=r(347106),V=r(693450),Z=r(499326),I=r(617813),j=r(129167),x=r(787164),D=r(135944);const R=l.iK.div`
  height: ${({height:e})=>e};
  width: ${({width:e})=>e};
`;function H({width:e,height:t,echartOptions:r,eventHandlers:l,zrEventHandlers:s,selectedValues:c={},refs:u},i){const o=(0,n.useRef)(null);u&&(u.divRef=o);const h=(0,n.useRef)(),d=(0,n.useMemo)((()=>Object.keys(c)||[]),[c]),f=(0,n.useRef)([]);(0,n.useImperativeHandle)(i,(()=>({getEchartInstance:()=>h.current}))),(0,n.useEffect)((()=>{o.current&&(h.current||(h.current=(0,a.S1)(o.current)),Object.entries(l||{}).forEach((([e,t])=>{var r,n;null==(r=h.current)||r.off(e),null==(n=h.current)||n.on(e,t)})),Object.entries(s||{}).forEach((([e,t])=>{var r,n;null==(r=h.current)||r.getZr().off(e),null==(n=h.current)||n.getZr().on(e,t)})),h.current.setOption(r,!0))}),[r,l,s]),(0,n.useEffect)((()=>{h.current&&(h.current.dispatchAction({type:"downplay",dataIndex:f.current.filter((e=>!d.includes(e)))}),d.length&&h.current.dispatchAction({type:"highlight",dataIndex:d}),f.current=d)}),[d]);const p=(0,n.useCallback)((({width:e,height:t})=>{h.current&&h.current.resize({width:e,height:t})}),[]);return(0,n.useEffect)((()=>(p({width:e,height:t}),()=>{var e;return null==(e=h.current)?void 0:e.dispose()})),[]),(0,n.useLayoutEffect)((()=>{p({width:e,height:t})}),[e,t,p]),(0,D.tZ)(R,{ref:o,height:t,width:e})}(0,s.D)([y.N,c.N,u.N,i.N,o.N,h.N,d.N,f.N,p.N,g.N,N.N,v.N,m.N,b.N,w.N,k.N,E.N,C.N,F.N,O.N,M.N,V.N,Z.N,I.N,j.N,x.T]);const S=(0,n.forwardRef)(H)},499381:(e,t,r)=>{r.d(t,{C0:()=>d});var n=r(850308),l=r.n(n),s=r(751115),a=r(767190),c=r(310581),u=r(806915);const i=(e,t,r)=>n=>{const l=Object.values(e);let s;s=l.includes(n)?l.filter((e=>e!==n)):[n];const a=s.map((e=>r[e]));return{dataMask:{extraFormData:{filters:0===s.length?[]:t.map(((e,t)=>{const r=a.map((e=>e[t]));return null==r?{col:e,op:"IS NULL"}:{col:e,op:"IN",val:r}}))},filterState:{value:a.length?a:null,selectedValues:s.length?s:null}},isCurrentValueSelected:l.includes(n)}},o=(e,t,r)=>({name:n})=>{var l;if(!r)return;const s=null==(l=e(n))?void 0:l.dataMask;s&&t(s)},h=(e,t,r,n,l,i)=>o=>{if(t){o.event.stop();const h=o.event.event,d=[];if(e.length>0){const t=r[o.name];e.forEach(((e,r)=>{d.push({col:e,op:"==",val:t[r],formattedVal:(0,u.mj)(t[r],{timeFormatter:(0,s.bt)(l.dateFormat),numberFormatter:(0,a.JB)(l.numberFormat),coltype:null==i?void 0:i[(0,c.Z)(e)]})})}))}t(h.clientX,h.clientY,{drillToDetail:d,crossFilter:e.length>0?n(o.name):void 0,drillBy:{filters:d,groupbyFieldName:"groupby"}})}},d=e=>{const{groupby:t,onContextMenu:r,setDataMask:n,labelMap:s,emitCrossFilters:a,selectedValues:c,coltypeMapping:u,formData:d}=e;return{click:t.length>0?o(i(c,t,s),n,a):l(),contextmenu:h(t,r,s,i(c,t,s),d,u)}}}}]);
//# sourceMappingURL=09cb0225efcda7173a9b.chunk.js.map