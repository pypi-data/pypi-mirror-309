(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[741],{260741:()=>{ace.define("ace/mode/yaml_highlight_rules",["require","exports","module","ace/lib/oop","ace/mode/text_highlight_rules"],(function(e,t,n){"use strict";var i=e("../lib/oop"),r=e("./text_highlight_rules").TextHighlightRules,o=function(){this.$rules={start:[{token:"comment",regex:"#.*$"},{token:"list.markup",regex:/^(?:-{3}|\.{3})\s*(?=#|$)/},{token:"list.markup",regex:/^\s*[\-?](?:$|\s)/},{token:"constant",regex:"!![\\w//]+"},{token:"constant.language",regex:"[&\\*][a-zA-Z0-9-_]+"},{token:["meta.tag","keyword"],regex:/^(\s*\w.*?)(:(?=\s|$))/},{token:["meta.tag","keyword"],regex:/(\w+?)(\s*:(?=\s|$))/},{token:"keyword.operator",regex:"<<\\w*:\\w*"},{token:"keyword.operator",regex:"-\\s*(?=[{])"},{token:"string",regex:'["](?:(?:\\\\.)|(?:[^"\\\\]))*?["]'},{token:"string",regex:/[|>][-+\d\s]*$/,onMatch:function(e,t,n,i){var r=/^\s*/.exec(i)[0];return n.length<1?n.push(this.next):n[0]="mlString",n.length<2?n.push(r.length):n[1]=r.length,this.token},next:"mlString"},{token:"string",regex:"['](?:(?:\\\\.)|(?:[^'\\\\]))*?[']"},{token:"constant.numeric",regex:/(\b|[+\-\.])[\d_]+(?:(?:\.[\d_]*)?(?:[eE][+\-]?[\d_]+)?)(?=[^\d-\w]|$)/},{token:"constant.numeric",regex:/[+\-]?\.inf\b|NaN\b|0x[\dA-Fa-f_]+|0b[10_]+/},{token:"constant.language.boolean",regex:"\\b(?:true|false|TRUE|FALSE|True|False|yes|no)\\b"},{token:"paren.lparen",regex:"[[({]"},{token:"paren.rparen",regex:"[\\])}]"},{token:"text",regex:/[^\s,:\[\]\{\}]+/}],mlString:[{token:"indent",regex:/^\s*$/},{token:"indent",regex:/^\s*/,onMatch:function(e,t,n){return n[1]>=e.length?(this.next="start",n.splice(0)):this.next="mlString",this.token},next:"mlString"},{token:"string",regex:".+"}]},this.normalizeRules()};i.inherits(o,r),t.YamlHighlightRules=o})),ace.define("ace/mode/matching_brace_outdent",["require","exports","module","ace/range"],(function(e,t,n){"use strict";var i=e("../range").Range,r=function(){};(function(){this.checkOutdent=function(e,t){return!!/^\s+$/.test(e)&&/^\s*\}/.test(t)},this.autoOutdent=function(e,t){var n=e.getLine(t).match(/^(\s*\})/);if(!n)return 0;var r=n[1].length,o=e.findMatchingBracket({row:t,column:r});if(!o||o.row==t)return 0;var a=this.$getIndent(e.getLine(o.row));e.replace(new i(t,0,t,r-1),a)},this.$getIndent=function(e){return e.match(/^\s*/)[0]}}).call(r.prototype),t.MatchingBraceOutdent=r})),ace.define("ace/mode/folding/coffee",["require","exports","module","ace/lib/oop","ace/mode/folding/fold_mode","ace/range"],(function(e,t,n){"use strict";var i=e("../../lib/oop"),r=e("./fold_mode").FoldMode,o=e("../../range").Range,a=t.FoldMode=function(){};i.inherits(a,r),function(){this.getFoldWidgetRange=function(e,t,n){var i=this.indentationBlock(e,n);if(i)return i;var r=/\S/,a=e.getLine(n),s=a.search(r);if(-1!=s&&"#"==a[s]){for(var g=a.length,c=e.getLength(),l=n,u=n;++n<c;){var h=(a=e.getLine(n)).search(r);if(-1!=h){if("#"!=a[h])break;u=n}}if(u>l){var d=e.getLine(u).length;return new o(l,g,u,d)}}},this.getFoldWidget=function(e,t,n){var i=e.getLine(n),r=i.search(/\S/),o=e.getLine(n+1),a=e.getLine(n-1),s=a.search(/\S/),g=o.search(/\S/);if(-1==r)return e.foldWidgets[n-1]=-1!=s&&s<g?"start":"","";if(-1==s){if(r==g&&"#"==i[r]&&"#"==o[r])return e.foldWidgets[n-1]="",e.foldWidgets[n+1]="","start"}else if(s==r&&"#"==i[r]&&"#"==a[r]&&-1==e.getLine(n-2).search(/\S/))return e.foldWidgets[n-1]="start",e.foldWidgets[n+1]="","";return e.foldWidgets[n-1]=-1!=s&&s<r?"start":"",r<g?"start":""}}.call(a.prototype)})),ace.define("ace/mode/yaml",["require","exports","module","ace/lib/oop","ace/mode/text","ace/mode/yaml_highlight_rules","ace/mode/matching_brace_outdent","ace/mode/folding/coffee"],(function(e,t,n){"use strict";var i=e("../lib/oop"),r=e("./text").Mode,o=e("./yaml_highlight_rules").YamlHighlightRules,a=e("./matching_brace_outdent").MatchingBraceOutdent,s=e("./folding/coffee").FoldMode,g=function(){this.HighlightRules=o,this.$outdent=new a,this.foldingRules=new s,this.$behaviour=this.$defaultBehaviour};i.inherits(g,r),function(){this.lineCommentStart=["#","//"],this.getNextLineIndent=function(e,t,n){var i=this.$getIndent(t);return"start"==e&&t.match(/^.*[\{\(\[]\s*$/)&&(i+=n),i},this.checkOutdent=function(e,t,n){return this.$outdent.checkOutdent(t,n)},this.autoOutdent=function(e,t,n){this.$outdent.autoOutdent(t,n)},this.$id="ace/mode/yaml"}.call(g.prototype),t.Mode=g}))}}]);
//# sourceMappingURL=0dabbacfd8bf437c4e6a.chunk.js.map