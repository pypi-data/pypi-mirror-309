import{r as o,j as e}from"./@radix-DeK6qiuw.js";import{z as i,i as v,ak as j,av as y,an as S,j as k,u as C,B as w,S as E}from"./index-CCOPpudF.js";import{u as F}from"./update-server-settings-mutation-LwuQfHYn.js";import{t as q}from"./zod-BwEbpOxH.js";import{c as A}from"./@tanstack-DT5WLu9C.js";import{u as I,C as b}from"./index.esm-Dy6Z9Ung.js";import"./@react-router-B3Z5rLr2.js";import"./@reactflow-CK0KJUen.js";const _=i.object({announcements:i.boolean(),updates:i.boolean()});function K({settings:t}){var h,f;const c=o.useId(),d=o.useId(),{toast:l}=v(),u=A(),{mutate:g}=F({onError:s=>{u.invalidateQueries({queryKey:y()}),S(s)&&l({status:"error",emphasis:"subtle",icon:e.jsx(k,{className:"h-5 w-5 shrink-0 fill-error-700"}),description:s.message,rounded:!0})},onSuccess:()=>{u.invalidateQueries({queryKey:y()}),l({status:"success",emphasis:"subtle",rounded:!0,description:"Settings updated successfully"})}}),{control:m,handleSubmit:p,watch:x}=I({resolver:q(_),defaultValues:{announcements:((h=t.body)==null?void 0:h.display_announcements)??void 0,updates:((f=t.body)==null?void 0:f.display_updates)??void 0}});function N({announcements:s,updates:a}){g({display_announcements:s,display_updates:a})}return o.useEffect(()=>{const s=x(()=>p(N)());return()=>s.unsubscribe()},[p,x]),e.jsx("form",{id:"create-user-form",className:"space-y-5",children:e.jsxs("div",{className:"space-y-5",children:[e.jsxs("div",{className:"flex items-center gap-5",children:[e.jsx(b,{control:m,name:"announcements",render:({field:{value:s,onChange:a,ref:n}})=>e.jsx(j,{ref:n,checked:s,onCheckedChange:r=>{a(!!r)},id:c})}),e.jsxs("label",{htmlFor:c,className:"text-text-md",children:[e.jsx("p",{className:"font-semibold",children:"Announcements"}),e.jsx("p",{className:"text-theme-text-secondary",children:"Enable Announcements for important ZenML updates, surveys, and feedback opportunities."})]})]}),e.jsx("hr",{}),e.jsxs("div",{className:"flex items-center gap-5",children:[e.jsx(b,{control:m,name:"updates",render:({field:{value:s,onChange:a,ref:n}})=>e.jsx(j,{ref:n,checked:s,onCheckedChange:r=>{a(!!r)},id:d})}),e.jsxs("label",{htmlFor:d,className:"text-text-md",children:[e.jsx("p",{className:"font-semibold",children:"Updates"}),e.jsx("p",{className:"text-theme-text-secondary",children:"Activate Updates to receive the latest ZenML news and feature releases."})]})]})]})})}function P(){const{data:t}=C({throwOnError:!0});return e.jsxs(w,{className:"flex flex-col gap-5 p-5",children:[e.jsxs("div",{className:"space-y-3",children:[e.jsx("h1",{className:"text-text-xl font-semibold",children:"Notifications"}),e.jsx("p",{className:"text-text-sm text-theme-text-secondary",children:"ZenML comes equipped with default widgets designed to enhance your experience by analyzing usage patterns, gathering your feedback, and ensuring you stay informed about our latest updates and features."})]}),e.jsx("div",{className:"",children:t?e.jsx(K,{settings:t}):e.jsx(E,{className:"h-[250px] w-full"})})]})}export{P as default};
