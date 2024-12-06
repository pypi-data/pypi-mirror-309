import{j as e,A as x,b7 as b,du as f,dv as y,l as n,dw as r,dx as P,dy as v,r as w,t as R,dz as L}from"./vendor-BX8_Znqy.js";import{t as z,a4 as E}from"./vendor-arizeai-CtHir-Ua.js";import{E as k,L as $,R as I,r as S,b as j,F as A,A as T,c as C,d as F,P as O,h as D,M as N,e as i,D as B,f as M,g as G,i as W,j as q,k as K,T as _,p as H,l as c,m as J,n as Q,o as p,q as U,s as m,t as g,v as V,w as X,x as Y,y as Z,z as ee,B as u,C as re,S as ae,G as oe,H as te,I as ne,J as se,K as le,N as de}from"./pages-B8FpJuXu.js";import{bR as ie,O as ce,R as pe,bS as me,bT as ge}from"./components-BXIz9ZO8.js";import"./vendor-three-DwGkEfCM.js";import"./vendor-recharts-CJRple0d.js";import"./vendor-codemirror-DLlGiguX.js";(function(){const s=document.createElement("link").relList;if(s&&s.supports&&s.supports("modulepreload"))return;for(const o of document.querySelectorAll('link[rel="modulepreload"]'))d(o);new MutationObserver(o=>{for(const t of o)if(t.type==="childList")for(const l of t.addedNodes)l.tagName==="LINK"&&l.rel==="modulepreload"&&d(l)}).observe(document,{childList:!0,subtree:!0});function h(o){const t={};return o.integrity&&(t.integrity=o.integrity),o.referrerPolicy&&(t.referrerPolicy=o.referrerPolicy),o.crossOrigin==="use-credentials"?t.credentials="include":o.crossOrigin==="anonymous"?t.credentials="omit":t.credentials="same-origin",t}function d(o){if(o.ep)return;o.ep=!0;const t=h(o);fetch(o.href,t)}})();function ue(){return e(b,{styles:a=>x`
        body {
          background-color: var(--ac-global-color-grey-75);
          color: var(--ac-global-text-color-900);
          font-family: "Roboto";
          font-size: ${a.typography.sizes.medium.fontSize}px;
          margin: 0;
          overflow: hidden;
          #root,
          #root > div[data-overlay-container="true"],
          #root > div[data-overlay-container="true"] > .ac-theme {
            height: 100vh;
          }
        }

        /* Remove list styling */
        ul {
          display: block;
          list-style-type: none;
          margin-block-start: none;
          margin-block-end: 0;
          padding-inline-start: 0;
          margin-block-start: 0;
        }

        /* A reset style for buttons */
        .button--reset {
          background: none;
          border: none;
          padding: 0;
        }
        /* this css class is added to html via modernizr @see modernizr.js */
        .no-hiddenscroll {
          /* Works on Firefox */
          * {
            scrollbar-width: thin;
            scrollbar-color: var(--ac-global-color-grey-300)
              var(--ac-global-color-grey-400);
          }

          /* Works on Chrome, Edge, and Safari */
          *::-webkit-scrollbar {
            width: 14px;
          }

          *::-webkit-scrollbar-track {
            background: var(--ac-global-color-grey-100);
          }

          *::-webkit-scrollbar-thumb {
            background-color: var(--ac-global-color-grey-75);
            border-radius: 8px;
            border: 1px solid var(--ac-global-color-grey-300);
          }
        }

        :root {
          --px-blue-color: ${a.colors.arizeBlue};

          --px-flex-gap-sm: ${a.spacing.margin4}px;
          --px-flex-gap-sm: ${a.spacing.margin8}px;

          --px-section-background-color: ${a.colors.gray500};

          /* An item is a typically something in a list */
          --px-item-background-color: ${a.colors.gray800};
          --px-item-border-color: ${a.colors.gray600};

          --px-spacing-sm: ${a.spacing.padding4}px;
          --px-spacing-med: ${a.spacing.padding8}px;
          --px-spacing-lg: ${a.spacing.padding16}px;

          --px-border-radius-med: ${a.borderRadius.medium}px;

          --px-font-size-sm: ${a.typography.sizes.small.fontSize}px;
          --px-font-size-med: ${a.typography.sizes.medium.fontSize}px;
          --px-font-size-lg: ${a.typography.sizes.large.fontSize}px;

          --px-gradient-bar-height: 8px;

          --px-nav-collapsed-width: 45px;
          --px-nav-expanded-width: 200px;
        }

        .ac-theme--dark {
          --px-primary-color: #9efcfd;
          --px-primary-color--transparent: rgb(158, 252, 253, 0.2);
          --px-reference-color: #baa1f9;
          --px-reference-color--transparent: #baa1f982;
          --px-corpus-color: #92969c;
          --px-corpus-color--transparent: #92969c63;
        }
        .ac-theme--light {
          --px-primary-color: #00add0;
          --px-primary-color--transparent: rgba(0, 173, 208, 0.2);
          --px-reference-color: #4500d9;
          --px-reference-color--transparent: rgba(69, 0, 217, 0.2);
          --px-corpus-color: #92969c;
          --px-corpus-color--transparent: #92969c63;
        }
      `})}const he=f(y(n(r,{path:"/",errorElement:e(k,{}),children:[e(r,{path:"/login",element:e($,{})}),e(r,{path:"/reset-password",element:e(I,{}),loader:S}),e(r,{path:"/reset-password-with-token",element:e(j,{})}),e(r,{path:"/forgot-password",element:e(A,{})}),e(r,{element:e(T,{}),loader:C,children:n(r,{element:e(F,{}),children:[e(r,{path:"/profile",handle:{crumb:()=>"profile"},element:e(O,{})}),e(r,{index:!0,loader:D}),n(r,{path:"/model",handle:{crumb:()=>"model"},element:e(N,{}),children:[e(r,{index:!0,element:e(i,{})}),e(r,{element:e(i,{}),children:e(r,{path:"dimensions",children:e(r,{path:":dimensionId",element:e(B,{}),loader:M})})}),e(r,{path:"embeddings",children:e(r,{path:":embeddingDimensionId",element:e(G,{}),loader:W,handle:{crumb:a=>a.embedding.name}})})]}),n(r,{path:"/projects",handle:{crumb:()=>"projects"},element:e(q,{}),children:[e(r,{index:!0,element:e(K,{})}),n(r,{path:":projectId",element:e(_,{}),loader:H,handle:{crumb:a=>a.project.name},children:[e(r,{index:!0,element:e(c,{})}),e(r,{element:e(c,{}),children:e(r,{path:"traces/:traceId",element:e(J,{})})})]})]}),n(r,{path:"/datasets",handle:{crumb:()=>"datasets"},children:[e(r,{index:!0,element:e(Q,{})}),n(r,{path:":datasetId",loader:p,handle:{crumb:a=>a.dataset.name},children:[n(r,{element:e(U,{}),loader:p,children:[e(r,{index:!0,element:e(m,{}),loader:g}),e(r,{path:"experiments",element:e(m,{}),loader:g}),e(r,{path:"examples",element:e(V,{}),loader:X,children:e(r,{path:":exampleId",element:e(Y,{})})})]}),e(r,{path:"compare",handle:{crumb:()=>"compare"},loader:Z,element:e(ee,{})})]})]}),n(r,{path:"/playground",handle:{crumb:()=>"Playground"},children:[e(r,{index:!0,element:e(u,{})}),e(r,{path:"datasets/:datasetId",element:e(u,{}),children:e(r,{path:"examples/:exampleId",element:e(re,{})})}),e(r,{path:"spans/:spanId",element:e(ae,{}),loader:oe,handle:{crumb:a=>a.span.__typename==="Span"?`span ${a.span.context.spanId}`:"span unknown"}})]}),e(r,{path:"/apis",element:e(te,{}),handle:{crumb:()=>"APIs"}}),e(r,{path:"/settings",element:e(ne,{}),handle:{crumb:()=>"Settings"}})]})})]})),{basename:window.Config.basename});function xe(){return e(P,{router:he})}function be(){return e(se,{children:e(ie,{children:e(fe,{})})})}function fe(){const{theme:a}=ce();return e(E,{theme:a,children:e(v,{theme:z,children:n(R.RelayEnvironmentProvider,{environment:pe,children:[e(ue,{}),e(le,{children:e(me,{children:e(de,{children:e(w.Suspense,{children:e(ge,{children:e(xe,{})})})})})})]})})})}const ye=document.getElementById("root"),Pe=L.createRoot(ye);Pe.render(e(be,{}));
