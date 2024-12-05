"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[7177],{452630:(e,t,a)=>{t.iB=t.YM=void 0;var n=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var a=arguments[t];for(var n in a)Object.prototype.hasOwnProperty.call(a,n)&&(e[n]=a[n])}return e},r=o(a(667294)),l=o(a(45697)),i=a(402371);function o(e){return e&&e.__esModule?e:{default:e}}t.YM=function(e){var t=e.itemTypeToComponent,a=e.WrapperComponent,o=void 0===a?"div":a,s=function(e){var a=e.currentPage,l=e.totalPages,s=e.boundaryPagesRange,u=e.siblingPagesRange,d=e.hideEllipsis,c=e.hidePreviousAndNextPageLinks,g=e.hideFirstAndLastPageLinks,h=e.onChange,p=e.disabled,m=function(e,t){var a={};for(var n in e)t.indexOf(n)>=0||Object.prototype.hasOwnProperty.call(e,n)&&(a[n]=e[n]);return a}(e,["currentPage","totalPages","boundaryPagesRange","siblingPagesRange","hideEllipsis","hidePreviousAndNextPageLinks","hideFirstAndLastPageLinks","onChange","disabled"]),f=(0,i.getPaginationModel)({currentPage:a,totalPages:l,boundaryPagesRange:s,siblingPagesRange:u,hideEllipsis:d,hidePreviousAndNextPageLinks:c,hideFirstAndLastPageLinks:g}),b=function(e,t,a){return function(l){var i,o,s,u=e[l.type],d=(o=(i=l).value,s=i.isDisabled,function(){!s&&a&&t!==o&&a(o)});return r.default.createElement(u,n({onClick:d},l))}}(t,a,h);return r.default.createElement(o,m,f.map((function(e){return b(n({},e,{isDisabled:!!p}))})))};return s.propTypes={currentPage:l.default.number.isRequired,totalPages:l.default.number.isRequired,boundaryPagesRange:l.default.number,siblingPagesRange:l.default.number,hideEllipsis:l.default.bool,hidePreviousAndNextPageLinks:l.default.bool,hideFirstAndLastPageLinks:l.default.bool,onChange:l.default.func,disabled:l.default.bool},s},t.iB=i.ITEM_TYPES},554070:(e,t,a)=>{a.d(t,{w:()=>o});var n=a(358593),r=a(83379),l=a(61988),i=a(135944);const o=({user:e,date:t})=>{const a=(0,i.tZ)("span",{className:"no-wrap",children:t});if(e){const t=(0,r.Z)(e),o=(0,l.t)("Modified by: %s",t);return(0,i.tZ)(n.u,{title:o,placement:"bottom",children:a})}return a}},606065:(e,t,a)=>{a.r(t),a.d(t,{default:()=>F});var n=a(751995),r=a(61988),l=a(431069),i=a(667294),o=a(419259),s=a(313322),u=a(593139),d=a(414114),c=a(358593),g=a(586074),h=a(115926),p=a.n(h),m=a(34858),f=a(211965),b=a(774069),v=a(281315),P=a(9875),E=a(784101),y=a(49238),_=a(608272);const S=[{label:(0,r.t)("Regular"),value:"Regular"},{label:(0,r.t)("Base"),value:"Base"}];var T;!function(e){e.Regular="Regular",e.Base="Base"}(T||(T={}));var L=a(135944);const w=f.iv`
  margin: 0;

  .ant-input {
    margin: 0;
  }
`,N=(0,n.iK)(b.default)`
  max-width: 1200px;
  min-width: min-content;
  width: 100%;
  .ant-modal-footer {
    white-space: nowrap;
  }
`,I=e=>f.iv`
  margin: auto ${2*e.gridUnit}px auto 0;
  color: ${e.colors.grayscale.base};
