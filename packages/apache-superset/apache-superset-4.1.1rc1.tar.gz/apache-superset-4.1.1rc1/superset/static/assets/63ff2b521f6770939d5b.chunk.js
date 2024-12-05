"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[3197],{493197:(e,t,n)=>{n.d(t,{tR:()=>R,iZ:()=>D,iA:()=>I,ex:()=>E,ZP:()=>Z});var l=n(667294),o=n(202307),i=n(731929),r=n(751995),s=n(61988),a=n(68492),d=n(838703);const c=(e,t,n)=>{let l=!1;const o=t-e;return o>0&&o<=n&&(l=!0),l};class u{constructor(e,t,n){this.tableRef=void 0,this.columnRef=void 0,this.setDerivedColumns=void 0,this.isDragging=void 0,this.resizable=void 0,this.reorderable=void 0,this.derivedColumns=void 0,this.RESIZE_INDICATOR_THRESHOLD=void 0,this.clearListeners=()=>{document.removeEventListener("mouseup",this.handleMouseup),this.initializeResizableColumns(!1,this.tableRef),this.initializeDragDropColumns(!1,this.tableRef)},this.setTableRef=e=>{this.tableRef=e},this.getColumnIndex=()=>{var e;let t=-1;const n=null==(e=this.columnRef)?void 0:e.parentNode;return n&&(t=Array.prototype.indexOf.call(n.children,this.columnRef)),t},this.handleColumnDragStart=e=>{var t;const n=null==e?void 0:e.currentTarget;n&&(this.columnRef=n),this.isDragging=!0;const l=this.getColumnIndex(),o={index:l,columnData:this.derivedColumns[l]};null==e||null==(t=e.dataTransfer)||t.setData(D,JSON.stringify(o))},this.handleDragDrop=e=>{var t;if(null==(t=e.dataTransfer)||null==t.getData?void 0:t.getData(D)){var n;e.preventDefault();const t=null==(n=e.currentTarget)?void 0:n.parentNode,l=Array.prototype.indexOf.call(t.children,e.currentTarget),o=this.getColumnIndex(),i=[...this.derivedColumns],r=i.slice(o,o+1);i.splice(o,1),i.splice(l,0,r[0]),this.derivedColumns=[...i],this.setDerivedColumns(i)}},this.allowDrop=e=>{e.preventDefault()},this.handleMouseDown=e=>{const t=null==e?void 0:e.currentTarget;t&&(this.columnRef=t,e&&c(e.offsetX,t.offsetWidth,this.RESIZE_INDICATOR_THRESHOLD)?(t.mouseDown=!0,t.oldX=e.x,t.oldWidth=t.offsetWidth,t.draggable=!1):this.reorderable&&(t.draggable=!0))},this.handleMouseMove=e=>{if(!0===this.resizable&&!this.isDragging){const t=e.currentTarget;e&&c(e.offsetX,t.offsetWidth,this.RESIZE_INDICATOR_THRESHOLD)?t.style.cursor="col-resize":t.style.cursor="default";const n=this.columnRef;if(null!=n&&n.mouseDown){let t=n.oldWidth;const l=e.x-n.oldX;n.oldWidth+(e.x-n.oldX)>0&&(t=n.oldWidth+l);const o=this.getColumnIndex();if(!Number.isNaN(o)){const e={...this.derivedColumns[o]};e.width=t,this.derivedColumns[o]=e,this.setDerivedColumns([...this.derivedColumns])}}}},this.handleMouseup=()=>{this.columnRef&&(this.columnRef.mouseDown=!1,this.columnRef.style.cursor="default",this.columnRef.draggable=!1),this.isDragging=!1},this.initializeResizableColumns=(e=!1,t)=>{var n,l;this.tableRef=t;const o=null==(n=this.tableRef)||null==(l=n.rows)?void 0:l[0];if(o){const{cells:t}=o,n=t.length;for(let l=0;l<n;l+=1){const n=t[l];!0===e?(this.resizable=!0,n.addEventListener("mousedown",this.handleMouseDown),n.addEventListener("mousemove",this.handleMouseMove,!0)):(this.resizable=!1,n.removeEventListener("mousedown",this.handleMouseDown),n.removeEventListener("mousemove",this.handleMouseMove,!0))}}},this.initializeDragDropColumns=(e=!1,t)=>{var n,l;this.tableRef=t;const o=null==(n=this.tableRef)||null==(l=n.rows)?void 0:l[0];if(o){const{cells:t}=o,n=t.length;for(let l=0;l<n;l+=1){const n=t[l];!0===e?(this.reorderable=!0,n.addEventListener("mousedown",this.handleMouseDown),n.addEventListener("dragover",this.allowDrop),n.addEventListener("dragstart",this.handleColumnDragStart),n.addEventListener("drop",this.handleDragDrop)):(this.reorderable=!1,n.draggable=!1,n.removeEventListener("mousedown",this.handleMouseDown),n.removeEventListener("dragover",this.allowDrop),n.removeEventListener("dragstart",this.handleColumnDragStart),n.removeEventListener("drop",this.handleDragDrop))}}},this.setDerivedColumns=n,this.tableRef=e,this.isDragging=!1,this.RESIZE_INDICATOR_THRESHOLD=8,this.resizable=!1,this.reorderable=!1,this.derivedColumns=[...t],document.addEventListener("mouseup",this.handleMouseup)}}var h=n(693967),g=n.n(h),f=n(899612),p=n(274061),m=n(332103),v=n(135944);const b=(0,r.iK)("div")((({theme:e,height:t})=>`\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n  padding-left: ${2*e.gridUnit}px;\n  padding-right: ${e.gridUnit}px;\n  border-bottom: 1px solid ${e.colors.grayscale.light3};\n  transition: background 0.3s;\n  line-height: ${t}px;\n  box-sizing: border-box;\n`)),w=(0,r.iK)(o.Z)((({theme:e})=>`\n    th.ant-table-cell {\n      font-weight: ${e.typography.weights.bold};\n      color: ${e.colors.grayscale.dark1};\n      user-select: none;\n      white-space: nowrap;\n      overflow: hidden;\n      text-overflow: ellipsis;\n    }\n\n    .ant-pagination-item-active {\n      border-color: ${e.colors.primary.base};\n      }\n    }\n    .ant-table.ant-table-small {\n      font-size: ${e.typography.sizes.s}px;\n    }\n`)),D="superset/table-column";var C,R,E;!function(e){e.Disabled="disabled",e.Single="single",e.Multi="multi"}(C||(C={})),function(e){e.Paginate="paginate",e.Sort="sort",e.Filter="filter"}(R||(R={})),function(e){e.Small="small",e.Middle="middle"}(E||(E={}));const y=[],S=40,x=68,T=(0,r.iK)(o.Z)((({theme:e,height:t})=>`\n    .ant-table-body {\n      overflow: auto;\n      height: ${t?`${t}px`:void 0};\n    }\n\n    th.ant-table-cell {\n      font-weight: ${e.typography.weights.bold};\n      color: ${e.colors.grayscale.dark1};\n      user-select: none;\n      white-space: nowrap;\n      overflow: hidden;\n      text-overflow: ellipsis;\n    }\n\n    .ant-table-tbody > tr > td {\n      user-select: none;\n      white-space: nowrap;\n      overflow: hidden;\n      text-overflow: ellipsis;\n      border-bottom: 1px solid ${e.colors.grayscale.light3};\n    }\n\n    .ant-pagination-item-active {\n      border-color: ${e.colors.primary.base};\n    }\n\n    .ant-table.ant-table-small {\n      font-size: ${e.typography.sizes.s}px;\n    }\n  `)),z=(0,r.iK)((e=>{var t;const{columns:n,pagination:o,onChange:i,height:s,scroll:a,size:d,allowHTML:c=!1}=e,[u,h]=(0,l.useState)(0),D=(0,l.useCallback)((e=>{h(e)}),[]),{ref:C}=(0,f.NB)({onResize:D}),y=(0,r.Fg)(),S=37*(null==y?void 0:y.gridUnit)||150,x=n.filter((({width:e})=>!e)).length;let T=0;null==n||n.forEach((e=>{e.width&&(T+=e.width)}));let z=0;const L=Math.max(Math.floor((u-T)/x),50),M=null!=(t=null==n||null==n.map?void 0:n.map((e=>{const t={...e};return e.width||(t.width=L),z+=t.width,t})))?t:[];if(z<u){const e=M[M.length-1];e.width=e.width+Math.floor(u-z)}const N=(0,l.useRef)(),[I]=(0,l.useState)((()=>{const e={};return Object.defineProperty(e,"scrollLeft",{get:()=>{var e,t;return N.current?null==(e=N.current)||null==(t=e.state)?void 0:t.scrollLeft:null},set:e=>{N.current&&N.current.scrollTo({scrollLeft:e})}}),e})),Z=()=>{var e;null==(e=N.current)||e.resetAfterIndices({columnIndex:0,shouldForceUpdate:!0})};(0,l.useEffect)((()=>Z),[u,n,d]);const O={...o,onChange:(e,t)=>{var n;null==(n=N.current)||null==n.scrollTo||n.scrollTo({scrollTop:0}),null==i||i({...o,current:e,pageSize:t},{},{},{action:R.Paginate,currentDataSource:[]})}};return(0,v.tZ)("div",{ref:C,children:(0,v.tZ)(w,{...e,sticky:!1,className:"virtual-table",columns:M,components:{body:(e,{ref:t,onScroll:n})=>{t.current=I;const l=d===E.Middle?47:39;return(0,v.tZ)(p.cd,{ref:N,className:"virtual-grid",columnCount:M.length,columnWidth:e=>{const{width:t=S}=M[e];return t},height:s||a.y,rowCount:e.length,rowHeight:()=>l,width:u,onScroll:({scrollLeft:e})=>{n({scrollLeft:e})},children:({columnIndex:t,rowIndex:n,style:o})=>{var i,r;const s=null==e?void 0:e[n];let a=null==s?void 0:s[null==M||null==(i=M[t])?void 0:i.dataIndex];const d=null==(r=M[t])?void 0:r.render;return"function"==typeof d&&(a=d(a,s,n)),c&&"string"==typeof a&&(a=(0,m.Ul)(a)),(0,v.tZ)(b,{className:g()("virtual-table-cell",{"virtual-table-cell-last":t===M.length-1}),style:o,title:"string"==typeof a?a:void 0,theme:y,height:l,children:a})}})}},pagination:!!o&&O})})}))((({theme:e})=>`\n  .virtual-table .ant-table-container:before,\n  .virtual-table .ant-table-container:after {\n    display: none;\n  }\n  .virtual-table-cell {\n    box-sizing: border-box;\n    padding: ${4*e.gridUnit}px;\n    white-space: nowrap;\n    overflow: hidden;\n    text-overflow: ellipsis;\n  }\n`)),L={filterTitle:(0,s.t)("Filter menu"),filterConfirm:(0,s.t)("OK"),filterReset:(0,s.t)("Reset"),filterEmptyText:(0,s.t)("No filters"),filterCheckall:(0,s.t)("Select all items"),filterSearchPlaceholder:(0,s.t)("Search in filters"),emptyText:(0,s.t)("No data"),selectAll:(0,s.t)("Select current page"),selectInvert:(0,s.t)("Invert current page"),selectNone:(0,s.t)("Clear all data"),selectionAll:(0,s.t)("Select all data"),sortTitle:(0,s.t)("Sort"),expand:(0,s.t)("Expand row"),collapse:(0,s.t)("Collapse row"),triggerDesc:(0,s.t)("Click to sort descending"),triggerAsc:(0,s.t)("Click to sort ascending"),cancelSort:(0,s.t)("Click to cancel sorting")},M={},N=()=>{};function I(e){const{data:t,bordered:n,columns:o,selectedRows:s=y,handleRowSelection:c,size:h=E.Small,selectionType:g=C.Disabled,sticky:f=!0,loading:p=!1,resizable:m=!1,reorderable:b=!1,usePagination:w=!0,defaultPageSize:D=15,pageSizeOptions:R=["5","15","25","50","100"],hideData:I=!1,emptyComponent:Z,locale:O,height:A,virtualize:k=!1,onChange:$=N,recordCount:H,onRow:P,allowHTML:U=!1,childrenColumnName:W}=e,X=(0,l.useRef)(null),[_,F]=(0,l.useState)(o),[K,B]=(0,l.useState)(D),[j,J]=(0,l.useState)({...L}),[q,G]=(0,l.useState)(s),Q=(0,l.useRef)(null),V=M[g],Y={type:V,selectedRowKeys:q,onChange:e=>{G(e),null==c||c(e)}};(0,l.useEffect)((()=>{!0===b&&a.Z.warn('EXPERIMENTAL FEATURE ENABLED: The "reorderable" prop of Table is experimental and NOT recommended for use in production deployments.'),!0===m&&a.Z.warn('EXPERIMENTAL FEATURE ENABLED: The "resizable" prop of Table is experimental and NOT recommended for use in production deployments.')}),[b,m]),(0,l.useEffect)((()=>{let e;e=O?{...L,...O}:{...L},J(e)}),[O]),(0,l.useEffect)((()=>F(o)),[o]),(0,l.useEffect)((()=>{var e,t;Q.current&&(null==(t=Q.current)||t.clearListeners());const n=null==(e=X.current)?void 0:e.getElementsByTagName("table")[0];var l,o;n&&(Q.current=new u(n,_,F),b&&(null==Q||null==(l=Q.current)||l.initializeDragDropColumns(b,n)),m&&(null==Q||null==(o=Q.current)||o.initializeResizableColumns(m,n)));return()=>{var e;null==Q||null==(e=Q.current)||null==e.clearListeners||e.clearListeners()}}),[X,b,m,k,Q]);const ee=(0,r.Fg)(),te=!!w&&{hideOnSinglePage:!0,pageSize:K,pageSizeOptions:R,onShowSizeChange:(e,t)=>B(t)};te&&H&&(te.total=H);let ne=A;ne&&(ne-=x,w&&H&&H>K&&(ne-=S));const le={loading:{spinning:null!=p&&p,indicator:(0,v.tZ)(d.Z,{})},hasData:!I&&t,columns:_,dataSource:I?void 0:t,size:h,pagination:te,locale:j,showSorterTooltip:!1,onChange:$,onRow:P,theme:ee,height:ne,bordered:n,expandable:{childrenColumnName:W}};return(0,v.tZ)(i.default,{renderEmpty:()=>null!=Z?Z:(0,v.tZ)("div",{children:j.emptyText}),children:(0,v.BX)("div",{ref:X,children:[!k&&(0,v.tZ)(T,{...le,rowSelection:V?Y:void 0,sticky:f}),k&&(0,v.tZ)(z,{...le,scroll:{y:300,x:"100vw",...!1},allowHTML:U})]})})}M[C.Multi]="checkbox",M[C.Single]="radio",M[C.Disabled]=null;const Z=I}}]);
//# sourceMappingURL=63ff2b521f6770939d5b.chunk.js.map