/* Same SI constants as the Python model; energy eV, position nm. MIT. */
(function(root){
'use strict';
const C=0.03809982106299686;
const add=(a,b)=>[a[0]+b[0],a[1]+b[1]],mul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],scale=(a,s)=>[a[0]*s,a[1]*s],abs2=a=>a[0]*a[0]+a[1]*a[1];
function validate(E,V,a){if(![E,V,a].every(Number.isFinite)||!(E>0&&E<V&&a>=0))throw Error('Require 0 < E < V0 and a >= 0.');}
function transmission(E=.5,V=1,a=.45){validate(E,V,a);if(a===0)return 1;const z=Math.sqrt((V-E)/C)*a,ls=z+Math.log(-Math.expm1(-2*z))-Math.log(2),lt=2*Math.log(V)+2*ls-Math.log(4*E*(V-E));return lt>700?0:1/(1+Math.exp(lt));}
function state(E=.5,V=1,a=.45){validate(E,V,a);const k=Math.sqrt(E/C),q=Math.sqrt((V-E)/C),ch=Math.cosh(q*a),sh=Math.sinh(q*a),D=[ch,.5*(q/k-k/q)*sh],den=abs2(D),t=[D[0]/den,-D[1]/den],r=add(mul(t,[ch,-k/q*sh]),[-1,0]);return{T:abs2(t),R:abs2(r),psi(x){if(x<0)return add([Math.cos(k*x),Math.sin(k*x)],mul(r,[Math.cos(k*x),-Math.sin(k*x)]));if(x>a)return mul(t,[Math.cos(k*(x-a)),Math.sin(k*(x-a))]);return mul(t,[Math.cosh(q*(a-x)),-k/q*Math.sinh(q*(a-x))]);}};}
root.Quantum={C,transmission,state,abs2};
if(typeof module!=='undefined')module.exports=root.Quantum;
})(typeof window!=='undefined'?window:globalThis);