`,A=n.iK.div`
  display: flex;
  flex-direction: column;
  padding: ${({theme:e})=>`${3*e.gridUnit}px ${4*e.gridUnit}px ${2*e.gridUnit}px`};

  label,
  .control-label {
    display: inline-block;
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    color: ${({theme:e})=>e.colors.grayscale.base};
    vertical-align: middle;
  }

  .info-solid-small {
    vertical-align: middle;
    padding-bottom: ${({theme:e})=>e.gridUnit/2}px;
  }
`,R=n.iK.div`
  display: flex;
  flex-direction: column;
  margin: ${({theme:e})=>e.gridUnit}px;
  margin-bottom: ${({theme:e})=>4*e.gridUnit}px;

  .input-container {
    display: flex;
    align-items: center;

    > div {
      width: 100%;
    }
  }

  input,
  textarea {
    flex: 1 1 auto;
  }

  .required {
    margin-left: ${({theme:e})=>e.gridUnit/2}px;
    color: ${({theme:e})=>e.colors.error.base};
  }
`,k=(0,n.iK)(P.Kx)`
  resize: none;
  margin-top: ${({theme:e})=>e.gridUnit}px;
`,Z={name:"",filter_type:T.Regular,tables:[],roles:[],clause:"",group_key:"",description:""},M=function(e){const{rule:t,addDangerToast:a,addSuccessToast:n,onHide:o,show:u}=e,[d,c]=(0,i.useState)({...Z}),[g,h]=(0,i.useState)(!0),f=null!==t,{state:{loading:b,resource:P,error:M},fetchResource:x,createResource:K,updateResource:B,clearError:C}=(0,m.LE)("rowlevelsecurity",(0,r.t)("rowlevelsecurity"),a),F=(e,t)=>{c((a=>({...a,[e]:t})))},Y=(0,i.useCallback)((()=>{var e,t;if(!P)return null;const a=[],n=[];return null==(e=P.tables)||e.forEach((e=>{a.push({key:e.id,label:e.schema?`${e.schema}.${e.table_name}`:e.table_name,value:e.id})})),null==(t=P.roles)||t.forEach((e=>{n.push({key:e.id,label:e.name,value:e.id})})),{tables:a,roles:n}}),[null==P?void 0:P.tables,null==P?void 0:P.roles]);(0,i.useEffect)((()=>{f?null===(null==t?void 0:t.id)||b||M||x(t.id):c({...Z})}),[t]),(0,i.useEffect)((()=>{if(P){c({...P,id:null==t?void 0:t.id});const e=Y();F("tables",(null==e?void 0:e.tables)||[]),F("roles",(null==e?void 0:e.roles)||[])}}),[P]);const G=d||{};(0,i.useEffect)((()=>{var e;null!=d&&d.name&&null!=d&&d.clause&&null!=(e=d.tables)&&e.length?h(!1):h(!0)}),[G.name,G.clause,null==G?void 0:G.tables]);const $=e=>{F(e.name,e.value)},D=()=>{C(),c({...Z}),o()},H=(0,i.useMemo)((()=>(e="",t,a)=>{const n=p().encode({filter:e,page:t,page_size:a});return l.Z.get({endpoint:`/api/v1/rowlevelsecurity/related/tables?q=${n}`}).then((e=>({data:e.json.result.map((e=>({label:e.text,value:e.value}))),totalCount:e.json.count})))}),[]),X=(0,i.useMemo)((()=>(e="",t,a)=>{const n=p().encode({filter:e,page:t,page_size:a});return l.Z.get({endpoint:`/api/v1/rowlevelsecurity/related/roles?q=${n}`}).then((e=>({data:e.json.result.map((e=>({label:e.text,value:e.value}))),totalCount:e.json.count})))}),[]);return(0,L.tZ)(N,{className:"no-content-padding",responsive:!0,show:u,onHide:D,primaryButtonName:f?(0,r.t)("Save"):(0,r.t)("Add"),disablePrimaryButton:g,onHandledPrimaryAction:()=>{var e,t;const a=[],l=[];null==(e=d.tables)||e.forEach((e=>a.push(e.key))),null==(t=d.roles)||t.forEach((e=>l.push(e.key)));const i={...d,tables:a,roles:l};if(f&&d.id){const e=d.id;delete i.id,B(e,i).then((e=>{e&&(n("Rule updated"),D())}))}else d&&K(i).then((e=>{e&&(n((0,r.t)("Rule added")),D())}))},width:"30%",maxWidth:"1450px",title:(0,L.BX)("h4",{children:[f?(0,L.tZ)(s.Z.EditAlt,{css:I}):(0,L.tZ)(s.Z.PlusLarge,{css:I}),f?(0,r.t)("Edit Rule"):(0,r.t)("Add Rule")]}),children:(0,L.tZ)(A,{children:(0,L.BX)("div",{className:"main-section",children:[(0,L.tZ)(R,{children:(0,L.tZ)(y.QA,{id:"name",name:"name",className:"labeled-input",value:d?d.name:"",required:!0,validationMethods:{onChange:({target:e})=>$(e)},css:w,label:(0,r.t)("Rule Name"),tooltipText:(0,r.t)("The name of the rule must be unique"),hasTooltip:!0})}),(0,L.BX)(R,{children:[(0,L.BX)("div",{className:"control-label",children:[(0,r.t)("Filter Type")," ",(0,L.tZ)(_.Z,{tooltip:(0,r.t)("Regular filters add where clauses to queries if a user belongs to a role referenced in the filter, base filters apply filters to all queries except the roles defined in the filter, and can be used to define what users can see if no RLS filters within a filter group apply to them.")})]}),(0,L.tZ)("div",{className:"input-container",children:(0,L.tZ)(v.Z,{name:"filter_type",ariaLabel:(0,r.t)("Filter Type"),placeholder:(0,r.t)("Filter Type"),onChange:e=>{F("filter_type",e)},value:null==d?void 0:d.filter_type,options:S})})]}),(0,L.BX)(R,{children:[(0,L.BX)("div",{className:"control-label",children:[(0,r.t)("Datasets")," ",(0,L.tZ)("span",{className:"required",children:"*"}),(0,L.tZ)(_.Z,{tooltip:(0,r.t)("These are the datasets this filter will be applied to.")})]}),(0,L.tZ)("div",{className:"input-container",children:(0,L.tZ)(E.Z,{ariaLabel:(0,r.t)("Tables"),mode:"multiple",onChange:e=>{F("tables",e||[])},value:(null==d?void 0:d.tables)||[],options:H})})]}),(0,L.BX)(R,{children:[(0,L.BX)("div",{className:"control-label",children:[d.filter_type===T.Base?(0,r.t)("Excluded roles"):(0,r.t)("Roles")," ",(0,L.tZ)(_.Z,{tooltip:(0,r.t)("For regular filters, these are the roles this filter will be applied to. For base filters, these are the roles that the filter DOES NOT apply to, e.g. Admin if admin should see all data.")})]}),(0,L.tZ)("div",{className:"input-container",children:(0,L.tZ)(E.Z,{ariaLabel:(0,r.t)("Roles"),mode:"multiple",onChange:e=>{F("roles",e||[])},value:(null==d?void 0:d.roles)||[],options:X})})]}),(0,L.tZ)(R,{children:(0,L.tZ)(y.QA,{id:"group_key",name:"group_key",value:d?d.group_key:"",validationMethods:{onChange:({target:e})=>$(e)},css:w,label:(0,r.t)("Group Key"),hasTooltip:!0,tooltipText:(0,r.t)("Filters with the same group key will be ORed together within the group, while different filter groups will be ANDed together. Undefined group keys are treated as unique groups, i.e. are not grouped together. For example, if a table has three filters, of which two are for departments Finance and Marketing (group key = 'department'), and one refers to the region Europe (group key = 'region'), the filter clause would apply the filter (department = 'Finance' OR department = 'Marketing') AND (region = 'Europe').")})}),(0,L.tZ)(R,{children:(0,L.tZ)("div",{className:"control-label",children:(0,L.tZ)(y.QA,{id:"clause",name:"clause",value:d?d.clause:"",required:!0,validationMethods:{onChange:({target:e})=>$(e)},css:w,label:(0,r.t)("Clause"),hasTooltip:!0,tooltipText:(0,r.t)("This is the condition that will be added to the WHERE clause. For example, to only return rows for a particular client, you might define a regular filter with the clause `client_id = 9`. To display no rows unless a user belongs to a RLS filter role, a base filter can be created with the clause `1 = 0` (always false).")})})}),(0,L.BX)(R,{children:[(0,L.tZ)("div",{className:"control-label",children:(0,r.t)("Description")}),(0,L.tZ)("div",{className:"input-container",children:(0,L.tZ)(k,{rows:4,name:"description",value:d?d.description:"",onChange:e=>$(e.target)})})]})]})})})};var x=a(440768),K=a(554070),B=a(400012);const C=n.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.base};
`,F=(0,d.ZP)((function(e){const{addDangerToast:t,addSuccessToast:a,user:n}=e,[d,h]=(0,i.useState)(!1),[f,b]=(0,i.useState)(null),{state:{loading:v,resourceCount:P,resourceCollection:E,bulkSelectEnabled:y},hasPerm:_,fetchData:S,refreshData:T,toggleBulkSelect:w}=(0,m.Yi)("rowlevelsecurity",(0,r.t)("Row Level Security"),t,!0,void 0,void 0,!0);function N(e){b(e),h(!0)}function I(){b(null),h(!1),T()}const A=_("can_write"),R=_("can_write"),k=_("can_export"),Z=(0,i.useMemo)((()=>[{accessor:"name",Header:(0,r.t)("Name")},{accessor:"filter_type",Header:(0,r.t)("Filter Type"),size:"xl"},{accessor:"group_key",Header:(0,r.t)("Group Key"),size:"xl"},{accessor:"clause",Header:(0,r.t)("Clause")},{Cell:({row:{original:{changed_on_delta_humanized:e,changed_by:t}}})=>(0,L.tZ)(K.w,{date:e,user:t}),Header:(0,r.t)("Last modified"),accessor:"changed_on_delta_humanized",size:"xl"},{Cell:({row:{original:e}})=>(0,L.BX)(C,{className:"actions",children:[A&&(0,L.tZ)(o.Z,{title:(0,r.t)("Please confirm"),description:(0,L.BX)(L.HY,{children:[(0,r.t)("Are you sure you want to delete")," ",(0,L.tZ)("b",{children:e.name})]}),onConfirm:()=>function({id:e,name:t},a,n,i){return l.Z.delete({endpoint:`/api/v1/rowlevelsecurity/${e}`}).then((()=>{a(),n((0,r.t)("Deleted %s",t))}),(0,x.v$)((e=>i((0,r.t)("There was an issue deleting %s: %s",t,e)))))}(e,T,a,t),children:e=>(0,L.tZ)(c.u,{id:"delete-action-tooltip",title:(0,r.t)("Delete"),placement:"bottom",children:(0,L.tZ)("span",{role:"button",tabIndex:0,className:"action-button",onClick:e,children:(0,L.tZ)(s.Z.Trash,{})})})}),R&&(0,L.tZ)(c.u,{id:"edit-action-tooltip",title:(0,r.t)("Edit"),placement:"bottom",children:(0,L.tZ)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>N(e),children:(0,L.tZ)(s.Z.EditAlt,{})})})]}),Header:(0,r.t)("Actions"),id:"actions",hidden:!R&&!A&&!k,disableSortBy:!0},{accessor:B.J.ChangedBy,hidden:!0}]),[n.userId,R,A,k,_,T,t,a]),F={title:(0,r.t)("No Rules yet"),image:"filter-results.svg",buttonAction:()=>N(null),buttonText:R?(0,L.BX)(L.HY,{children:[(0,L.tZ)("i",{className:"fa fa-plus"})," ","Rule"," "]}):null},Y=(0,i.useMemo)((()=>[{Header:(0,r.t)("Name"),key:"search",id:"name",input:"search",operator:u.p.StartsWith},{Header:(0,r.t)("Filter Type"),key:"filter_type",id:"filter_type",input:"select",operator:u.p.Equals,unfilteredLabel:(0,r.t)("Any"),selects:[{label:(0,r.t)("Regular"),value:"Regular"},{label:(0,r.t)("Base"),value:"Base"}]},{Header:(0,r.t)("Group Key"),key:"search",id:"group_key",input:"search",operator:u.p.StartsWith},{Header:(0,r.t)("Modified by"),key:"changed_by",id:"changed_by",input:"select",operator:u.p.RelationOneMany,unfilteredLabel:(0,r.t)("All"),fetchSelects:(0,x.tm)("rowlevelsecurity","changed_by",(0,x.v$)((e=>(0,r.t)("An error occurred while fetching dataset datasource values: %s",e))),n),paginate:!0}]),[n]),G=[{id:"changed_on_delta_humanized",desc:!0}],$=[];return A&&($.push({name:(0,L.BX)(L.HY,{children:[(0,L.tZ)("i",{className:"fa fa-plus"})," ",(0,r.t)("Rule")]}),buttonStyle:"primary",onClick:()=>N(null)}),$.push({name:(0,r.t)("Bulk select"),buttonStyle:"secondary",onClick:w})),(0,L.BX)(L.HY,{children:[(0,L.tZ)(g.Z,{name:(0,r.t)("Row Level Security"),buttons:$}),(0,L.tZ)(o.Z,{title:(0,r.t)("Please confirm"),description:(0,r.t)("Are you sure you want to delete the selected rules?"),onConfirm:function(e){const n=e.map((({id:e})=>e));return l.Z.delete({endpoint:`/api/v1/rowlevelsecurity/?q=${p().encode(n)}`}).then((()=>{T(),a((0,r.t)("Deleted"))}),(0,x.v$)((e=>t((0,r.t)("There was an issue deleting rules: %s",e)))))},children:e=>{const n=[];return A&&n.push({key:"delete",name:(0,r.t)("Delete"),type:"danger",onSelect:e}),(0,L.BX)(L.HY,{children:[(0,L.tZ)(M,{rule:f,addDangerToast:t,onHide:I,addSuccessToast:a,show:d}),(0,L.tZ)(u.Z,{className:"rls-list-view",bulkActions:n,bulkSelectEnabled:y,disableBulkSelect:w,columns:Z,count:P,data:E,emptyState:F,fetchData:S,filters:Y,initialSort:G,loading:v,addDangerToast:t,addSuccessToast:a,refreshData:()=>{},pageSize:25})]})}})]})}))},656590:(e,t)=>{t.ITEM_TYPES={PAGE:"PAGE",ELLIPSIS:"ELLIPSIS",FIRST_PAGE_LINK:"FIRST_PAGE_LINK",PREVIOUS_PAGE_LINK:"PREVIOUS_PAGE_LINK",NEXT_PAGE_LINK:"NEXT_PAGE_LINK",LAST_PAGE_LINK:"LAST_PAGE_LINK"},t.ITEM_KEYS={FIRST_ELLIPSIS:-1,SECOND_ELLIPSIS:-2,FIRST_PAGE_LINK:-3,PREVIOUS_PAGE_LINK:-4,NEXT_PAGE_LINK:-5,LAST_PAGE_LINK:-6}},653804:(e,t,a)=>{var n=a(656590);t.createFirstEllipsis=function(e){return{type:n.ITEM_TYPES.ELLIPSIS,key:n.ITEM_KEYS.FIRST_ELLIPSIS,value:e,isActive:!1}},t.createSecondEllipsis=function(e){return{type:n.ITEM_TYPES.ELLIPSIS,key:n.ITEM_KEYS.SECOND_ELLIPSIS,value:e,isActive:!1}},t.createFirstPageLink=function(e){var t=e.currentPage;return{type:n.ITEM_TYPES.FIRST_PAGE_LINK,key:n.ITEM_KEYS.FIRST_PAGE_LINK,value:1,isActive:1===t}},t.createPreviousPageLink=function(e){var t=e.currentPage;return{type:n.ITEM_TYPES.PREVIOUS_PAGE_LINK,key:n.ITEM_KEYS.PREVIOUS_PAGE_LINK,value:Math.max(1,t-1),isActive:1===t}},t.createNextPageLink=function(e){var t=e.currentPage,a=e.totalPages;return{type:n.ITEM_TYPES.NEXT_PAGE_LINK,key:n.ITEM_KEYS.NEXT_PAGE_LINK,value:Math.min(a,t+1),isActive:t===a}},t.createLastPageLink=function(e){var t=e.currentPage,a=e.totalPages;return{type:n.ITEM_TYPES.LAST_PAGE_LINK,key:n.ITEM_KEYS.LAST_PAGE_LINK,value:a,isActive:t===a}},t.createPageFunctionFactory=function(e){var t=e.currentPage;return function(e){return{type:n.ITEM_TYPES.PAGE,key:e,value:e,isActive:e===t}}}},1158:(e,t)=>{t.createRange=function(e,t){for(var a=[],n=e;n<=t;n++)a.push(n);return a}},402371:(e,t,a)=>{var n=a(1158),r=a(653804);t.getPaginationModel=function(e){if(null==e)throw new Error("getPaginationModel(): options object should be a passed");var t=Number(e.totalPages);if(isNaN(t))throw new Error("getPaginationModel(): totalPages should be a number");if(t<0)throw new Error("getPaginationModel(): totalPages shouldn't be a negative number");var a=Number(e.currentPage);if(isNaN(a))throw new Error("getPaginationModel(): currentPage should be a number");if(a<0)throw new Error("getPaginationModel(): currentPage shouldn't be a negative number");if(a>t)throw new Error("getPaginationModel(): currentPage shouldn't be greater than totalPages");var l=null==e.boundaryPagesRange?1:Number(e.boundaryPagesRange);if(isNaN(l))throw new Error("getPaginationModel(): boundaryPagesRange should be a number");if(l<0)throw new Error("getPaginationModel(): boundaryPagesRange shouldn't be a negative number");var i=null==e.siblingPagesRange?1:Number(e.siblingPagesRange);if(isNaN(i))throw new Error("getPaginationModel(): siblingPagesRange should be a number");if(i<0)throw new Error("getPaginationModel(): siblingPagesRange shouldn't be a negative number");var o=Boolean(e.hidePreviousAndNextPageLinks),s=Boolean(e.hideFirstAndLastPageLinks),u=Boolean(e.hideEllipsis),d=u?0:1,c=[],g=r.createPageFunctionFactory(e);if(s||c.push(r.createFirstPageLink(e)),o||c.push(r.createPreviousPageLink(e)),1+2*d+2*i+2*l>=t){var h=n.createRange(1,t).map(g);c.push.apply(c,h)}else{var p=l,m=n.createRange(1,p).map(g),f=t+1-l,b=t,v=n.createRange(f,b).map(g),P=Math.min(Math.max(a-i,p+d+1),f-d-2*i-1),E=P+2*i,y=n.createRange(P,E).map(g);if(c.push.apply(c,m),!u){var _=P-1,S=(_===p+1?g:r.createFirstEllipsis)(_);c.push(S)}if(c.push.apply(c,y),!u){var T=E+1,L=(T===f-1?g:r.createSecondEllipsis)(T);c.push(L)}c.push.apply(c,v)}return o||c.push(r.createNextPageLink(e)),s||c.push(r.createLastPageLink(e)),c};var l=a(656590);t.ITEM_TYPES=l.ITEM_TYPES,t.ITEM_KEYS=l.ITEM_KEYS}}]);
//# sourceMappingURL=057a359ab00c3e623a19.chunk.js.map