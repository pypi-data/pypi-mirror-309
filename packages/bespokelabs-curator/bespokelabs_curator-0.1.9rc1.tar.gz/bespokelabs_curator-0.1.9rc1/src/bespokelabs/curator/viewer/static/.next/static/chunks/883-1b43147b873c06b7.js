"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[883],{89669:(e,t,s)=>{s.d(t,{h:()=>u});var a=s(57437),r=s(50495),o=s(3274),n=s(92699),l=s(38296),i=s(66648),d=s(16463),c=s(2265);function u(e){let{isLoading:t,isPolling:s,onTogglePolling:u,showPolling:m=!0,loadingText:p="Loading dataset...",pollingText:f="Polling for updates..."}=e,x=(0,d.useRouter)(),[g,h]=(0,c.useState)("light"),[v,b]=(0,c.useState)(!1);return((0,c.useEffect)(()=>{let e=window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";h(localStorage.getItem("theme")||e),b(!0)},[]),(0,c.useEffect)(()=>{v&&("dark"===g?document.documentElement.classList.add("dark"):document.documentElement.classList.remove("dark"),localStorage.setItem("theme",g))},[g,v]),v)?(0,a.jsx)("header",{className:"border-b sticky top-0 z-50 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/75",children:(0,a.jsxs)("div",{className:"container mx-auto px-4 py-4 flex items-center justify-between",children:[(0,a.jsxs)("div",{className:"flex items-center gap-2 cursor-pointer",onClick:()=>x.push("/"),children:[(0,a.jsx)(i.default,{src:"/Bespoke-Labs-Logomark-Red-on-Mint.svg",alt:"Bespoke Logo",width:32,height:32,className:"object-contain"}),(0,a.jsx)("h1",{className:"text-2xl font-bold",children:"Bespoke Dataset Viewer"})]}),(0,a.jsxs)("div",{className:"flex items-center gap-4",children:[t?(0,a.jsxs)("div",{className:"flex items-center gap-2 text-sm text-muted-foreground",children:[(0,a.jsx)(o.Z,{className:"h-4 w-4 animate-spin"}),(0,a.jsx)("span",{children:p})]}):s&&m?(0,a.jsxs)("div",{className:"flex items-center gap-2 text-sm text-muted-foreground",children:[(0,a.jsx)(o.Z,{className:"h-4 w-4 animate-spin"}),(0,a.jsx)("span",{children:f})]}):null,m&&u&&(0,a.jsxs)(r.z,{variant:"outline",size:"sm",onClick:u,disabled:t,children:[s?"Stop":"Start"," Updates"]}),(0,a.jsxs)(r.z,{variant:"ghost",size:"icon",onClick:()=>{h(e=>"light"===e?"dark":"light")},children:["light"===g?(0,a.jsx)(n.Z,{className:"h-5 w-5"}):(0,a.jsx)(l.Z,{className:"h-5 w-5"}),(0,a.jsx)("span",{className:"sr-only",children:"Toggle theme"})]})]})]})}):null}},50495:(e,t,s)=>{s.d(t,{d:()=>i,z:()=>d});var a=s(57437),r=s(2265),o=s(71538),n=s(12218),l=s(37440);let i=(0,n.j)("inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",{variants:{variant:{default:"bg-primary text-primary-foreground hover:bg-primary/90",destructive:"bg-destructive text-destructive-foreground hover:bg-destructive/90",outline:"border border-input bg-background hover:bg-accent hover:text-accent-foreground",secondary:"bg-secondary text-secondary-foreground hover:bg-secondary/80",ghost:"hover:bg-accent hover:text-accent-foreground",link:"text-primary underline-offset-4 hover:underline"},size:{default:"h-10 px-4 py-2",sm:"h-9 rounded-md px-3",lg:"h-11 rounded-md px-8",icon:"h-10 w-10"}},defaultVariants:{variant:"default",size:"default"}}),d=r.forwardRef((e,t)=>{let{className:s,variant:r,size:n,asChild:d=!1,...c}=e,u=d?o.g7:"button";return(0,a.jsx)(u,{className:(0,l.cn)(i({variant:r,size:n,className:s})),ref:t,...c})});d.displayName="Button"},46910:(e,t,s)=>{s.d(t,{$F:()=>u,AW:()=>m,Xi:()=>p,h_:()=>c});var a=s(57437),r=s(2265),o=s(64247),n=s(87592),l=s(22468),i=s(28165),d=s(37440);let c=o.fC,u=o.xz;o.ZA,o.Uv,o.Tr,o.Ee,r.forwardRef((e,t)=>{let{className:s,inset:r,children:l,...i}=e;return(0,a.jsxs)(o.fF,{ref:t,className:(0,d.cn)("flex cursor-default gap-2 select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none focus:bg-accent data-[state=open]:bg-accent [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",r&&"pl-8",s),...i,children:[l,(0,a.jsx)(n.Z,{className:"ml-auto"})]})}).displayName=o.fF.displayName,r.forwardRef((e,t)=>{let{className:s,...r}=e;return(0,a.jsx)(o.tu,{ref:t,className:(0,d.cn)("z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-lg data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",s),...r})}).displayName=o.tu.displayName;let m=r.forwardRef((e,t)=>{let{className:s,sideOffset:r=4,...n}=e;return(0,a.jsx)(o.Uv,{children:(0,a.jsx)(o.VY,{ref:t,sideOffset:r,className:(0,d.cn)("z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",s),...n})})});m.displayName=o.VY.displayName;let p=r.forwardRef((e,t)=>{let{className:s,inset:r,...n}=e;return(0,a.jsx)(o.ck,{ref:t,className:(0,d.cn)("relative flex cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",r&&"pl-8",s),...n})});p.displayName=o.ck.displayName,r.forwardRef((e,t)=>{let{className:s,children:r,checked:n,...i}=e;return(0,a.jsxs)(o.oC,{ref:t,className:(0,d.cn)("relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",s),checked:n,...i,children:[(0,a.jsx)("span",{className:"absolute left-2 flex h-3.5 w-3.5 items-center justify-center",children:(0,a.jsx)(o.wU,{children:(0,a.jsx)(l.Z,{className:"h-4 w-4"})})}),r]})}).displayName=o.oC.displayName,r.forwardRef((e,t)=>{let{className:s,children:r,...n}=e;return(0,a.jsxs)(o.Rk,{ref:t,className:(0,d.cn)("relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",s),...n,children:[(0,a.jsx)("span",{className:"absolute left-2 flex h-3.5 w-3.5 items-center justify-center",children:(0,a.jsx)(o.wU,{children:(0,a.jsx)(i.Z,{className:"h-2 w-2 fill-current"})})}),r]})}).displayName=o.Rk.displayName,r.forwardRef((e,t)=>{let{className:s,inset:r,...n}=e;return(0,a.jsx)(o.__,{ref:t,className:(0,d.cn)("px-2 py-1.5 text-sm font-semibold",r&&"pl-8",s),...n})}).displayName=o.__.displayName,r.forwardRef((e,t)=>{let{className:s,...r}=e;return(0,a.jsx)(o.Z0,{ref:t,className:(0,d.cn)("-mx-1 my-1 h-px bg-muted",s),...r})}).displayName=o.Z0.displayName},92694:(e,t,s)=>{s.d(t,{d:()=>I});var a=s(57437),r=s(2265),o=s(75149),n=s(85392),l=s(37440);let i=r.forwardRef((e,t)=>{let{className:s,...r}=e;return(0,a.jsx)("div",{className:"relative w-full overflow-auto",children:(0,a.jsx)("table",{ref:t,className:(0,l.cn)("w-full caption-bottom text-sm",s),...r})})});i.displayName="Table";let d=r.forwardRef((e,t)=>{let{className:s,...r}=e;return(0,a.jsx)("thead",{ref:t,className:(0,l.cn)("[&_tr]:border-b",s),...r})});d.displayName="TableHeader";let c=r.forwardRef((e,t)=>{let{className:s,...r}=e;return(0,a.jsx)("tbody",{ref:t,className:(0,l.cn)("[&_tr:last-child]:border-0",s),...r})});c.displayName="TableBody",r.forwardRef((e,t)=>{let{className:s,...r}=e;return(0,a.jsx)("tfoot",{ref:t,className:(0,l.cn)("border-t bg-muted/50 font-medium [&>tr]:last:border-b-0",s),...r})}).displayName="TableFooter";let u=r.forwardRef((e,t)=>{let{className:s,...r}=e;return(0,a.jsx)("tr",{ref:t,className:(0,l.cn)("border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted",s),...r})});u.displayName="TableRow";let m=r.forwardRef((e,t)=>{let{className:s,...r}=e;return(0,a.jsx)("th",{ref:t,className:(0,l.cn)("h-12 px-4 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0",s),...r})});m.displayName="TableHead";let p=r.forwardRef((e,t)=>{let{className:s,...r}=e;return(0,a.jsx)("td",{ref:t,className:(0,l.cn)("p-4 align-middle [&:has([role=checkbox])]:pr-0",s),...r})});p.displayName="TableCell",r.forwardRef((e,t)=>{let{className:s,...r}=e;return(0,a.jsx)("caption",{ref:t,className:(0,l.cn)("mt-4 text-sm text-muted-foreground",s),...r})}).displayName="TableCaption";var f=s(71322),x=s(404),g=s(14392),h=s(42421),v=s(15554),b=s(46910);let N=r.forwardRef((e,t)=>{let{className:s,type:r,...o}=e;return(0,a.jsx)("input",{type:r,className:(0,l.cn)("flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",s),ref:t,...o})});function j(e){let{column:t,onSort:s,sortColumn:r,sortDirection:o,onFilter:l,filterValue:i}=e,{attributes:d,listeners:c,setNodeRef:u,transform:p,transition:j}=(0,n.nB)({id:t.key}),y={transform:v.ux.Transform.toString(p),transition:j};return(0,a.jsx)(m,{ref:u,style:y,className:"whitespace-nowrap",children:(0,a.jsxs)("div",{className:"flex items-center space-x-2",children:[(0,a.jsx)("div",{...d,...c,children:(0,a.jsx)(f.Z,{className:"h-4 w-4 cursor-grab"})}),(0,a.jsx)("span",{children:t.label}),(0,a.jsxs)("div",{className:"flex items-center space-x-1",onClick:e=>e.stopPropagation(),children:[(0,a.jsxs)(b.h_,{children:[(0,a.jsx)(b.$F,{asChild:!0,children:(0,a.jsx)("button",{className:"hover:bg-muted rounded p-1",onClick:e=>e.stopPropagation(),children:(0,a.jsx)(x.Z,{className:"h-4 w-4"})})}),(0,a.jsx)(b.AW,{children:(0,a.jsx)("div",{className:"p-2",children:(0,a.jsx)(N,{placeholder:"Filter ".concat(t.label),value:i,onChange:e=>l(t.key,e.target.value),onClick:e=>e.stopPropagation()})})})]}),(0,a.jsx)("button",{onClick:e=>{e.stopPropagation(),s(t.key)},className:"hover:bg-muted rounded p-1",children:r===t.key?"asc"===o?(0,a.jsx)(g.Z,{className:"h-4 w-4"}):(0,a.jsx)(h.Z,{className:"h-4 w-4"}):(0,a.jsx)(h.Z,{className:"h-4 w-4 opacity-30"})})]})]})})}N.displayName="Input";var y=s(81976);let w=y.zt,k=y.fC,_=y.xz,S=r.forwardRef((e,t)=>{let{className:s,sideOffset:r=4,...o}=e;return(0,a.jsx)(y.VY,{ref:t,sideOffset:r,className:(0,l.cn)("z-50 overflow-hidden rounded-md bg-popover px-3 py-2 text-sm text-popover-foreground shadow-md animate-in fade-in-50 zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",s),...o})});S.displayName=y.VY.displayName;var C=s(58606),T=s(70518),R=s(87592),A=(s(63550),s(50495));let z=e=>{let{className:t,...s}=e;return(0,a.jsx)("nav",{role:"navigation","aria-label":"pagination",className:(0,l.cn)("mx-auto flex w-full justify-center",t),...s})};z.displayName="Pagination";let E=r.forwardRef((e,t)=>{let{className:s,...r}=e;return(0,a.jsx)("ul",{ref:t,className:(0,l.cn)("flex flex-row items-center gap-1",s),...r})});E.displayName="PaginationContent";let O=r.forwardRef((e,t)=>{let{className:s,...r}=e;return(0,a.jsx)("li",{ref:t,className:(0,l.cn)("",s),...r})});O.displayName="PaginationItem";let M=e=>{let{className:t,isActive:s,size:r="icon",...o}=e;return(0,a.jsx)("a",{"aria-current":s?"page":void 0,className:(0,l.cn)((0,A.d)({variant:s?"outline":"ghost",size:r}),t),...o})};M.displayName="PaginationLink";let Z=e=>{let{className:t,...s}=e;return(0,a.jsxs)(M,{"aria-label":"Go to previous page",size:"default",className:(0,l.cn)("gap-1 pl-2.5",t),...s,children:[(0,a.jsx)(T.Z,{className:"h-4 w-4"}),(0,a.jsx)("span",{children:"Previous"})]})};Z.displayName="PaginationPrevious";let P=e=>{let{className:t,...s}=e;return(0,a.jsxs)(M,{"aria-label":"Go to next page",size:"default",className:(0,l.cn)("gap-1 pr-2.5",t),...s,children:[(0,a.jsx)("span",{children:"Next"}),(0,a.jsx)(R.Z,{className:"h-4 w-4"})]})};function I(e){let{columns:t,data:s,getRowKey:m,getCellContent:f,onRowClick:x,initialSortColumn:g="",initialSortDirection:h="asc",truncateConfig:v={enabled:!1,maxLength:100},rowProps:b,pageSize:N=10}=e,[y,T]=(0,r.useState)(g),[R,A]=(0,r.useState)(h),[I,L]=(0,r.useState)({}),[D,F]=(0,r.useState)(t.map(e=>e.key)),[V,U]=(0,r.useState)(1),B=(0,r.useCallback)(e=>{y===e?A(e=>"asc"===e?"desc":"asc"):(T(e),A("asc"))},[y]),Y=(0,r.useCallback)((e,t)=>{L(s=>({...s,[e]:t}))},[]),W=(0,r.useCallback)(e=>{let{active:t,over:s}=e;t.id!==(null==s?void 0:s.id)&&F(e=>{var a;let r=e.indexOf(t.id.toString()),o=e.indexOf(null!==(a=null==s?void 0:s.id.toString())&&void 0!==a?a:"");return(0,n.Rp)(e,r,o)})},[]),G=(0,r.useMemo)(()=>{let e=[...s];return Object.entries(I).forEach(t=>{let[s,a]=t;a&&(e=e.filter(e=>String(f(e,s)).toLowerCase().includes(a.toLowerCase())))}),y&&e.sort((e,t)=>{let s=f(e,y),a=f(t,y);if((0,l.kE)(s)&&(0,l.kE)(a)){let e=parseFloat(String(s)),t=parseFloat(String(a));return"asc"===R?e-t:t-e}return"asc"===R?String(s).localeCompare(String(a)):String(a).localeCompare(String(s))}),e},[s,I,y,R,f]),H=(0,r.useMemo)(()=>{let e=(V-1)*N;return G.slice(e,e+N)},[G,V,N]),X=Math.ceil(G.length/N),$=(0,r.useCallback)(()=>{U(e=>Math.max(1,e-1))},[]),q=(0,r.useCallback)(()=>{U(e=>Math.min(X,e+1))},[X]),J=(0,r.useCallback)(e=>{U(e)},[]),K=(0,r.useMemo)(()=>D.map(e=>t.find(t=>t.key===e)),[D,t]),Q=(e,t)=>{if(!t||"string"!=typeof e)return e;let s=v.maxLength||100;if(e.length<=s)return e;let r="".concat(e.slice(0,s),"...");return(0,a.jsx)(w,{children:(0,a.jsxs)(k,{children:[(0,a.jsx)(_,{asChild:!0,children:(0,a.jsx)("span",{className:"border-b border-dotted border-muted-foreground/50 hover:border-foreground transition-colors",children:r})}),(0,a.jsx)(S,{className:"max-w-[400px] whitespace-pre-wrap bg-popover/95 backdrop-blur supports-[backdrop-filter]:bg-popover/85",children:e})]})})},ee=(0,r.useCallback)((e,t)=>{if(t<=5)return Array.from({length:t},(e,t)=>t+1);let s=Math.max(1,e-Math.floor(2.5)),a=s+5-1;a>t&&(s=Math.max(1,(a=t)-5+1));let r=[];s>1&&(r.push(1),s>2&&r.push("..."));for(let e=s;e<=a;e++)r.push(e);return a<t&&(a<t-1&&r.push("..."),r.push(t)),r},[]);return(0,a.jsxs)("div",{className:"rounded-lg border bg-card",children:[(0,a.jsx)(o.LB,{onDragEnd:W,children:(0,a.jsxs)(i,{children:[(0,a.jsx)(d,{children:(0,a.jsx)(u,{children:(0,a.jsx)(n.Fo,{items:D,children:K.map(e=>(0,a.jsx)(j,{column:e,onSort:B,sortColumn:y,sortDirection:R,onFilter:Y,filterValue:I[e.key]||""},e.key))})})}),(0,a.jsx)(c,{children:H.map(e=>{var t;return(0,a.jsx)(C.E.tr,{className:(0,l.cn)(x?"cursor-pointer hover:bg-muted/50":"",null==b?void 0:null===(t=b(e))||void 0===t?void 0:t.className),onClick:()=>null==x?void 0:x(e),...(null==b?void 0:b(e))||{},children:K.map(t=>(0,a.jsx)(p,{children:Q(f(e,t.key),v.enabled)},"".concat(m(e),"-").concat(t.key)))},m(e))})})]})}),X>1&&(0,a.jsx)("div",{className:"flex justify-center py-4 border-t",children:(0,a.jsx)(z,{children:(0,a.jsxs)(E,{children:[(0,a.jsx)(O,{children:(0,a.jsx)(Z,{onClick:$,className:(0,l.cn)(1===V&&"pointer-events-none opacity-50")})}),ee(V,X).map((e,t)=>(0,a.jsx)(O,{children:"..."===e?(0,a.jsx)("span",{className:"px-4 py-2",children:"..."}):(0,a.jsx)(M,{onClick:()=>J(e),isActive:V===e,children:e})},"page-".concat(t))),(0,a.jsx)(O,{children:(0,a.jsx)(P,{onClick:q,className:(0,l.cn)(V===X&&"pointer-events-none opacity-50")})})]})})})]})}P.displayName="PaginationNext"},35657:(e,t,s)=>{s.d(t,{pm:()=>m});var a=s(2265);let r=0,o=new Map,n=e=>{if(o.has(e))return;let t=setTimeout(()=>{o.delete(e),c({type:"REMOVE_TOAST",toastId:e})},1e6);o.set(e,t)},l=(e,t)=>{switch(t.type){case"ADD_TOAST":return{...e,toasts:[t.toast,...e.toasts].slice(0,1)};case"UPDATE_TOAST":return{...e,toasts:e.toasts.map(e=>e.id===t.toast.id?{...e,...t.toast}:e)};case"DISMISS_TOAST":{let{toastId:s}=t;return s?n(s):e.toasts.forEach(e=>{n(e.id)}),{...e,toasts:e.toasts.map(e=>e.id===s||void 0===s?{...e,open:!1}:e)}}case"REMOVE_TOAST":if(void 0===t.toastId)return{...e,toasts:[]};return{...e,toasts:e.toasts.filter(e=>e.id!==t.toastId)}}},i=[],d={toasts:[]};function c(e){d=l(d,e),i.forEach(e=>{e(d)})}function u(e){let{...t}=e,s=(r=(r+1)%Number.MAX_VALUE).toString(),a=()=>c({type:"DISMISS_TOAST",toastId:s});return c({type:"ADD_TOAST",toast:{...t,id:s,open:!0,onOpenChange:e=>{e||a()}}}),{id:s,dismiss:a,update:e=>c({type:"UPDATE_TOAST",toast:{...e,id:s}})}}function m(){let[e,t]=a.useState(d);return a.useEffect(()=>(i.push(t),()=>{let e=i.indexOf(t);e>-1&&i.splice(e,1)}),[e]),{...e,toast:u,dismiss:e=>c({type:"DISMISS_TOAST",toastId:e})}}},37440:(e,t,s)=>{s.d(t,{L1:()=>n,cn:()=>l,kE:()=>o});var a=s(44839),r=s(96164);function o(e){return null!=e&&Number.isFinite(Number(e))}let n=(e,t)=>{var s,a,r,o,n,l,i,d,c,u,m,p,f,x,g,h,v,b,N,j,y;if(!e)return"N/A";switch(t){case"user_message":return(null===(r=e.generic_request)||void 0===r?void 0:null===(a=r.messages)||void 0===a?void 0:null===(s=a.find(e=>"user"===e.role))||void 0===s?void 0:s.content)||"N/A";case"assistant_message":if("object"==typeof e.response_message)return JSON.stringify(e.response_message,null,2);return e.response_message||"N/A";case"prompt_tokens":return(null===(n=e.raw_response.usage)||void 0===n?void 0:null===(o=n.prompt_tokens)||void 0===o?void 0:o.toString())||(null===(c=e.raw_response.response)||void 0===c?void 0:null===(d=c.body)||void 0===d?void 0:null===(i=d.usage)||void 0===i?void 0:null===(l=i.prompt_tokens)||void 0===l?void 0:l.toString())||"N/A";case"completion_tokens":return(null===(m=e.raw_response.usage)||void 0===m?void 0:null===(u=m.completion_tokens)||void 0===u?void 0:u.toString())||(null===(g=e.raw_response.response)||void 0===g?void 0:null===(x=g.body)||void 0===x?void 0:null===(f=x.usage)||void 0===f?void 0:null===(p=f.completion_tokens)||void 0===p?void 0:p.toString())||"N/A";case"total_tokens":return(null===(v=e.raw_response.usage)||void 0===v?void 0:null===(h=v.total_tokens)||void 0===h?void 0:h.toString())||(null===(y=e.raw_response.response)||void 0===y?void 0:null===(j=y.body)||void 0===j?void 0:null===(N=j.usage)||void 0===N?void 0:null===(b=N.total_tokens)||void 0===b?void 0:b.toString())||"N/A";default:return"N/A"}};function l(){for(var e=arguments.length,t=Array(e),s=0;s<e;s++)t[s]=arguments[s];return(0,r.m6)((0,a.W)(t))}}}]);