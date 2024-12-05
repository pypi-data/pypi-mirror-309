"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[3157],{611950:(e,t,n)=>{var r=n(564836),o=n(475263);Object.defineProperty(t,"__esModule",{value:!0}),t.default=t.HOOK_MARK=void 0;var i=o(n(667294)),a=r(n(645520));t.HOOK_MARK="RC_FORM_INTERNAL_HOOKS";var u=function(){(0,a.default)(!1,"Can not find FormContext. Please make sure you wrap Field under Form.")},l=i.createContext({getFieldValue:u,getFieldsValue:u,getFieldError:u,getFieldsError:u,isFieldsTouched:u,isFieldTouched:u,isFieldValidating:u,isFieldsValidating:u,resetFields:u,setFields:u,setFieldsValue:u,validateFields:u,submit:u,getInternalHooks:function(){return u(),{dispatch:u,initEntityValue:u,registerField:u,useSubscribe:u,setInitialValues:u,setCallbacks:u,getFields:u,setValidateMessages:u,setPreserve:u}}});t.default=l},367265:(e,t,n)=>{var r=n(475263).default;Object.defineProperty(t,"__esModule",{value:!0}),t.default=function(e,t,n){var r=o.useRef({});return"value"in r.current&&!n(r.current.condition,t)||(r.current.value=e(),r.current.condition=t),r.current.value};var o=r(n(667294))},564543:(e,t)=>{Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var n=function(e){return+setTimeout(e,16)},r=function(e){return clearTimeout(e)};"undefined"!=typeof window&&"requestAnimationFrame"in window&&(n=function(e){return window.requestAnimationFrame(e)},r=function(e){return window.cancelAnimationFrame(e)});var o=0,i=new Map;function a(e){i.delete(e)}var u=function(e){var t=o+=1;return function r(o){if(0===o)a(t),e();else{var u=n((function(){r(o-1)}));i.set(t,u)}}(arguments.length>1&&void 0!==arguments[1]?arguments[1]:1),t};u.cancel=function(e){var t=i.get(e);return a(e),r(t)},t.default=u},475531:(e,t,n)=>{var r=n(564836).default;Object.defineProperty(t,"__esModule",{value:!0}),t.useComposeRef=t.supportRef=t.supportNodeRef=t.getNodeRef=t.fillRef=t.composeRef=void 0;var o=r(n(918698)),i=n(667294),a=n(211805),u=r(n(367265)),l=t.fillRef=function(e,t){"function"==typeof e?e(t):"object"===(0,o.default)(e)&&e&&"current"in e&&(e.current=t)},s=t.composeRef=function(){for(var e=arguments.length,t=new Array(e),n=0;n<e;n++)t[n]=arguments[n];var r=t.filter(Boolean);return r.length<=1?r[0]:function(e){t.forEach((function(t){l(t,e)}))}},d=(t.useComposeRef=function(){for(var e=arguments.length,t=new Array(e),n=0;n<e;n++)t[n]=arguments[n];return(0,u.default)((function(){return s.apply(void 0,t)}),t,(function(e,t){return e.length!==t.length||e.every((function(e,n){return e!==t[n]}))}))},t.supportRef=function(e){var t,n,r=(0,a.isMemo)(e)?e.type.type:e.type;return!!("function"!=typeof r||null!==(t=r.prototype)&&void 0!==t&&t.render||r.$$typeof===a.ForwardRef)&&!!("function"!=typeof e||null!==(n=e.prototype)&&void 0!==n&&n.render||e.$$typeof===a.ForwardRef)});function f(e){return(0,i.isValidElement)(e)&&!(0,a.isFragment)(e)}t.supportNodeRef=function(e){return f(e)&&d(e)},t.getNodeRef=Number(i.version.split(".")[0])>=19?function(e){return f(e)?e.props.ref:null}:function(e){return f(e)?e.ref:null}},804591:(e,t,n)=>{n.d(t,{Z:()=>o});var r=n(897538);const o=(0,n(751995).iK)(r.Z.Item)`
  ${({theme:e})=>`\n    .ant-form-item-label {\n      padding-bottom: ${e.gridUnit}px;\n      & > label {\n        text-transform: uppercase;\n        font-size: ${e.typography.sizes.s}px;\n        color: ${e.colors.grayscale.base};\n\n        &.ant-form-item-required:not(.ant-form-item-required-mark-optional) {\n          &::before {\n            display: none;\n          }\n          &::after {\n            display: inline-block;\n            color: ${e.colors.error.base};\n            font-size: ${e.typography.sizes.s}px;\n            content: '*';\n          }\n        }\n      }\n    }\n  `}
`},281948:(e,t,n)=>{n.r(t),n.d(t,{default:()=>s});var r=n(355786),o=n(61988),i=n(667294),a=n(104715),u=n(174448),l=n(135944);function s(e){const{data:t,formData:n,height:s,width:d,setDataMask:f,setHoveredFilter:c,unsetHoveredFilter:p,setFocusedFilter:v,unsetFocusedFilter:m,setFilterActive:g,filterState:h,inputRef:F}=e,{defaultValue:y}=n,[b,w]=(0,i.useState)(null!=y?y:[]),R=(0,i.useMemo)((()=>t.reduce(((e,{duration:t,name:n})=>({...e,[t]:n})),{})),[JSON.stringify(t)]),M=e=>{const t=(0,r.Z)(e),[n]=t,o=n?R[n]:void 0,i={};n&&(i.time_grain_sqla=n),w(t),f({extraFormData:i,filterState:{label:o,value:t.length?t:null}})};(0,i.useEffect)((()=>{M(null!=y?y:[])}),[JSON.stringify(y)]),(0,i.useEffect)((()=>{var e;M(null!=(e=h.value)?e:[])}),[JSON.stringify(h.value)]);const _=0===(t||[]).length?(0,o.t)("No data"):(0,o.tn)("%s option","%s options",t.length,t.length),O={};h.validateMessage&&(O.extra=(0,l.tZ)(u.Am,{status:h.validateStatus,children:h.validateMessage}));const $=(t||[]).map((e=>{const{name:t,duration:n}=e;return{label:t,value:n}}));return(0,l.tZ)(u.un,{height:s,width:d,children:(0,l.tZ)(u.jp,{validateStatus:h.validateStatus,...O,children:(0,l.tZ)(a.Ph,{allowClear:!0,value:b,placeholder:_,onChange:M,onBlur:m,onFocus:v,onMouseEnter:c,onMouseLeave:p,ref:F,options:$,onDropdownVisibleChange:g})})})}},174448:(e,t,n)=>{n.d(t,{Am:()=>l,h2:()=>i,jp:()=>u,un:()=>a});var r=n(751995),o=n(804591);const i=0,a=r.iK.div`
  min-height: ${({height:e})=>e}px;
  width: ${({width:e})=>e===i?"100%":`${e}px`};
`,u=(0,r.iK)(o.Z)`
  &.ant-row.ant-form-item {
    margin: 0;
  }
`,l=r.iK.div`
  color: ${({theme:e,status:t="error"})=>{var n;return null==(n=e.colors[t])?void 0:n.base}};
`}}]);
//# sourceMappingURL=c1d2fbd73e9816dd585c.chunk.js.map