"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[5264],{15264:(e,t,r)=>{r.r(t),r.d(t,{default:()=>f});var s=r(943323),a=r(751995),n=r(45697),o=r.n(n),i=r(615078),c=r.n(i),d=r(767190),p=r(328062);const l={data:o().shape({matrix:o().arrayOf(o().arrayOf(o().number)),nodes:o().arrayOf(o().string)}),width:o().number,height:o().number,colorScheme:o().string,numberFormat:o().string};function h(e,t){const{data:r,width:s,height:a,numberFormat:n,colorScheme:o,sliceId:i}=t;e.innerHTML="";const l=c().select(e);l.classed("superset-legacy-chart-chord",!0);const{nodes:h,matrix:u}=r,g=(0,d.JB)(n),m=p.getScale(o),y=Math.min(s,a)/2-10,f=y-24;let v;const x=c().svg.arc().innerRadius(f).outerRadius(y),$=c().layout.chord().padding(.04).sortSubgroups(c().descending).sortChords(c().descending),b=c().svg.chord().radius(f),T=l.append("svg").attr("width",s).attr("height",a).on("mouseout",(()=>v.classed("fade",!1))).append("g").attr("id","circle").attr("transform",`translate(${s/2}, ${a/2})`);T.append("circle").attr("r",y),$.matrix(u);const C=T.selectAll(".group").data($.groups).enter().append("g").attr("class","group").on("mouseover",((e,t)=>{v.classed("fade",(e=>e.source.index!==t&&e.target.index!==t))}));C.append("title").text(((e,t)=>`${h[t]}: ${g(e.value)}`));const N=C.append("path").attr("id",((e,t)=>`group${t}`)).attr("d",x).style("fill",((e,t)=>m(h[t],i,o))),k=C.append("text").attr("x",6).attr("dy",15);k.append("textPath").attr("xlink:href",((e,t)=>`#group${t}`)).text(((e,t)=>h[t])),k.filter((function(e,t){return N[0][t].getTotalLength()/2-16<this.getComputedTextLength()})).remove(),v=T.selectAll(".chord").data($.chords).enter().append("path").attr("class","chord").on("mouseover",(e=>{v.classed("fade",(t=>t!==e))})).style("fill",(e=>m(h[e.source.index],i,o))).attr("d",b),v.append("title").text((e=>`${h[e.source.index]} → ${h[e.target.index]}: ${g(e.target.value)}\n${h[e.target.index]} → ${h[e.source.index]}: ${g(e.source.value)}`))}h.displayName="Chord",h.propTypes=l;const u=h;var g=r(135944);const m=(0,s.Z)(u),y=({className:e,...t})=>(0,g.tZ)("div",{className:e,children:(0,g.tZ)(m,{...t})});y.defaultProps={otherProps:{}},y.propTypes={className:o().string.isRequired,otherProps:o().objectOf(o().any)};const f=(0,a.iK)(y)`
  ${({theme:e})=>`\n    .superset-legacy-chart-chord svg #circle circle {\n      fill: none;\n      pointer-events: all;\n    }\n    .superset-legacy-chart-chord svg .group path {\n      fill-opacity: ${e.opacity.mediumHeavy};\n    }\n    .superset-legacy-chart-chord svg path.chord {\n      stroke: ${e.colors.grayscale.dark2};\n      stroke-width: 0.25px;\n    }\n    .superset-legacy-chart-chord svg #circle:hover path.fade {\n      opacity:  ${e.opacity.light};\n    }\n  `}
`},943323:(e,t,r)=>{r.d(t,{Z:()=>n});var s=r(667294),a=r(135944);function n(e,t){class r extends s.Component{constructor(e){super(e),this.container=void 0,this.setContainerRef=this.setContainerRef.bind(this)}componentDidMount(){this.execute()}componentDidUpdate(){this.execute()}componentWillUnmount(){this.container=void 0,null!=t&&t.componentWillUnmount&&t.componentWillUnmount.bind(this)()}setContainerRef(e){this.container=e}execute(){this.container&&e(this.container,this.props)}render(){const{id:e,className:t}=this.props;return(0,a.tZ)("div",{ref:this.setContainerRef,id:e,className:t})}}const n=r;return e.displayName&&(n.displayName=e.displayName),e.propTypes&&(n.propTypes={...n.propTypes,...e.propTypes}),e.defaultProps&&(n.defaultProps=e.defaultProps),r}}}]);
//# sourceMappingURL=6e5fda68128eaaa76fe2.chunk.js.map