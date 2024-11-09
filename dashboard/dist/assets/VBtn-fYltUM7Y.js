import{aX as ie,g as V,ak as Ct,aY as Oe,m as N,al as ue,aZ as Ce,T as ce,p as S,a_ as St,K as Fe,e as m,R as G,aE as je,a$ as Ve,b0 as _t,b1 as kt,b2 as wt,aS as j,j as p,$ as le,b as U,c as H,r as F,d as W,b3 as xt,t as z,h as A,b4 as pt,b5 as It,i as c,a0 as De,a1 as Me,D as Se,b6 as _e,at as Q,s as D,x as M,aU as Bt,M as ke,z as de,Z as ge,ae as Vt,L as Ge,_ as Pt,Q as ye,b7 as Et,b8 as Pe,ai as Tt,ar as Ue,as as Lt,aH as $t,A as He,y as zt,b9 as Rt,aw as We,a6 as Nt,ba as At,bb as Ot,bc as Ee,a7 as Ft,G as jt,I as qe,v as Te,ah as Dt,u as Mt,E as Gt}from"./index-D3ojRB6d.js";const Xe=["top","bottom"],Ut=["start","end","left","right"];function Ht(e,a){let[n,t]=e.split(" ");return t||(t=ie(Xe,n)?"start":ie(Ut,n)?"top":"center"),{side:Le(n,a),align:Le(t,a)}}function Le(e,a){return e==="start"?a?"right":"left":e==="end"?a?"left":"right":e}function zn(e){return{side:{center:"center",top:"bottom",bottom:"top",left:"right",right:"left"}[e.side],align:e.align}}function Rn(e){return{side:e.side,align:{center:"center",top:"bottom",bottom:"top",left:"right",right:"left"}[e.align]}}function Nn(e){return{side:e.align,align:e.side}}function An(e){return ie(Xe,e.side)?"y":"x"}function On(e){let a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:"div",n=arguments.length>2?arguments[2]:void 0;return V()({name:n??Ct(Oe(e.replace(/__/g,"-"))),props:{tag:{type:String,default:a},...N()},setup(t,s){let{slots:i}=s;return()=>{var l;return ue(t.tag,{class:[e,t.class],style:t.style},(l=i.default)==null?void 0:l.call(i))}}})}const Wt=S({disabled:Boolean,group:Boolean,hideOnLeave:Boolean,leaveAbsolute:Boolean,mode:String,origin:String},"transition");function P(e,a,n){return V()({name:e,props:Wt({mode:n,origin:a}),setup(t,s){let{slots:i}=s;const l={onBeforeEnter(r){t.origin&&(r.style.transformOrigin=t.origin)},onLeave(r){if(t.leaveAbsolute){const{offsetTop:u,offsetLeft:v,offsetWidth:g,offsetHeight:y}=r;r._transitionInitialStyles={position:r.style.position,top:r.style.top,left:r.style.left,width:r.style.width,height:r.style.height},r.style.position="absolute",r.style.top=`${u}px`,r.style.left=`${v}px`,r.style.width=`${g}px`,r.style.height=`${y}px`}t.hideOnLeave&&r.style.setProperty("display","none","important")},onAfterLeave(r){if(t.leaveAbsolute&&(r!=null&&r._transitionInitialStyles)){const{position:u,top:v,left:g,width:y,height:o}=r._transitionInitialStyles;delete r._transitionInitialStyles,r.style.position=u||"",r.style.top=v||"",r.style.left=g||"",r.style.width=y||"",r.style.height=o||""}}};return()=>{const r=t.group?Ce:ce;return ue(r,{name:t.disabled?"":e,css:!t.disabled,...t.group?void 0:{mode:t.mode},...t.disabled?{}:l},i.default)}}})}function Ye(e,a){let n=arguments.length>2&&arguments[2]!==void 0?arguments[2]:"in-out";return V()({name:e,props:{mode:{type:String,default:n},disabled:Boolean,group:Boolean},setup(t,s){let{slots:i}=s;const l=t.group?Ce:ce;return()=>ue(l,{name:t.disabled?"":e,css:!t.disabled,...t.disabled?{}:a},i.default)}})}function Je(){let e=arguments.length>0&&arguments[0]!==void 0?arguments[0]:"";const n=(arguments.length>1&&arguments[1]!==void 0?arguments[1]:!1)?"width":"height",t=Oe(`offset-${n}`);return{onBeforeEnter(l){l._parent=l.parentNode,l._initialStyle={transition:l.style.transition,overflow:l.style.overflow,[n]:l.style[n]}},onEnter(l){const r=l._initialStyle;l.style.setProperty("transition","none","important"),l.style.overflow="hidden";const u=`${l[t]}px`;l.style[n]="0",l.offsetHeight,l.style.transition=r.transition,e&&l._parent&&l._parent.classList.add(e),requestAnimationFrame(()=>{l.style[n]=u})},onAfterEnter:i,onEnterCancelled:i,onLeave(l){l._initialStyle={transition:"",overflow:l.style.overflow,[n]:l.style[n]},l.style.overflow="hidden",l.style[n]=`${l[t]}px`,l.offsetHeight,requestAnimationFrame(()=>l.style[n]="0")},onAfterLeave:s,onLeaveCancelled:s};function s(l){e&&l._parent&&l._parent.classList.remove(e),i(l)}function i(l){const r=l._initialStyle[n];l.style.overflow=l._initialStyle.overflow,r!=null&&(l.style[n]=r),delete l._initialStyle}}P("fab-transition","center center","out-in");P("dialog-bottom-transition");P("dialog-top-transition");const Fn=P("fade-transition");P("scale-transition");P("scroll-x-transition");P("scroll-x-reverse-transition");P("scroll-y-transition");P("scroll-y-reverse-transition");P("slide-x-transition");P("slide-x-reverse-transition");const jn=P("slide-y-transition");P("slide-y-reverse-transition");const Dn=Ye("expand-transition",Je()),Mn=Ye("expand-x-transition",Je("",!0)),qt=S({defaults:Object,disabled:Boolean,reset:[Number,String],root:[Boolean,String],scoped:Boolean},"VDefaultsProvider"),ne=V(!1)({name:"VDefaultsProvider",props:qt(),setup(e,a){let{slots:n}=a;const{defaults:t,disabled:s,reset:i,root:l,scoped:r}=St(e);return Fe(t,{reset:i,root:l,scoped:r,disabled:s}),()=>{var u;return(u=n.default)==null?void 0:u.call(n)}}});function we(e){return je(()=>{const a=[],n={};if(e.value.background)if(Ve(e.value.background)){if(n.backgroundColor=e.value.background,!e.value.text&&_t(e.value.background)){const t=kt(e.value.background);if(t.a==null||t.a===1){const s=wt(t);n.color=s,n.caretColor=s}}}else a.push(`bg-${e.value.background}`);return e.value.text&&(Ve(e.value.text)?(n.color=e.value.text,n.caretColor=e.value.text):a.push(`text-${e.value.text}`)),{colorClasses:a,colorStyles:n}})}function re(e,a){const n=m(()=>({text:G(e)?e.value:a?e[a]:null})),{colorClasses:t,colorStyles:s}=we(n);return{textColorClasses:t,textColorStyles:s}}function ae(e,a){const n=m(()=>({background:G(e)?e.value:a?e[a]:null})),{colorClasses:t,colorStyles:s}=we(n);return{backgroundColorClasses:t,backgroundColorStyles:s}}const Xt=["x-small","small","default","large","x-large"],ve=S({size:{type:[String,Number],default:"default"}},"size");function fe(e){let a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:j();return je(()=>{let n,t;return ie(Xt,e.size)?n=`${a}--size-${e.size}`:e.size&&(t={width:p(e.size),height:p(e.size)}),{sizeClasses:n,sizeStyles:t}})}const Yt=S({color:String,disabled:Boolean,start:Boolean,end:Boolean,icon:le,...N(),...ve(),...U({tag:"i"}),...H()},"VIcon"),se=V()({name:"VIcon",props:Yt(),setup(e,a){let{attrs:n,slots:t}=a;const s=F(),{themeClasses:i}=W(e),{iconData:l}=xt(m(()=>s.value||e.icon)),{sizeClasses:r}=fe(e),{textColorClasses:u,textColorStyles:v}=re(z(e,"color"));return A(()=>{var o,d;const g=(o=t.default)==null?void 0:o.call(t);g&&(s.value=(d=pt(g).filter(b=>b.type===It&&b.children&&typeof b.children=="string")[0])==null?void 0:d.children);const y=!!(n.onClick||n.onClickOnce);return c(l.value.component,{tag:e.tag,icon:l.value.icon,class:["v-icon","notranslate",i.value,r.value,u.value,{"v-icon--clickable":y,"v-icon--disabled":e.disabled,"v-icon--start":e.start,"v-icon--end":e.end},e.class],style:[r.value?void 0:{fontSize:p(e.size),height:p(e.size),width:p(e.size)},v.value,e.style],role:y?"button":void 0,"aria-hidden":!y,tabindex:y?e.disabled?-1:0:void 0},{default:()=>[g]})}),{}}});function Jt(e){return{aspectStyles:m(()=>{const a=Number(e.aspectRatio);return a?{paddingBottom:String(1/a*100)+"%"}:void 0})}}const Ke=S({aspectRatio:[String,Number],contentClass:null,inline:Boolean,...N(),...De()},"VResponsive"),$e=V()({name:"VResponsive",props:Ke(),setup(e,a){let{slots:n}=a;const{aspectStyles:t}=Jt(e),{dimensionStyles:s}=Me(e);return A(()=>{var i;return c("div",{class:["v-responsive",{"v-responsive--inline":e.inline},e.class],style:[s.value,e.style]},[c("div",{class:"v-responsive__sizer",style:t.value},null),(i=n.additional)==null?void 0:i.call(n),n.default&&c("div",{class:["v-responsive__content",e.contentClass]},[n.default()])])}),{}}}),Z=S({rounded:{type:[Boolean,Number,String],default:void 0},tile:Boolean},"rounded");function ee(e){let a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:j();return{roundedClasses:m(()=>{const t=G(e)?e.value:e.rounded,s=G(e)?e.value:e.tile,i=[];if(t===!0||t==="")i.push(`${a}--rounded`);else if(typeof t=="string"||t===0)for(const l of String(t).split(" "))i.push(`rounded-${l}`);else(s||t===!1)&&i.push("rounded-0");return i})}}const Kt=S({transition:{type:[Boolean,String,Object],default:"fade-transition",validator:e=>e!==!0}},"transition"),te=(e,a)=>{let{slots:n}=a;const{transition:t,disabled:s,group:i,...l}=e,{component:r=i?Ce:ce,...u}=typeof t=="object"?t:{};return ue(r,Se(typeof t=="string"?{name:s?"":t}:u,typeof t=="string"?{}:Object.fromEntries(Object.entries({disabled:s,group:i}).filter(v=>{let[g,y]=v;return y!==void 0})),l),n)};function Qt(e,a){if(!_e)return;const n=a.modifiers||{},t=a.value,{handler:s,options:i}=typeof t=="object"?t:{handler:t,options:{}},l=new IntersectionObserver(function(){var y;let r=arguments.length>0&&arguments[0]!==void 0?arguments[0]:[],u=arguments.length>1?arguments[1]:void 0;const v=(y=e._observe)==null?void 0:y[a.instance.$.uid];if(!v)return;const g=r.some(o=>o.isIntersecting);s&&(!n.quiet||v.init)&&(!n.once||g||v.init)&&s(g,r,u),g&&n.once?Qe(e,a):v.init=!0},i);e._observe=Object(e._observe),e._observe[a.instance.$.uid]={init:!1,observer:l},l.observe(e)}function Qe(e,a){var t;const n=(t=e._observe)==null?void 0:t[a.instance.$.uid];n&&(n.observer.unobserve(e),delete e._observe[a.instance.$.uid])}const Zt={mounted:Qt,unmounted:Qe},en=S({alt:String,cover:Boolean,color:String,draggable:{type:[Boolean,String],default:void 0},eager:Boolean,gradient:String,lazySrc:String,options:{type:Object,default:()=>({root:void 0,rootMargin:void 0,threshold:void 0})},sizes:String,src:{type:[String,Object],default:""},crossorigin:String,referrerpolicy:String,srcset:String,position:String,...Ke(),...N(),...Z(),...Kt()},"VImg"),tn=V()({name:"VImg",directives:{intersect:Zt},props:en(),emits:{loadstart:e=>!0,load:e=>!0,error:e=>!0},setup(e,a){let{emit:n,slots:t}=a;const{backgroundColorClasses:s,backgroundColorStyles:i}=ae(z(e,"color")),{roundedClasses:l}=ee(e),r=Q("VImg"),u=D(""),v=F(),g=D(e.eager?"loading":"idle"),y=D(),o=D(),d=m(()=>e.src&&typeof e.src=="object"?{src:e.src.src,srcset:e.srcset||e.src.srcset,lazySrc:e.lazySrc||e.src.lazySrc,aspect:Number(e.aspectRatio||e.src.aspect||0)}:{src:e.src,srcset:e.srcset,lazySrc:e.lazySrc,aspect:Number(e.aspectRatio||0)}),b=m(()=>d.value.aspect||y.value/o.value||0);M(()=>e.src,()=>{f(g.value!=="idle")}),M(b,(h,k)=>{!h&&k&&v.value&&x(v.value)}),Bt(()=>f());function f(h){if(!(e.eager&&h)&&!(_e&&!h&&!e.eager)){if(g.value="loading",d.value.lazySrc){const k=new Image;k.src=d.value.lazySrc,x(k,null)}d.value.src&&ke(()=>{var k;n("loadstart",((k=v.value)==null?void 0:k.currentSrc)||d.value.src),setTimeout(()=>{var I;if(!r.isUnmounted)if((I=v.value)!=null&&I.complete){if(v.value.naturalWidth||_(),g.value==="error")return;b.value||x(v.value,null),g.value==="loading"&&C()}else b.value||x(v.value),E()})})}}function C(){var h;r.isUnmounted||(E(),x(v.value),g.value="loaded",n("load",((h=v.value)==null?void 0:h.currentSrc)||d.value.src))}function _(){var h;r.isUnmounted||(g.value="error",n("error",((h=v.value)==null?void 0:h.currentSrc)||d.value.src))}function E(){const h=v.value;h&&(u.value=h.currentSrc||h.src)}let T=-1;de(()=>{clearTimeout(T)});function x(h){let k=arguments.length>1&&arguments[1]!==void 0?arguments[1]:100;const I=()=>{if(clearTimeout(T),r.isUnmounted)return;const{naturalHeight:Y,naturalWidth:Be}=h;Y||Be?(y.value=Be,o.value=Y):!h.complete&&g.value==="loading"&&k!=null?T=window.setTimeout(I,k):(h.currentSrc.endsWith(".svg")||h.currentSrc.startsWith("data:image/svg+xml"))&&(y.value=1,o.value=1)};I()}const R=m(()=>({"v-img__img--cover":e.cover,"v-img__img--contain":!e.cover})),L=()=>{var I;if(!d.value.src||g.value==="idle")return null;const h=c("img",{class:["v-img__img",R.value],style:{objectPosition:e.position},src:d.value.src,srcset:d.value.srcset,alt:e.alt,crossorigin:e.crossorigin,referrerpolicy:e.referrerpolicy,draggable:e.draggable,sizes:e.sizes,ref:v,onLoad:C,onError:_},null),k=(I=t.sources)==null?void 0:I.call(t);return c(te,{transition:e.transition,appear:!0},{default:()=>[ge(k?c("picture",{class:"v-img__picture"},[k,h]):h,[[Pt,g.value==="loaded"]])]})},O=()=>c(te,{transition:e.transition},{default:()=>[d.value.lazySrc&&g.value!=="loaded"&&c("img",{class:["v-img__img","v-img__img--preload",R.value],style:{objectPosition:e.position},src:d.value.lazySrc,alt:e.alt,crossorigin:e.crossorigin,referrerpolicy:e.referrerpolicy,draggable:e.draggable},null)]}),q=()=>t.placeholder?c(te,{transition:e.transition,appear:!0},{default:()=>[(g.value==="loading"||g.value==="error"&&!t.error)&&c("div",{class:"v-img__placeholder"},[t.placeholder()])]}):null,X=()=>t.error?c(te,{transition:e.transition,appear:!0},{default:()=>[g.value==="error"&&c("div",{class:"v-img__error"},[t.error()])]}):null,w=()=>e.gradient?c("div",{class:"v-img__gradient",style:{backgroundImage:`linear-gradient(${e.gradient})`}},null):null,$=D(!1);{const h=M(b,k=>{k&&(requestAnimationFrame(()=>{requestAnimationFrame(()=>{$.value=!0})}),h())})}return A(()=>{const h=$e.filterProps(e);return ge(c($e,Se({class:["v-img",{"v-img--booting":!$.value},s.value,l.value,e.class],style:[{width:p(e.width==="auto"?y.value:e.width)},i.value,e.style]},h,{aspectRatio:b.value,"aria-label":e.alt,role:e.alt?"img":void 0}),{additional:()=>c(Ge,null,[c(L,null,null),c(O,null,null),c(w,null,null),c(q,null,null),c(X,null,null)]),default:t.default}),[[Vt("intersect"),{handler:f,options:e.options},null,{once:!0}]])}),{currentSrc:u,image:v,state:g,naturalWidth:y,naturalHeight:o}}}),nn=[null,"default","comfortable","compact"],xe=S({density:{type:String,default:"default",validator:e=>nn.includes(e)}},"density");function pe(e){let a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:j();return{densityClasses:m(()=>`${a}--density-${e.density}`)}}const an=["elevated","flat","tonal","outlined","text","plain"];function Ze(e,a){return c(Ge,null,[e&&c("span",{key:"overlay",class:`${a}__overlay`},null),c("span",{key:"underlay",class:`${a}__underlay`},null)])}const Ie=S({color:String,variant:{type:String,default:"elevated",validator:e=>an.includes(e)}},"variant");function et(e){let a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:j();const n=m(()=>{const{variant:i}=ye(e);return`${a}--variant-${i}`}),{colorClasses:t,colorStyles:s}=we(m(()=>{const{variant:i,color:l}=ye(e);return{[["elevated","flat"].includes(i)?"background":"text"]:l}}));return{colorClasses:t,colorStyles:s,variantClasses:n}}const sn=S({start:Boolean,end:Boolean,icon:le,image:String,text:String,...N(),...xe(),...Z(),...ve(),...U(),...H(),...Ie({variant:"flat"})},"VAvatar"),Gn=V()({name:"VAvatar",props:sn(),setup(e,a){let{slots:n}=a;const{themeClasses:t}=W(e),{colorClasses:s,colorStyles:i,variantClasses:l}=et(e),{densityClasses:r}=pe(e),{roundedClasses:u}=ee(e),{sizeClasses:v,sizeStyles:g}=fe(e);return A(()=>c(e.tag,{class:["v-avatar",{"v-avatar--start":e.start,"v-avatar--end":e.end},t.value,s.value,r.value,u.value,v.value,l.value,e.class],style:[i.value,g.value,e.style]},{default:()=>[n.default?c(ne,{key:"content-defaults",defaults:{VImg:{cover:!0,image:e.image},VIcon:{icon:e.icon}}},{default:()=>[n.default()]}):e.image?c(tn,{key:"image",src:e.image,alt:"",cover:!0},null):e.icon?c(se,{key:"icon",icon:e.icon},null):e.text,Ze(!1,"v-avatar")]})),{}}}),be=Symbol("rippleStop"),ln=80;function ze(e,a){e.style.transform=a,e.style.webkitTransform=a}function he(e){return e.constructor.name==="TouchEvent"}function tt(e){return e.constructor.name==="KeyboardEvent"}const rn=function(e,a){var y;let n=arguments.length>2&&arguments[2]!==void 0?arguments[2]:{},t=0,s=0;if(!tt(e)){const o=a.getBoundingClientRect(),d=he(e)?e.touches[e.touches.length-1]:e;t=d.clientX-o.left,s=d.clientY-o.top}let i=0,l=.3;(y=a._ripple)!=null&&y.circle?(l=.15,i=a.clientWidth/2,i=n.center?i:i+Math.sqrt((t-i)**2+(s-i)**2)/4):i=Math.sqrt(a.clientWidth**2+a.clientHeight**2)/2;const r=`${(a.clientWidth-i*2)/2}px`,u=`${(a.clientHeight-i*2)/2}px`,v=n.center?r:`${t-i}px`,g=n.center?u:`${s-i}px`;return{radius:i,scale:l,x:v,y:g,centerX:r,centerY:u}},oe={show(e,a){var d;let n=arguments.length>2&&arguments[2]!==void 0?arguments[2]:{};if(!((d=a==null?void 0:a._ripple)!=null&&d.enabled))return;const t=document.createElement("span"),s=document.createElement("span");t.appendChild(s),t.className="v-ripple__container",n.class&&(t.className+=` ${n.class}`);const{radius:i,scale:l,x:r,y:u,centerX:v,centerY:g}=rn(e,a,n),y=`${i*2}px`;s.className="v-ripple__animation",s.style.width=y,s.style.height=y,a.appendChild(t);const o=window.getComputedStyle(a);o&&o.position==="static"&&(a.style.position="relative",a.dataset.previousPosition="static"),s.classList.add("v-ripple__animation--enter"),s.classList.add("v-ripple__animation--visible"),ze(s,`translate(${r}, ${u}) scale3d(${l},${l},${l})`),s.dataset.activated=String(performance.now()),setTimeout(()=>{s.classList.remove("v-ripple__animation--enter"),s.classList.add("v-ripple__animation--in"),ze(s,`translate(${v}, ${g}) scale3d(1,1,1)`)},0)},hide(e){var i;if(!((i=e==null?void 0:e._ripple)!=null&&i.enabled))return;const a=e.getElementsByClassName("v-ripple__animation");if(a.length===0)return;const n=a[a.length-1];if(n.dataset.isHiding)return;n.dataset.isHiding="true";const t=performance.now()-Number(n.dataset.activated),s=Math.max(250-t,0);setTimeout(()=>{n.classList.remove("v-ripple__animation--in"),n.classList.add("v-ripple__animation--out"),setTimeout(()=>{var r;e.getElementsByClassName("v-ripple__animation").length===1&&e.dataset.previousPosition&&(e.style.position=e.dataset.previousPosition,delete e.dataset.previousPosition),((r=n.parentNode)==null?void 0:r.parentNode)===e&&e.removeChild(n.parentNode)},300)},s)}};function nt(e){return typeof e>"u"||!!e}function J(e){const a={},n=e.currentTarget;if(!(!(n!=null&&n._ripple)||n._ripple.touched||e[be])){if(e[be]=!0,he(e))n._ripple.touched=!0,n._ripple.isTouch=!0;else if(n._ripple.isTouch)return;if(a.center=n._ripple.centered||tt(e),n._ripple.class&&(a.class=n._ripple.class),he(e)){if(n._ripple.showTimerCommit)return;n._ripple.showTimerCommit=()=>{oe.show(e,n,a)},n._ripple.showTimer=window.setTimeout(()=>{var t;(t=n==null?void 0:n._ripple)!=null&&t.showTimerCommit&&(n._ripple.showTimerCommit(),n._ripple.showTimerCommit=null)},ln)}else oe.show(e,n,a)}}function Re(e){e[be]=!0}function B(e){const a=e.currentTarget;if(a!=null&&a._ripple){if(window.clearTimeout(a._ripple.showTimer),e.type==="touchend"&&a._ripple.showTimerCommit){a._ripple.showTimerCommit(),a._ripple.showTimerCommit=null,a._ripple.showTimer=window.setTimeout(()=>{B(e)});return}window.setTimeout(()=>{a._ripple&&(a._ripple.touched=!1)}),oe.hide(a)}}function at(e){const a=e.currentTarget;a!=null&&a._ripple&&(a._ripple.showTimerCommit&&(a._ripple.showTimerCommit=null),window.clearTimeout(a._ripple.showTimer))}let K=!1;function st(e){!K&&(e.keyCode===Pe.enter||e.keyCode===Pe.space)&&(K=!0,J(e))}function it(e){K=!1,B(e)}function lt(e){K&&(K=!1,B(e))}function rt(e,a,n){const{value:t,modifiers:s}=a,i=nt(t);if(i||oe.hide(e),e._ripple=e._ripple??{},e._ripple.enabled=i,e._ripple.centered=s.center,e._ripple.circle=s.circle,Et(t)&&t.class&&(e._ripple.class=t.class),i&&!n){if(s.stop){e.addEventListener("touchstart",Re,{passive:!0}),e.addEventListener("mousedown",Re);return}e.addEventListener("touchstart",J,{passive:!0}),e.addEventListener("touchend",B,{passive:!0}),e.addEventListener("touchmove",at,{passive:!0}),e.addEventListener("touchcancel",B),e.addEventListener("mousedown",J),e.addEventListener("mouseup",B),e.addEventListener("mouseleave",B),e.addEventListener("keydown",st),e.addEventListener("keyup",it),e.addEventListener("blur",lt),e.addEventListener("dragstart",B,{passive:!0})}else!i&&n&&ot(e)}function ot(e){e.removeEventListener("mousedown",J),e.removeEventListener("touchstart",J),e.removeEventListener("touchend",B),e.removeEventListener("touchmove",at),e.removeEventListener("touchcancel",B),e.removeEventListener("mouseup",B),e.removeEventListener("mouseleave",B),e.removeEventListener("keydown",st),e.removeEventListener("keyup",it),e.removeEventListener("dragstart",B),e.removeEventListener("blur",lt)}function on(e,a){rt(e,a,!1)}function un(e){delete e._ripple,ot(e)}function cn(e,a){if(a.value===a.oldValue)return;const n=nt(a.oldValue);rt(e,a,n)}const dn={mounted:on,unmounted:un,updated:cn},vn=S({modelValue:{type:null,default:void 0},multiple:Boolean,mandatory:[Boolean,String],max:Number,selectedClass:String,disabled:Boolean},"group"),fn=S({value:null,disabled:Boolean,selectedClass:String},"group-item");function mn(e,a){let n=arguments.length>2&&arguments[2]!==void 0?arguments[2]:!0;const t=Q("useGroupItem");if(!t)throw new Error("[Vuetify] useGroupItem composable must be used inside a component setup function");const s=Tt();Ue(Symbol.for(`${a.description}:id`),s);const i=Lt(a,null);if(!i){if(!n)return i;throw new Error(`[Vuetify] Could not find useGroup injection with symbol ${a.description}`)}const l=z(e,"value"),r=m(()=>!!(i.disabled.value||e.disabled));i.register({id:s,value:l,disabled:r},t),de(()=>{i.unregister(s)});const u=m(()=>i.isSelected(s)),v=m(()=>i.items.value[0].id===s),g=m(()=>i.items.value[i.items.value.length-1].id===s),y=m(()=>u.value&&[i.selectedClass.value,e.selectedClass]);return M(u,o=>{t.emit("group:selected",{value:o})},{flush:"sync"}),{id:s,isSelected:u,isFirst:v,isLast:g,toggle:()=>i.select(s,!u.value),select:o=>i.select(s,o),selectedClass:y,value:l,disabled:r,group:i}}function gn(e,a){let n=!1;const t=$t([]),s=He(e,"modelValue",[],o=>o==null?[]:ut(t,Nt(o)),o=>{const d=bn(t,o);return e.multiple?d:d[0]}),i=Q("useGroup");function l(o,d){const b=o,f=Symbol.for(`${a.description}:id`),_=At(f,i==null?void 0:i.vnode).indexOf(d);ye(b.value)==null&&(b.value=_,b.useIndexAsValue=!0),_>-1?t.splice(_,0,b):t.push(b)}function r(o){if(n)return;u();const d=t.findIndex(b=>b.id===o);t.splice(d,1)}function u(){const o=t.find(d=>!d.disabled);o&&e.mandatory==="force"&&!s.value.length&&(s.value=[o.id])}zt(()=>{u()}),de(()=>{n=!0}),Rt(()=>{for(let o=0;o<t.length;o++)t[o].useIndexAsValue&&(t[o].value=o)});function v(o,d){const b=t.find(f=>f.id===o);if(!(d&&(b!=null&&b.disabled)))if(e.multiple){const f=s.value.slice(),C=f.findIndex(E=>E===o),_=~C;if(d=d??!_,_&&e.mandatory&&f.length<=1||!_&&e.max!=null&&f.length+1>e.max)return;C<0&&d?f.push(o):C>=0&&!d&&f.splice(C,1),s.value=f}else{const f=s.value.includes(o);if(e.mandatory&&f)return;s.value=d??!f?[o]:[]}}function g(o){if(e.multiple,s.value.length){const d=s.value[0],b=t.findIndex(_=>_.id===d);let f=(b+o)%t.length,C=t[f];for(;C.disabled&&f!==b;)f=(f+o)%t.length,C=t[f];if(C.disabled)return;s.value=[t[f].id]}else{const d=t.find(b=>!b.disabled);d&&(s.value=[d.id])}}const y={register:l,unregister:r,selected:s,select:v,disabled:z(e,"disabled"),prev:()=>g(t.length-1),next:()=>g(1),isSelected:o=>s.value.includes(o),selectedClass:m(()=>e.selectedClass),items:m(()=>t),getItemIndex:o=>yn(t,o)};return Ue(a,y),y}function yn(e,a){const n=ut(e,[a]);return n.length?e.findIndex(t=>t.id===n[0]):-1}function ut(e,a){const n=[];return a.forEach(t=>{const s=e.find(l=>We(t,l.value)),i=e[t];(s==null?void 0:s.value)!=null?n.push(s.id):i!=null&&n.push(i.id)}),n}function bn(e,a){const n=[];return a.forEach(t=>{const s=e.findIndex(i=>i.id===t);if(~s){const i=e[s];n.push(i.value!=null?i.value:s)}}),n}const ct=S({border:[Boolean,Number,String]},"border");function dt(e){let a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:j();return{borderClasses:m(()=>{const t=G(e)?e.value:e.border,s=[];if(t===!0||t==="")s.push(`${a}--border`);else if(typeof t=="string"||t===0)for(const i of String(t).split(" "))s.push(`border-${i}`);return s})}}const vt=S({elevation:{type:[Number,String],validator(e){const a=parseInt(e);return!isNaN(a)&&a>=0&&a<=24}}},"elevation");function ft(e){return{elevationClasses:m(()=>{const n=G(e)?e.value:e.elevation,t=[];return n==null||t.push(`elevation-${n}`),t})}}function hn(){const e=Q("useRoute");return m(()=>{var a;return(a=e==null?void 0:e.proxy)==null?void 0:a.$route})}function Un(){var e,a;return(a=(e=Q("useRouter"))==null?void 0:e.proxy)==null?void 0:a.$router}function Cn(e,a){var v,g;const n=Ot("RouterLink"),t=m(()=>!!(e.href||e.to)),s=m(()=>(t==null?void 0:t.value)||Ee(a,"click")||Ee(e,"click"));if(typeof n=="string"||!("useLink"in n))return{isLink:t,isClickable:s,href:z(e,"href")};const i=m(()=>({...e,to:z(()=>e.to||"")})),l=n.useLink(i.value),r=m(()=>e.to?l:void 0),u=hn();return{isLink:t,isClickable:s,route:(v=r.value)==null?void 0:v.route,navigate:(g=r.value)==null?void 0:g.navigate,isActive:m(()=>{var y,o,d;return r.value?e.exact?u.value?((d=r.value.isExactActive)==null?void 0:d.value)&&We(r.value.route.value.query,u.value.query):((o=r.value.isExactActive)==null?void 0:o.value)??!1:((y=r.value.isActive)==null?void 0:y.value)??!1:!1}),href:m(()=>{var y;return e.to?(y=r.value)==null?void 0:y.route.value.href:e.href})}}const Sn=S({href:String,replace:Boolean,to:[String,Object],exact:Boolean},"router");let me=!1;function Hn(e,a){let n=!1,t,s;Ft&&(ke(()=>{window.addEventListener("popstate",i),t=e==null?void 0:e.beforeEach((l,r,u)=>{me?n?a(u):u():setTimeout(()=>n?a(u):u()),me=!0}),s=e==null?void 0:e.afterEach(()=>{me=!1})}),jt(()=>{window.removeEventListener("popstate",i),t==null||t(),s==null||s()}));function i(l){var r;(r=l.state)!=null&&r.replaced||(n=!0,setTimeout(()=>n=!1))}}function mt(e,a){const n=F(),t=D(!1);if(_e){const s=new IntersectionObserver(i=>{t.value=!!i.find(l=>l.isIntersecting)},a);de(()=>{s.disconnect()}),M(n,(i,l)=>{l&&(s.unobserve(l),t.value=!1),i&&s.observe(i)},{flush:"post"})}return{intersectionRef:n,isIntersecting:t}}const Ne={center:"center",top:"bottom",bottom:"top",left:"right",right:"left"},gt=S({location:String},"location");function yt(e){let a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!1,n=arguments.length>2?arguments[2]:void 0;const{isRtl:t}=qe();return{locationStyles:m(()=>{if(!e.location)return{};const{side:i,align:l}=Ht(e.location.split(" ").length>1?e.location:`${e.location} center`,t.value);function r(v){return n?n(v):0}const u={};return i!=="center"&&(a?u[Ne[i]]=`calc(100% - ${r(i)}px)`:u[i]=0),l!=="center"?a?u[Ne[l]]=`calc(100% - ${r(l)}px)`:u[l]=0:(i==="center"?u.top=u.left="50%":u[{top:"left",bottom:"left",left:"top",right:"top"}[i]]="50%",u.transform={top:"translateX(-50%)",bottom:"translateX(-50%)",left:"translateY(-50%)",right:"translateY(-50%)",center:"translate(-50%, -50%)"}[i]),u})}}const _n=S({absolute:Boolean,active:{type:Boolean,default:!0},bgColor:String,bgOpacity:[Number,String],bufferValue:{type:[Number,String],default:0},bufferColor:String,bufferOpacity:[Number,String],clickable:Boolean,color:String,height:{type:[Number,String],default:4},indeterminate:Boolean,max:{type:[Number,String],default:100},modelValue:{type:[Number,String],default:0},opacity:[Number,String],reverse:Boolean,stream:Boolean,striped:Boolean,roundedBar:Boolean,...N(),...gt({location:"top"}),...Z(),...U(),...H()},"VProgressLinear"),kn=V()({name:"VProgressLinear",props:_n(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:n}=a;const t=He(e,"modelValue"),{isRtl:s,rtlClasses:i}=qe(),{themeClasses:l}=W(e),{locationStyles:r}=yt(e),{textColorClasses:u,textColorStyles:v}=re(e,"color"),{backgroundColorClasses:g,backgroundColorStyles:y}=ae(m(()=>e.bgColor||e.color)),{backgroundColorClasses:o,backgroundColorStyles:d}=ae(m(()=>e.bufferColor||e.bgColor||e.color)),{backgroundColorClasses:b,backgroundColorStyles:f}=ae(e,"color"),{roundedClasses:C}=ee(e),{intersectionRef:_,isIntersecting:E}=mt(),T=m(()=>parseFloat(e.max)),x=m(()=>parseFloat(e.height)),R=m(()=>Te(parseFloat(e.bufferValue)/T.value*100,0,100)),L=m(()=>Te(parseFloat(t.value)/T.value*100,0,100)),O=m(()=>s.value!==e.reverse),q=m(()=>e.indeterminate?"fade-transition":"slide-x-transition");function X(w){if(!_.value)return;const{left:$,right:h,width:k}=_.value.getBoundingClientRect(),I=O.value?k-w.clientX+(h-k):w.clientX-$;t.value=Math.round(I/k*T.value)}return A(()=>c(e.tag,{ref:_,class:["v-progress-linear",{"v-progress-linear--absolute":e.absolute,"v-progress-linear--active":e.active&&E.value,"v-progress-linear--reverse":O.value,"v-progress-linear--rounded":e.rounded,"v-progress-linear--rounded-bar":e.roundedBar,"v-progress-linear--striped":e.striped},C.value,l.value,i.value,e.class],style:[{bottom:e.location==="bottom"?0:void 0,top:e.location==="top"?0:void 0,height:e.active?p(x.value):0,"--v-progress-linear-height":p(x.value),...e.absolute?r.value:{}},e.style],role:"progressbar","aria-hidden":e.active?"false":"true","aria-valuemin":"0","aria-valuemax":e.max,"aria-valuenow":e.indeterminate?void 0:L.value,onClick:e.clickable&&X},{default:()=>[e.stream&&c("div",{key:"stream",class:["v-progress-linear__stream",u.value],style:{...v.value,[O.value?"left":"right"]:p(-x.value),borderTop:`${p(x.value/2)} dotted`,opacity:parseFloat(e.bufferOpacity),top:`calc(50% - ${p(x.value/4)})`,width:p(100-R.value,"%"),"--v-progress-linear-stream-to":p(x.value*(O.value?1:-1))}},null),c("div",{class:["v-progress-linear__background",g.value],style:[y.value,{opacity:parseFloat(e.bgOpacity),width:e.stream?0:void 0}]},null),c("div",{class:["v-progress-linear__buffer",o.value],style:[d.value,{opacity:parseFloat(e.bufferOpacity),width:p(R.value,"%")}]},null),c(ce,{name:q.value},{default:()=>[e.indeterminate?c("div",{class:"v-progress-linear__indeterminate"},[["long","short"].map(w=>c("div",{key:w,class:["v-progress-linear__indeterminate",w,b.value],style:f.value},null))]):c("div",{class:["v-progress-linear__determinate",b.value],style:[f.value,{width:p(L.value,"%")}]},null)]}),n.default&&c("div",{class:"v-progress-linear__content"},[n.default({value:L.value,buffer:R.value})])]})),{}}}),wn=S({loading:[Boolean,String]},"loader");function xn(e){let a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:j();return{loaderClasses:m(()=>({[`${a}--loading`]:e.loading}))}}function Wn(e,a){var t;let{slots:n}=a;return c("div",{class:`${e.name}__loader`},[((t=n.default)==null?void 0:t.call(n,{color:e.color,isActive:e.active}))||c(kn,{absolute:e.absolute,active:e.active,color:e.color,height:"2",indeterminate:!0},null)])}const qn=Dt("user",()=>{const e=localStorage.getItem("fci-user")?F(JSON.parse(localStorage.getItem("fci-user"))):F({username:"",password:"",token:"",id:0}),a=F(""),n=F(!0),t="/api/v1/auth/";async function s(){const r=await(await fetch(t,{method:"post",headers:{"Content-Type":"application/json"},body:JSON.stringify(e.value)})).json();r.token&&r.id?(e.value.token=r.token,e.value.id=r.id,n.value=!0,a.value="",localStorage.setItem("fci-user",JSON.stringify(r))):(a.value="Username or password invalid.",n.value=!1)}function i(){e.value.id=0,e.value.token="",e.value.username="",e.value.password="",localStorage.removeItem("fci-user")}return{user:e,isValid:n,loginResult:a,login:s,logout:i}}),pn=["static","relative","fixed","absolute","sticky"],In=S({position:{type:String,validator:e=>pn.includes(e)}},"position");function Bn(e){let a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:j();return{positionClasses:m(()=>e.position?`${a}--${e.position}`:void 0)}}const bt=S({baseColor:String,divided:Boolean,...ct(),...N(),...xe(),...vt(),...Z(),...U(),...H(),...Ie()},"VBtnGroup"),Ae=V()({name:"VBtnGroup",props:bt(),setup(e,a){let{slots:n}=a;const{themeClasses:t}=W(e),{densityClasses:s}=pe(e),{borderClasses:i}=dt(e),{elevationClasses:l}=ft(e),{roundedClasses:r}=ee(e);Fe({VBtn:{height:"auto",baseColor:z(e,"baseColor"),color:z(e,"color"),density:z(e,"density"),flat:!0,variant:z(e,"variant")}}),A(()=>c(e.tag,{class:["v-btn-group",{"v-btn-group--divided":e.divided},t.value,i.value,s.value,l.value,r.value,e.class],style:e.style},n))}}),ht=Symbol.for("vuetify:v-btn-toggle"),Vn=S({...bt(),...vn()},"VBtnToggle");V()({name:"VBtnToggle",props:Vn(),emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:n}=a;const{isSelected:t,next:s,prev:i,select:l,selected:r}=gn(e,ht);return A(()=>{const u=Ae.filterProps(e);return c(Ae,Se({class:["v-btn-toggle",e.class]},u,{style:e.style}),{default:()=>{var v;return[(v=n.default)==null?void 0:v.call(n,{isSelected:t,next:s,prev:i,select:l,selected:r})]}})}),{next:s,prev:i,select:l}}});const Pn=S({bgColor:String,color:String,indeterminate:[Boolean,String],modelValue:{type:[Number,String],default:0},rotate:{type:[Number,String],default:0},width:{type:[Number,String],default:4},...N(),...ve(),...U({tag:"div"}),...H()},"VProgressCircular"),En=V()({name:"VProgressCircular",props:Pn(),setup(e,a){let{slots:n}=a;const t=20,s=2*Math.PI*t,i=F(),{themeClasses:l}=W(e),{sizeClasses:r,sizeStyles:u}=fe(e),{textColorClasses:v,textColorStyles:g}=re(z(e,"color")),{textColorClasses:y,textColorStyles:o}=re(z(e,"bgColor")),{intersectionRef:d,isIntersecting:b}=mt(),{resizeRef:f,contentRect:C}=Mt(),_=m(()=>Math.max(0,Math.min(100,parseFloat(e.modelValue)))),E=m(()=>Number(e.width)),T=m(()=>u.value?Number(e.size):C.value?C.value.width:Math.max(E.value,32)),x=m(()=>t/(1-E.value/T.value)*2),R=m(()=>E.value/T.value*x.value),L=m(()=>p((100-_.value)/100*s));return Gt(()=>{d.value=i.value,f.value=i.value}),A(()=>c(e.tag,{ref:i,class:["v-progress-circular",{"v-progress-circular--indeterminate":!!e.indeterminate,"v-progress-circular--visible":b.value,"v-progress-circular--disable-shrink":e.indeterminate==="disable-shrink"},l.value,r.value,v.value,e.class],style:[u.value,g.value,e.style],role:"progressbar","aria-valuemin":"0","aria-valuemax":"100","aria-valuenow":e.indeterminate?void 0:_.value},{default:()=>[c("svg",{style:{transform:`rotate(calc(-90deg + ${Number(e.rotate)}deg))`},xmlns:"http://www.w3.org/2000/svg",viewBox:`0 0 ${x.value} ${x.value}`},[c("circle",{class:["v-progress-circular__underlay",y.value],style:o.value,fill:"transparent",cx:"50%",cy:"50%",r:t,"stroke-width":R.value,"stroke-dasharray":s,"stroke-dashoffset":0},null),c("circle",{class:"v-progress-circular__overlay",fill:"transparent",cx:"50%",cy:"50%",r:t,"stroke-width":R.value,"stroke-dasharray":s,"stroke-dashoffset":L.value},null)]),n.default&&c("div",{class:"v-progress-circular__content"},[n.default({value:_.value})])]})),{}}});function Tn(e,a){M(()=>{var n;return(n=e.isActive)==null?void 0:n.value},n=>{e.isLink.value&&n&&a&&ke(()=>{a(!0)})},{immediate:!0})}const Ln=S({active:{type:Boolean,default:void 0},baseColor:String,symbol:{type:null,default:ht},flat:Boolean,icon:[Boolean,String,Function,Object],prependIcon:le,appendIcon:le,block:Boolean,readonly:Boolean,slim:Boolean,stacked:Boolean,ripple:{type:[Boolean,Object],default:!0},text:String,...ct(),...N(),...xe(),...De(),...vt(),...fn(),...wn(),...gt(),...In(),...Z(),...Sn(),...ve(),...U({tag:"button"}),...H(),...Ie({variant:"elevated"})},"VBtn"),Xn=V()({name:"VBtn",props:Ln(),emits:{"group:selected":e=>!0},setup(e,a){let{attrs:n,slots:t}=a;const{themeClasses:s}=W(e),{borderClasses:i}=dt(e),{densityClasses:l}=pe(e),{dimensionStyles:r}=Me(e),{elevationClasses:u}=ft(e),{loaderClasses:v}=xn(e),{locationStyles:g}=yt(e),{positionClasses:y}=Bn(e),{roundedClasses:o}=ee(e),{sizeClasses:d,sizeStyles:b}=fe(e),f=mn(e,e.symbol,!1),C=Cn(e,n),_=m(()=>{var w;return e.active!==void 0?e.active:C.isLink.value?(w=C.isActive)==null?void 0:w.value:f==null?void 0:f.isSelected.value}),E=m(()=>{var $,h;return{color:(f==null?void 0:f.isSelected.value)&&(!C.isLink.value||(($=C.isActive)==null?void 0:$.value))||!f||((h=C.isActive)==null?void 0:h.value)?e.color??e.baseColor:e.baseColor,variant:e.variant}}),{colorClasses:T,colorStyles:x,variantClasses:R}=et(E),L=m(()=>(f==null?void 0:f.disabled.value)||e.disabled),O=m(()=>e.variant==="elevated"&&!(e.disabled||e.flat||e.border)),q=m(()=>{if(!(e.value===void 0||typeof e.value=="symbol"))return Object(e.value)===e.value?JSON.stringify(e.value,null,0):e.value});function X(w){var $;L.value||C.isLink.value&&(w.metaKey||w.ctrlKey||w.shiftKey||w.button!==0||n.target==="_blank")||(($=C.navigate)==null||$.call(C,w),f==null||f.toggle())}return Tn(C,f==null?void 0:f.select),A(()=>{const w=C.isLink.value?"a":e.tag,$=!!(e.prependIcon||t.prepend),h=!!(e.appendIcon||t.append),k=!!(e.icon&&e.icon!==!0);return ge(c(w,{type:w==="a"?void 0:"button",class:["v-btn",f==null?void 0:f.selectedClass.value,{"v-btn--active":_.value,"v-btn--block":e.block,"v-btn--disabled":L.value,"v-btn--elevated":O.value,"v-btn--flat":e.flat,"v-btn--icon":!!e.icon,"v-btn--loading":e.loading,"v-btn--readonly":e.readonly,"v-btn--slim":e.slim,"v-btn--stacked":e.stacked},s.value,i.value,T.value,l.value,u.value,v.value,y.value,o.value,d.value,R.value,e.class],style:[x.value,r.value,g.value,b.value,e.style],"aria-busy":e.loading?!0:void 0,disabled:L.value||void 0,href:C.href.value,tabindex:e.loading||e.readonly?-1:void 0,onClick:X,value:q.value},{default:()=>{var I;return[Ze(!0,"v-btn"),!e.icon&&$&&c("span",{key:"prepend",class:"v-btn__prepend"},[t.prepend?c(ne,{key:"prepend-defaults",disabled:!e.prependIcon,defaults:{VIcon:{icon:e.prependIcon}}},t.prepend):c(se,{key:"prepend-icon",icon:e.prependIcon},null)]),c("span",{class:"v-btn__content","data-no-activator":""},[!t.default&&k?c(se,{key:"content-icon",icon:e.icon},null):c(ne,{key:"content-defaults",disabled:!k,defaults:{VIcon:{icon:e.icon}}},{default:()=>{var Y;return[((Y=t.default)==null?void 0:Y.call(t))??e.text]}})]),!e.icon&&h&&c("span",{key:"append",class:"v-btn__append"},[t.append?c(ne,{key:"append-defaults",disabled:!e.appendIcon,defaults:{VIcon:{icon:e.appendIcon}}},t.append):c(se,{key:"append-icon",icon:e.appendIcon},null)]),!!e.loading&&c("span",{key:"loader",class:"v-btn__loader"},[((I=t.loader)==null?void 0:I.call(t))??c(En,{color:typeof e.loading=="boolean"?void 0:e.loading,indeterminate:!0,width:"2"},null)])]}}),[[dn,!L.value&&!!e.ripple,"",{center:!!e.icon}]])}),{group:f}}});export{fn as A,Sn as B,et as C,mn as D,Cn as E,Ze as F,Mn as G,Ht as H,Zt as I,zn as J,Rn as K,Wn as L,Nn as M,An as N,te as O,Hn as P,On as Q,dn as R,gt as S,In as T,yt as U,tn as V,Bn as W,Dn as X,jn as Y,vt as a,Z as b,dt as c,ft as d,ee as e,Un as f,ne as g,qn as h,Xn as i,se as j,Gn as k,ve as l,ct as m,fe as n,xe as o,pe as p,Kt as q,re as r,Ie as s,Le as t,ae as u,wn as v,xn as w,vn as x,gn as y,Fn as z};